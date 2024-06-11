from puddle.config import InitConfig, Config
from puddle.collection import opendb
import os.path
import os
import chromadb
from pydantic import DirectoryPath, FilePath 

def init(force = False) -> Config:

    iconf = InitConfig()

    rcfile = os.path.join(iconf.home, "config")

    # If a config already exists, just load it and go on
    if (not force) and os.path.isfile(rcfile):

        with open(rcfile, "r") as fh:
            json_config = fh.read()
            config = Config.model_validate_json(json_config)

    # Otherwise, create everything as needed
    else:

        datadir = os.path.join(iconf.home, "data")

        if not os.path.isdir(iconf.home):
            os.makedirs(iconf.home)

        if not os.path.isdir(datadir):
            os.makedirs(datadir)

        # remake rcfile
        with open(rcfile, "w") as fh:
            print("", file=fh)

        chromafile = os.path.join(iconf.home, "chromadb")
        collection = "puddle"
        opendb(chromafile, collection)

        config = Config(
            home = DirectoryPath(iconf.home),
            rc = FilePath(rcfile),
            chromadb = FilePath(chromafile),
            collection = collection,
            datadir = DirectoryPath(datadir),
        )

        config_json = config.model_dump_json(indent=2)
        with open(rcfile, "w") as fh:
            print(config_json, file=fh)

    return config
