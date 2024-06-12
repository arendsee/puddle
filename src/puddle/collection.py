from puddle.config import load_config
import glob
import chromadb
from chromadb.api.types import Metadata, OneOrMany
import os.path
import os
import time
from typing import List, Tuple

text_extensions = [".hs"]

def opendb(path, collection):
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection(name=collection)
    return (client, collection)

def opencol() -> chromadb.Collection: 
    config = load_config()
    client = chromadb.PersistentClient(path=str(config.chromadb))
    collection = client.get_or_create_collection(name=config.collection)
    return collection

def lines2chunks(lines : List[str], chunk_size : int = 30) -> List[str]:
    chunks = []
    for i in range(len(lines) // chunk_size):
        chunks.append(lines[i*chunk_size:i*chunk_size+chunk_size])
    return chunks


def process_text(file : str) -> Tuple[List[str], List[str], OneOrMany[Metadata]]:
    timestamp = time.ctime()
    with open(file, "r") as fh:
        ids = []
        documents = []
        metadatas = []
        lineno = 0

        for (i, chunk) in enumerate(lines2chunks(fh.readlines())):
            ids.append(f"{file}:{lineno}-{lineno+len(chunk)}")
            documents.append("".join(chunk))
            metadatas.append({
              "file" : file,
              "timestamp" : str(timestamp),
              "chunk_id" : str(i),
              "total_chunks" : str(len(chunk))
            })
            lineno += len(chunk)

        return (ids, documents, metadatas)

def update() -> None:
    config = load_config()
    _, collection = opendb(str(config.chromadb), config.collection)
    for file in glob.iglob(os.path.join(config.datadir, "**"), recursive=True):
        extsplit = os.path.splitext(file)
        if (len(extsplit) == 2 and extsplit[1] in text_extensions):
            (ids, documents, metadatas) = process_text(file)
            # ignore empty files
            if(len(ids) > 0):
                collection.upsert(
                    ids = ids,
                    documents = documents,
                    metadatas = metadatas,
                )

def query(collection : chromadb.Collection, txt : str, n : int = 1) -> chromadb.QueryResult:
    return collection.query(
        query_texts=[txt],
        n_results=n,
    )
