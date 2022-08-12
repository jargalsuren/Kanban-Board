# Kanban Board

This is a simple Kanban Board that can help you create new task, move the status of the task (e.g. To do, Doing, Done), and Deleting the task you have created. You will be able to monitor the tasks you have created by signing up in the home page and login to your unique account.

# Features

### Sign up and Log in

In the Kanban Board application, you are able to sign up by filling out your username, email, and password. You will use this information to (username and password) to login to you Kanban account. After you log in, you will be able to access the Kanban Board features. For authorization, email and username should be unique value. 
1. Username is limited to 4 to 15 characters
2. Password is limited to 4 to 50 characters
3. Email is limited to 50 characters. 
You will be able to Log out of the Kanban application by using Logout button placed in the navigation bar.

### Kanban Board

You will be able to create a task with its status in the /add_task page. All the changes you have made will be shown in your dashboard, so you are able to monitor your tasks with its status. From the Dashboard, you are able to create a new task, without needing to go back to a task creation page. The "Create a new task" and "Your tasks" navigation is interrelated, so that you will be easily find the pages you need to. 

### Testing

Testings are provided for the task creation, tasks status update, task deletion, and successful connection to each page loading.


### Installation:
To run the Kanban Board, you will simply run this snippet of code. 

#### macOS
```python3
python3.6 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3.6 app.py
```

### Structure of the Folder

1. ENV folder
    - Virtual environment folder
2. Kanban
    1. Static
        It contains the CSS file: kanban.css & login.css. Login.css is applied to both login and sign up page. Kanban.css is applied to create new task and Kanban Board pages after the user has logged in.
    2. Templates
        - dashboard.html: It contains html file for the Kanban Board with all the tasks user have created and their statuses. It also includes navigation bar and Welcome Back texts.
        - kanban.html: It is an html file for a page where you are able to create a task and select its status.
        - login.html: HTML file for the login page.
        - signup.html: HTML file for the sign up page.
    3. kanban.db: Kanban database
    4. Kanban.py: The main kanban board Flask application.
        The Python file contains database connection of the app,database setup, login and sign up form and setup, setup for each of the 4 pages I have designed: login, signup, dashboard, add_task. The file also contains codes for the task statuses and how they are updated and deleted.
3. Tests
    It contains test_kanban.py for the unit testing file for the Kanban Board application
4. README.md
    You are reading it now. :)
5. Requirements.txt
    This txt file contains all the current packages list in the environment and their versions used.

