from pytest_mock import mocker
from typer.testing import CliRunner

from project import app, delete_task, add_task, move_task, focus, clear_board

runner = CliRunner()

def test_show(mocker):
    # Create a mock-up for the get_do, get_doing, get_done
    mocker.patch("project.get_do", return_value=[(1, "Task 1"), (2, "Task 2")])
    mocker.patch("project.get_doing", return_value=[(3, "Task 3"), (4, "Task 4")])
    mocker.patch("project.get_done", return_value=[(5, "Task 5"), (6, "Task 6")])
    result = runner.invoke(app, ["show"])

    assert "Kanban" in result.stdout
    assert "Do" in result.stdout
    assert "Doing" in result.stdout
    assert "Done" in result.stdout
    assert "Task 1" in result.stdout
    assert "Task 3" in result.stdout
    assert "Task 5" in result.stdout

def test_delete(mocker):

    mocker.patch("project.get_do", return_value=[(1, "Task 1"), (2, "Task 2")])
    mocker.patch("project.get_doing", return_value=[(3, "Task 3"), (4, "Task 4")])
    mocker.patch("project.get_done", return_value=[(5, "Task 5"), (6, "Task 6")])
    delete_task_mock = mocker.patch("project.delete_task")

    result = runner.invoke(app, ["delete", "do", "1"])
    assert "Deleted Task 1 from \'Do\'" in result.stdout

    # Check if the function was called
    delete_task_mock.assert_called_with("Task 1", "do")

    result = runner.invoke(app, ["delete", "doing", "2"])
    assert "Deleted Task 4 from \'Doing\'" in result.stdout

    # Check if the function was called
    delete_task_mock.assert_called_with("Task 4", "doing")


def test_do(mocker):
    do_mock = mocker.patch("project.add_task")

    result = runner.invoke(app, ["do", "Something"])
    assert "Added Something to \'Do\'" in result.stdout
    do_mock.assert_called_with("Something")


def test_doing(mocker):
    mocker.patch("project.get_do", return_value=[(1, "Do 1"), (2, "Do 2")])
    doing_mock = mocker.patch("project.move_task")

    result = runner.invoke(app, ["doing", "1"])
    assert "Moved Do 1 from \'Do\' to \'Doing\'" in result.stdout
    doing_mock.assert_called_with("Do 1", doing=True)


def test_done(mocker):
    mocker.patch("project.get_doing", return_value=[(1, "Doing 1"), (2, "Doing 2")])
    doing_mock = mocker.patch("project.move_task")

    result = runner.invoke(app, ["done", "2"])
    assert "Moved Doing 2 from \'Doing\' to \'Done\'" in result.stdout
    doing_mock.assert_called_with("Doing 2", done=True)


def test_focus(mocker):
    mocker.patch("project.get_doing", return_value=[(1, "Doing 1"), (2, "Doing 2")])

    result = runner.invoke(app, ["focus", "1"])
    assert "Focus" in result.stdout
    assert "Doing 1" in result.stdout


def test_clear(mocker):
    mocker.patch("project.typer.confirm", return_value=True)
    clear_board_mock = mocker.patch("project.clear_board")

    result = runner.invoke(app, ["clear"])

    assert "All tasks have been deleted" in result.stdout
    clear_board_mock.assert_called_once()