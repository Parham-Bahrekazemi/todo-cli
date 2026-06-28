
from pathlib import Path
from todo.database import DatabaseHandler
from typing import Any , Dict , NamedTuple,List
from todo import DB_READ_ERROR , ID_ERROR

class CurrentTodo(NamedTuple):

    todo: Dict[str , Any]
    error : int



class Todoer:

    def __init__(self , db_path : Path):
        self.db_handler= DatabaseHandler(db_path)

    def add(self , description :List[str], priority : int = 2) -> CurrentTodo:
        description_text = ' '.join(description)
        if not description_text.endswith('.'):
            description_text += '.'

        todo = {
            'description' : description_text,
            'priority' : priority,
            'done' : False,
        }

        read = self.db_handler.read_todos()

        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo ,read.error)
        
        read.todo_list.append(todo)
        write = self.db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo , write.error)
    

    def get_todo_list(self) -> list[dict]:
        read = self.db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return []
        return read.todo_list
    
    def set_done(self , todo_id : int) -> CurrentTodo:
        read = self.db_handler.read_todos()
        if read.error:
            return CurrentTodo({} , read.error)
        
        try:
            todo = read.todo_list[todo_id - 1] 
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo['done'] = True
        write = self.db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo  , write.error)
    
    def remove(self , todo_id : int)-> CurrentTodo:
        read = self.db_handler.read_todos()
        if read.error:
            return CurrentTodo({} , read.error)
        try:
            todo = read.todo_list[todo_id - 1] 
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        read.todo_list.remove(todo)
        write = self.db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo  , write.error)
    
    def remove_all(self)-> CurrentTodo:
        write = self.db_handler.write_todos([])
        return CurrentTodo({} , write.error)

        


