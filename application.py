from nicegui import ui
from data_access.db import create_db_and_tables
from ui import pages

def run() -> None:
    create_db_and_tables()
    ui.run(
        title="Student Task Manager",
        port=8081,  # Changed from default 8080 to 8081
        host='127.0.0.1',
        reload=False  # Disable auto-reload to avoid conflicts
    )

# This line is crucial - actually call the function
if __name__ == '__main__':
    run()