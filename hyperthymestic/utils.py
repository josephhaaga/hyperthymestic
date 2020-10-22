from hashlib import sha256
from pathlib import Path
from typing import Mapping

from appdirs import AppDirs
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hyperthymestic import __version__
from hyperthymestic.models import Base


def dirs() -> AppDirs:
    return AppDirs("hyperthymestic", "K Street Labs", version=__version__)


def config_file_path() -> Path:
    return Path(dirs().user_config_dir) / "hyperthymestic.conf"


def database_file_path() -> Path:
    return Path(dirs().user_data_dir) / "data.sqlite3"


def get_config() -> Mapping:
    config_file = config_file_path()
    config_directory = config_file.parents[0]
    config_directory.mkdir(parents=True, exist_ok=True)
    config_file.touch(exist_ok=True)
    conf = ConfigParser()
    conf.read(config_file)
    return conf


def write_config(conf_map: Mapping) -> None:
    conf_file_path = config_file_path()
    print(f"Writing to config: {conf_file_path}")
    with open(conf_file_path, 'w') as configfile:
        conf_map.write(configfile)

def get_database():
    db_filepath = database_file_path()
    db_filepath.touch(mode=0o775, exist_ok=True)
    engine = create_engine("sqlite:///"+str(db_filepath), echo=False)
    session = sessionmaker(bind=engine)
    return engine, session()

def create_tables():
    eng, _ = get_database()
    Base.metadata.create_all(eng)
    print(f"Created tables!")


def hash_file(filepath: Path) -> str:
    h = sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
        return h.hexdigest()


