from nicegui import ui
from nicegui import ui, app
from datetime import date

from ui.controllers import create_task, delete_task, complete_task, get_tasks, update_task

# State for current filter
current_filter = 'all'
search_text = ''  # NEW: Store search text

def get_priority_color(priority):
    """Return color for priority level"""
    if priority == 'high':
        return 'red'
    elif priority == 'medium':
        return 'orange'
    else:
        return 'green'

@ui.page('/')
def index_page():
    ui.label('Student Task Manager').classes('text-2xl font-bold')

    title_input = ui.input('Title')
    description_input = ui.input('Description')
    priority_select = ui.select(
        ['low', 'medium', 'high'],
        value='medium',
        label='Priority',
    )
    due_date_input = ui.input('Due Date (YYYY-MM-DD)')

    # NEW: Search input
    with ui.row().classes('w-full items-center gap-4 my-2'):
        ui.label('Filter:').classes('font-bold')
        
        # Filter buttons
        ui.button('All', on_click=lambda: set_filter('all')).props('flat')
        ui.button('Pending', on_click=lambda: set_filter('pending')).props('flat')
        ui.button('Completed', on_click=lambda: set_filter('completed')).props('flat')
        
        # Spacer to push search to the right
        ui.space()
        
        # NEW: Search box
        search_input = ui.input(placeholder='🔍 Search by title...').props('clearable')
        search_input.classes('w-64')
        
        def on_search():
            global search_text
            search_text = search_input.value if search_input.value else ''
            refresh_tasks()
        
        search_input.on('change', on_search)

    def handle_create():
        create_task(
            title_input.value,
            description_input.value,
            priority_select.value,
            due_date_input.value if due_date_input.value else None,
        )
        refresh_tasks()
        # Clear form
        title_input.value = ''
        description_input.value = ''
        due_date_input.value = ''

    ui.button('Create Task', on_click=handle_create, icon='add')

    task_list_container = ui.column()

    def set_filter(filter_value):
        global current_filter
        current_filter = filter_value
        refresh_tasks()

    def edit_task(task_id):
        """Open edit dialog for a task"""
        task = next((t for t in get_tasks() if t.id == task_id), None)
        if not task:
            return
        
        with ui.dialog() as dialog, ui.card().classes('w-full min-w-[400px]'):
            ui.label('Edit Task').classes('text-h5 mb-4')
            
            edit_title = ui.input('Title', value=task.title)
            edit_description = ui.input('Description', value=task.description)
            edit_priority = ui.select(
                ['low', 'medium', 'high'],
                value=task.priority,
                label='Priority'
            )
            edit_due_date = ui.input('Due Date', value=task.due_date if task.due_date else '')
            
            def save_changes():
                updated_task = task
                updated_task.title = edit_title.value
                updated_task.description = edit_description.value
                updated_task.priority = edit_priority.value
                updated_task.due_date = edit_due_date.value if edit_due_date.value else None
                update_task(updated_task)
                refresh_tasks()
                dialog.close()
                ui.notify('Task updated!', type='positive')
            
            with ui.row().classes('justify-end w-full mt-4 gap-2'):
                ui.button('Cancel', on_click=dialog.close).props('flat')
                ui.button('Save', on_click=save_changes).props('color=primary')
        
        dialog.open()

    def refresh_tasks():
        task_list_container.clear()

        with task_list_container:
            all_tasks = get_tasks()
            
            # Sort by due date
            all_tasks.sort(key=lambda x: x.due_date if x.due_date else date(9999, 12, 31))
            
            # Apply status filter
            if current_filter == 'pending':
                tasks = [t for t in all_tasks if not t.completed]
            elif current_filter == 'completed':
                tasks = [t for t in all_tasks if t.completed]
            else:
                tasks = all_tasks
            
            # NEW: Apply search filter by title
            if search_text:
                tasks = [t for t in tasks if search_text.lower() in t.title.lower()]
                if tasks:
                    ui.label(f'🔍 Found {len(tasks)} task(s) matching "{search_text}"').classes('text-caption mb-2')

            if not tasks:
                if search_text:
                    ui.label(f'No tasks found matching "{search_text}"').classes('text-center p-4')
                else:
                    ui.label('No tasks yet.')
                return

            for task in tasks:
                with ui.card().classes('w-full'):
                    # Title with color-coded priority badge
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label(f'{task.title}').classes('text-h6')
                            priority_color = get_priority_color(task.priority)
                            ui.badge(task.priority, color=priority_color).classes('text-white')
                        status_color = 'green' if task.completed else 'blue'
                        ui.badge(task.status, color=status_color).classes('text-white')
                    
                    if task.description:
                        ui.label(task.description).classes('text-grey-7 mt-2')
                    
                    ui.label(f'📅 Due: {task.due_date if task.due_date else "Not set"}').classes('text-caption mt-1')

                    with ui.row().classes('mt-2 gap-2'):
                        if not task.completed:
                            ui.button(
                                'Complete',
                                on_click=lambda tid=task.id: [complete_task(tid), refresh_tasks()],
                                icon='check_circle',
                            ).props('flat color=green')
                        ui.button(
                            'Edit',
                            on_click=lambda tid=task.id: edit_task(tid),
                            icon='edit',
                        ).props('flat color=orange')
                        ui.button(
                            'Delete',
                            on_click=lambda tid=task.id: [delete_task(tid), refresh_tasks()],
                            icon='delete',
                        ).props('flat color=red')

    refresh_tasks()