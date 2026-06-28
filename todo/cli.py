''' this module provides the to-do cli '''


from typing import Optional , List
import typer
from pathlib import Path
from todo import __version__ , __app_name__ , ERRORS , config ,database , todo


app = typer.Typer()

@app.command()
def init(
    db_path : str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        '--db-path',
        '-db',
        prompt='to-do database location??',
    )
):
    app_init_error = config.init_app(db_path)

    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed "{ERRORS[db_init_error]}"'
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f'to-do database is {db_path}'
        )


def get_todoer()-> todo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(f'Config file not found. please run "todo init" first')
        raise typer.Exit(1)
    if db_path.exists():
        todoer = todo.Todoer(db_path)
        return todoer
    else:
        typer.secho(f'Database file not found. please run "todo init" first')
        raise typer.Exit(1)
    

@app.command()
def add(description : List[str] = typer.Argument(
        ...,
    ),
    priority : int = typer.Option(2 , '--priority' , '-p' , min=1 , max=3)
    ):

    todoer = get_todoer()
    todo , error = todoer.add(description , priority)
    if error:
        typer.secho(f'Adding task failed with "{ERRORS[error]}"')
        raise typer.Exit(1)
    else:
        typer.secho(f'''todo "{todo['description']}" was added''' f'''with priority {priority}''')


@app.command(name='list')
def list_all():
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    if len(todo_list) == 0:
        typer.secho('no task find')
        raise typer.Exit()
    typer.secho('\nto-do list:\n')
    columns = (
        'ID ',
        '| priority ',
        '| done ',
        '| description ',

    )

    header = ''.join(columns)

    typer.secho(header)
    typer.secho('-' * len(header))

    for id , todo in enumerate(todo_list , 1):
        desc , priority , done = todo.values()
        typer.secho(f'{id}{(len(columns[0] ) - len(str(id))) * ' '}' f'| ({priority}){(len(columns[1]) - len(str(priority)) -4)  * ' '}'
                     f'| ({done}){(len(columns[2]) - len(str(done)) - 2)  * ' '}' f'| {desc}')

    typer.secho('-' * len(header) + '\n')


@app.command(name='complete')
def set_done(todo_id : int = typer.Argument(...)):
    todoer = get_todoer()
    todo , error = todoer.set_done(todo_id)
    if error:
        typer.secho(f'setting as task done failed with "{ERRORS[error]}"')
        raise typer.Exit(1)
    else:
        typer.secho(f'''todo # {todo_id} "{todo['description']}" completed ''')

@app.command()
def remove(todo_id : int = typer.Argument(...) ,  force: bool = typer.Option(
        False,
        '--force',
        '-f'
    )
):
    todoer = get_todoer()
    

    def _remove():
        todo , error = todoer.remove(todo_id)
        if error:
            typer.secho(f'removing todo #{todo_id} failed with "{ERRORS[error]}"')
            raise typer.Exit(1)
        else:
            typer.secho(f'''todo # {todo_id}:"{todo['description']}" was removed ''')

    if force:
        _remove()
    else:
        todo_list = todoer.get_todo_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho(f'''invalid todo id # {todo_id}''')
            raise typer.Exit(1)
        delete =  typer.confirm(f'Are you sure want to remove todo # {todo_id} : {todo['description']}?')

        if delete:
            _remove()
        else:
            typer.secho(f'''operation canceled''')


@app.command('clear')
def remove_all(force: bool = typer.Option(
        ...,
        prompt='Are you sure want to remove all tasks?',
    )):
    todoer = get_todoer()
    if force:
        error = todoer.remove_all().error
        if error :
            typer.secho(f'removing all tasks failed with "{ERRORS[error]}"')
            raise typer.Exit(1)
        else:
            typer.secho('All task removed')

    else:
         typer.secho(f'''operation canceled''')



def __version_callback(value : bool):
    if value:
        typer.echo(f'{__app_name__} version {__version__}')
        raise typer.Exit()


@app.callback()
def main(version : Optional[bool] = typer.Option(None , '--version' , '-v' , is_eager=True , help='Show the version and exit' , callback=__version_callback)):
    return 
