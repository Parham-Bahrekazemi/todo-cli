

from typer.testing import CliRunner

from todo import __app_name__ , __version__,cli,DB_READ_ERROR,SUCCESS,todo

import json
import pytest


runner = CliRunner()



@pytest.fixture
def mock_json_file(tmp_path):

    todo = [
        {
            'description' : 'Get Some Milk',
            'priority' : 1,
            'done' : False
        }
    ]

    db_file = tmp_path / 'todo.json'
    with db_file.open('w') as db:
        json.dump(todo, db , indent=4)
    return db_file


test_data1 = {
    'description' : ['clean' , 'the' , 'house'],
    'priority' : 1,
    'todo':{
        'description' : 'clean the house.',
        'priority' : 1,
        'done' : False
    }
}

test_data2 = {
    'description' : ['wash the car'],
    'priority' : 2,
    'todo':{
        'description' : 'wash the car.',
        'priority' : 2,
        'done' : False
    }
}


@pytest.mark.parametrize(
        'description, priority, expected',
        [
            pytest.param(test_data1['description'], test_data1['priority'],(test_data1['todo'] , SUCCESS)),
            pytest.param(test_data2['description'], test_data2['priority'],(test_data2['todo'] , SUCCESS)),
        ],
)

def test_add(mock_json_file , description , priority , expected):
    todoer = todo.Todoer(mock_json_file)
    assert todoer.add(description , priority) == expected
    read = todoer.db_handler.read_todos()
    assert len(read.todo_list) == 2

def test_version():
    result = runner.invoke(cli.app,['--version'])
    assert result.exit_code == 0
    assert f'{__app_name__} version {__version__}\n' in result.stdout