import configparser

from pathlib import Path

from typing import Any , Dict , NamedTuple , List

from todo import DB_WRITE_ERROR , SUCCESS , DB_READ_ERROR , JSON_ERROR

import json


DEFAULT_DB_FILE_PATH = Path.home().joinpath('.' + Path.home().stem + '_todo.json')


class DBResponse(NamedTuple):
    
    todo_list: list[Dict[str , Any]]
    error : int


class DatabaseHandler:
    def __init__(self, db_path : Path):
        self.db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self.db_path.open('r') as db:
                try:
                    todo_list = json.load(db)
                    return DBResponse(todo_list, SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([] , JSON_ERROR)
        except OSError:
            return DBResponse([] , DB_READ_ERROR)
    
    def write_todos(self , todo_list : List[Dict[str , Any]]) -> DBResponse:

        try:
            with self.db_path.open('w') as db:
                json.dump(todo_list , db , indent=4)
            return DBResponse(todo_list , SUCCESS)
        except OSError:
           return DBResponse([] , DB_READ_ERROR)




def get_database_path(config_file : Path) -> Path:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser['General']['database'])


def init_database(db_path : Path) -> int:
    try:
        db_path.write_text('[]')
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR