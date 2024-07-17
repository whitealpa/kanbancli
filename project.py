from enum import Enum
import sys

import typer
from rich.console import Console
from rich.table import Table

from data import (
    get_do, get_doing, get_done,
    add_task, delete_task, move_task, move_task_back,
    clear_board
)


app = typer.Typer()
console = Console()


def main():
    """
    If no command-line arguments are provided, the `show` command is executed by default.
    """
    if len(sys.argv) == 1:
        show()
    else:
        app()


@app.command(short_help="Show the kanban board")
def show():
    """
    Show the kanban board with # column as TASK_ID
    """
    do_tasks = get_do()
    doing_tasks = get_doing()
    done_tasks = get_done()

    # Create a matrix from the data
    max_length = (max(len(do_tasks), len(doing_tasks), len(done_tasks )))
    tasks = [["", "", ""] for _ in range(max_length)]

    for i in range(len(do_tasks)):
        tasks[i][0] = do_tasks[i][1]

    for i in range(len(doing_tasks)):
        tasks[i][1] = doing_tasks[i][1]

    for i in range(len(done_tasks)):
        tasks[i][2] = done_tasks[i][1]

    # Create the table using Rich
    table = Table(title="Kanban", title_style="bold", show_header=True, header_style="yellow bold")
    table.add_column("#")
    table.add_column("Do")
    table.add_column("Doing")
    table.add_column("Done")

    for idx, task in enumerate(tasks):
        table.add_row(str(idx + 1), task[0], task[1], task[2])

    print()
    console.print(table)
    print()


class DeleteColumn(str, Enum):
    do = "do"
    doing = "doing"
    done = "done"

@app.command(short_help="Delete a task from a specific column")
def delete(column: DeleteColumn, task_id: int):
    """
    Delete a task from a specific column using task_id to specify the row.
    """
    if column.value == "do":
        tasks = get_do()
    if column.value == "doing":
        tasks = get_doing()
    if column.value == "done":
        tasks = get_done()


    task = tasks[task_id - 1][1]

    delete_task(task, column.value)
    print()
    console.print(f"Deleted [bold]{task}[/bold] from \'{column.value.title()}\'")

    show()


@app.command(short_help="Add a task to \'Do\'")
def do(task: str):
    """
    Add a task to the 'Do' column
    """
    add_task(task)
    print()
    console.print(f"Added [bold]{task}[/bold] to \'Do\'")

    show()


@app.command(short_help="Move a task from \'Do\' to \'Doing\' || from 'Doing' to 'Do' with --back")
def doing(task_id: int, back: bool=False):
    """
    Move as task from the 'Do' column to 'Doing' column.
    Use --back to move from 'Doing' column to 'Done' column
    """
    if not back:
        tasks = get_do()
        task = tasks[task_id - 1][1]

        move_task(task, doing=True)
        print()
        console.print(f"Moved [bold]{task}[/bold] from \'Do\' to \'Doing\'")


    if back:
        tasks = get_doing()
        task = tasks[task_id - 1][1]

        move_task_back(task, doing=True)
        print()
        console.print(f"Moved [bold]{task}[/bold] back from \'Doing\' to \'Do\'")

    show()


@app.command(short_help="Move a task from \'Doing\' to \'Done\' || from 'Done' to 'Doing' with --back")
def done(task_id: int, back: bool=False):
    """
    Move as task from the 'Doing' column to 'Done' column.
    Use --back to move from 'Done' column to 'Doing' column
    """
    if not back:
        tasks = get_doing()
        task = tasks[task_id - 1][1]

        move_task(task, done=True)
        print()
        console.print(f"Moved [bold]{task}[/bold] from \'Doing\' to \'Done\'")

    if back:
        tasks = get_done()
        task = tasks[task_id - 1][1]

        move_task_back(task, done=True)
        print()
        console.print(f"Moved [bold]{task}[/bold] back from \'Done\' to \'Doing\'")

    show()


@app.command(short_help="Focus on a single task on \'Doing\'")
def focus(task_id: int):
    """
    Enter 'Focus Mode' with a single task from the 'Doing' column
    """
    tasks = get_doing()
    task = tasks[task_id - 1][1]

    table = Table(title="Kanban", title_style="bold", show_header=True, header_style="blue bold")
    table.add_column("Focus")
    table.add_row(task)

    print()
    console.print(table)
    print()


@app.command(short_help="Clear all tasks from the board")
def clear():
    """
    Clear all tasks from the board
    """
    confirmation = typer.confirm("Are you sure you want to delete all tasks?")
    if confirmation:
        clear_board()
        console.print(f"[bold red]All tasks have been deleted[/bold red]")
        show()

if __name__ == "__main__":
    main()