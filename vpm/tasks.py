import typer
from typing_extensions import Annotated
from rich import print
import json
from datetime import datetime
from vpm.services.elements import TaskService, ElementService
from vpm.models.tasks import Task, TaskType
from vpm.utils.helpers import serialize

app = typer.Typer(no_args_is_help=True)
task_service = TaskService()
element_service = ElementService()

@app.command(help="Adds a new task to the local database.")
def add(
    element_name: Annotated[str, typer.Option(prompt="Element name", help="Name of the element to add the task to")],
    name: Annotated[str, typer.Option(prompt="Task name", help="Name of the task")],
    description: Annotated[str, typer.Option(prompt="Description", help="Description of how to complete the task")] = None,
    due_date: Annotated[datetime | None, typer.Option(prompt="Due date (YYYY-MM-DD)", help="Due date of the task")] = None,
    interval_unit: Annotated[str | None, typer.Option(prompt="Interval unit", help="Unit for interval (daily, weekly, monthly, yearly)")] = None,
    interval: Annotated[int | None, typer.Option(prompt="Interval", help="Interval for recurring task")] = None
) -> None:
    element = element_service.get_by_name(name=element_name)
    try:
        new_task = Task(
            element_id=element.id,
            name=name,
            description=description,
            due_date=due_date,
            interval=interval,
            interval_unit=interval_unit,
        )
        task = task_service.create(new_task)
        print(json.dumps(task.model_dump(), indent=4, default=serialize))
    except ValueError:
        print(f"Error: Invalid task type. Must be one of: {', '.join(t.value for t in TaskType)}")
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Get task information")
def get(
    name: Annotated[str, typer.Option(prompt="Task name")]
) -> None:
    task = task_service.get_by_name(name=name)
    print(json.dumps(task.model_dump(), indent=4, default=serialize))

@app.command(help="Update task information")
def update(
    name: Annotated[str, typer.Option(prompt="Task name")],
    new_name: Annotated[str | None, typer.Option()] = None,
    type: Annotated[str | None, typer.Option(help="Type of task (MAINTENANCE, REPAIR, REPLACE, INSPECT)")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    due_date: Annotated[datetime | None, typer.Option()] = None,
    priority: Annotated[int | None, typer.Option()] = None
) -> None:
    try:
        task = task_service.get_by_name(name=name)
        args = {k: v for k, v in locals().items() if v is not None and k != 'name'}
        if 'type' in args:
            args['type'] = TaskType(args['type'].upper())
        result = task_service.update(item_id=task.id, **args)
        print(json.dumps(result.model_dump(), indent=4, default=serialize))
    except ValueError:
        print(f"Error: Invalid task type. Must be one of: {', '.join(t.value for t in TaskType)}")
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Get all tasks")
def all() -> None:
    tasks = task_service.get_all()
    for task in tasks:
        print(json.dumps(task.model_dump(), indent=4, default=serialize))

@app.command(help="Delete a task")
def delete(
    name: Annotated[str, typer.Option(prompt="Task name")]
) -> None:
    try:
        task = task_service.get_by_name(name=name)
        task_service.delete(item_id=task.id)
        print(f'Task "{name}" deleted successfully')
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Mark a task as complete")
def complete(
    name: Annotated[str, typer.Option(prompt="Task name")]
) -> None:
    try:
        task = task_service.get_by_name(name=name)
        
        # Mark current task as complete
        result = task_service.update(
            item_id=task.id,
            complete=True,
            completed_at=datetime.now()
        )
        print(f'Task "{name}" marked as complete')
        
    except Exception as e:
        print(f"Error: {str(e)}")
    if task.interval is not None:
        new_task = task_service.create_recurring_task(task)
        print(json.dumps(new_task.model_dump(), indent=4, default=serialize))

if __name__ == "__main__":
    app() 