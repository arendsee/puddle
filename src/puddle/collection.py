from puddle.config import load_config
import glob
import chromadb
import os.path
import os
import time

supported_extensions = [".hs"]

def opendb(path, collection):
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection(name=collection)
    return (client, collection)

def opencol() -> chromadb.Collection: 
    config = load_config()
    client = chromadb.PersistentClient(path=str(config.chromadb))
    collection = client.get_or_create_collection(name=config.collection)
    return collection

def update() -> None:
    config = load_config()
    _, collection = opendb(str(config.chromadb), config.collection)
    for file in glob.iglob(os.path.join(config.datadir, "**"), recursive=True):
        extsplit = os.path.splitext(file)
        if (len(extsplit) == 2 and extsplit[1] in supported_extensions):
            with open(file, "r") as fh:
                collection.upsert(
                    ids = [file],
                    documents = [fh.read()],
                    metadatas = [{"timestamp" : time.ctime()}],
                )

def query(collection : chromadb.Collection, txt : str) -> chromadb.QueryResult:
    return collection.query(
        query_texts=[txt],
        n_results=3,
    )
