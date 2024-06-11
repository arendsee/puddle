from pydantic import BaseModel, DirectoryPath, FilePath
import os.path

class InitConfig(BaseModel):
    home : str = os.path.expanduser("~/.puddle")


class Config(BaseModel):
    home : DirectoryPath
    rc : FilePath
    chromadb : DirectoryPath
    datadir : DirectoryPath
    collection : str

def load_config() -> Config:
    iconf = InitConfig()
    rcfile = os.path.join(iconf.home, "config")
    with open(rcfile, "r") as fh:
        return Config.model_validate_json(fh.read())
