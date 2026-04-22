# ToDoApp_Semester2
## 📝 Application To Do

---

### Problem

First-year students often struggle to manage multiple assignments, deadlines, and study tasks across different modules. This leads to poor prioritization, procrastination, and last-minute stress.

Without a centralized system, tasks are scattered and difficult to track, resulting in missed deadlines, inefficient study time, and reduced academic performance.

---

### Scenario

A student opens the To-Do App in their browser to manage all academic tasks in one place.

They can create tasks with titles, descriptions, priorities, and due dates. The system validates inputs, stores tasks in a database, and allows the user to view, update, complete, or delete tasks.

This helps the student stay organized, track progress, and improve productivity.

---

## User Stories

### 1. Create Task
As a student, I want to create a new task with details so that I can track my work.
Description: The user creates a task with title, description, priority, and due date.  
Inputs: title `str`, description `str`, priority `str`, due_date `date`  
Outputs: task saved in database  

---

### 2. View Tasks
As a student, I want to view all my tasks so that I can see my workload.
Description: The application displays all tasks.  
Inputs: none  
Outputs: list of tasks (`list[Task]`)  

---

### 3. Mark Task as Complete
As a student, I want to mark tasks as complete so that I can track progress.  
Description: The user updates a task’s status to completed.  
Inputs: task_id `int`  
Outputs: updated task status  

---

### 4. Delete Task
As a student, I want to delete tasks so that I can remove unnecessary items.  
Description: The user deletes a task from the system.  
Inputs: task_id `int`  
Outputs: task removed  

---

### 5. Edit Task
As a student, I want to edit a task so that I can update its details.
Description: The user modifies task attributes.  
Inputs: task_id `int`, updated fields  
Outputs: updated task  

---

### 6. Set Priority
As a student, I want to assign priority levels so that I can focus on important tasks. 
Description: Tasks can be categorized as Low, Medium, or High priority.  
Inputs: priority (`Low | Medium | High`)  
Outputs: prioritized tasks  

---

### 7. Add Due Date
As a student, I want to assign due dates so that I can manage deadlines.
Description: Each task includes a deadline.  
Inputs: due_date `date`  
Outputs: task with deadline  

---

### 8. Filter Tasks
As a student, I want to filter tasks by status or priority so that I can focus on specific tasks.
Description: The user filters tasks based on criteria.  
Inputs: filter criteria  
Outputs: filtered list of tasks  

---

### 9. Persistent Storage
As a student, I want my tasks saved permanently so that I don’t lose my data.
Description: Tasks are stored in a database.  
Inputs: task data  
Outputs: stored tasks  

---

### 10. Input Validation
As a student, I want the app to validate my input so that I avoid errors.  
Description: The system checks user input for correctness.  
Inputs: user input  
Outputs: validation messages or accepted input  

---

### 11. View Completed Tasks
As a student, I want to view completed tasks so that I can review my progress.
Description: The system shows completed tasks separately.  
Inputs: none  
Outputs: completed tasks list  

---

### 12. Dashboard Overview
As a student, I want to see a summary of my tasks so that I can quickly understand my workload.
Description: The system displays task statistics.  
Inputs: none  
Outputs: counts of total, completed, and pending tasks  

---
### 12. Analytics
As a student, I want to see a summary of my tasks so that I can quickly understand my workload.
Description: The system displays task statistics.  
Inputs: none  
Outputs: counts of total, completed, and pending tasks 

## Use cases
![ToDo_App_UseCase_Diagram](https://github.com/user-attachments/assets/e73cbe26-af08-450d-9b93-09f38290a0e7)

**Main Use Cases**

- Create Task (Student)  
- View Tasks (Student)  
- Edit Task (Student)  
- Delete Task (Student)  
- Mark Task as Complete (Student)  
- Filter Tasks (Student)  

**Actors**

- Student (main user)

---

## 🏛️ Architecture
<img width="651" height="331" alt="TodoApp_Architecture" src="https://github.com/user-attachments/assets/bcd5546e-ae06-487f-a8e6-cf908a8c2059" />

### Software Architecture

**Layers / components:**

- UI (NiceGUI browser interface)  
- Application logic (task management and validation)  
- Persistence (SQLite database with ORM)  

**Design decisions:**

- Use MVC (Model–View–Controller) pattern  
- Separate UI from business logic and database  
- Store tasks in a database instead of JSON  

---

## 🗄️ Database and ORM
<img width="201" height="134" alt="Task_ERD_ToDo" src="https://github.com/user-attachments/assets/e86b0acd-45e0-437b-8c80-7945e013bc4e" />

**Entities:**

Task:
- id (`int`)
- title (`str`)
- description (`str`)
- priority (`str`)
- due_date (`date`)
- completed (`bool`)


Student:
- id (`int`)
- department (`str`)

Priority:
- id (`int`)
- status (`str`)

---

## ✅ Project Requirements

### 1. Browser-based App (NiceGUI)

The application runs in the browser using NiceGUI. Users can create, view, update, and delete tasks interactively.

---

### 2. Data Validation

- Minimum title and description length  
- Valid priority values (Low, Medium, High)  
- Valid date format for due dates  

---
### 3. Data Validation
All relevant data is managed via an ORM(e.g. SQLModel or SQLAlchemy).