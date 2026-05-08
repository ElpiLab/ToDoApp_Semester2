from nicegui import ui

from ui.controllers import create_task, delete_task, complete_task, get_tasks


@ui.page('/')
def index_page():
    ui.label('ToDo App').classes('text-2xl font-bold')

    title_input = ui.input('Title')
    description_input = ui.input('Description')
    priority_select = ui.select(
        ['low', 'medium', 'high'],
        value='medium',
        label='Priority',
    )
    due_date_input = ui.input('Due Date (YYYY-MM-DD)')

    def handle_create():
        create_task(
            title_input.value,
            description_input.value,
            priority_select.value,
            due_date_input.value if due_date_input.value else None,
        )
        refresh_tasks()

    ui.button('Create Task', on_click=handle_create)

    task_list_container = ui.column()

    def refresh_tasks():
        task_list_container.clear()

        with task_list_container:
            tasks = get_tasks()

            if not tasks:
                ui.label('No tasks yet.')
                return

            for task in tasks:
                with ui.card().classes('w-full'):
                    ui.label(f'{task.title} ({task.priority})')
                    ui.label(task.description)
                    ui.label(f'Status: {task.status}')
                    ui.label(f'Due Date: {task.due_date}')

                    with ui.row():
                        ui.button(
                            'Complete',
                            on_click=lambda task_id=task.id: [complete_task(task_id), refresh_tasks()],
                        )
                        ui.button(
                            'Delete',
                            on_click=lambda task_id=task.id: [delete_task(task_id), refresh_tasks()],
                        )

    refresh_tasks()