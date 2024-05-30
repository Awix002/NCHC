!! please follow these steps to successfully run this project in your Windows Device !!

# Getting Started for Windows
# Make Sure all these are installed in your window device
- Download Python ( https://www.python.org/downloads/ )
- Download Node.js ( https://nodejs.org/en/download )
- Download PostgreSQL ( https://www.postgresql.org/download/ )
- Download Visual Studio Code ( https://code.visualstudio.com/download )
- Download 7Zip ( https://www.7-zip.org/download.html )

# Setting Up Project
- Download the Project File and Extract it using 7Zip.
- Make sure the main folder is "NCHC" and sub folders are "backend" and "frontend".
- Do not rename any other existing folder except main folder to "NCHC" if needed.

# Setting Up Database: PostgreSQL
- Open pgAdmin (PostgreSQL)
- set up your database by entering credentials.
- Create new database named "nchc_db"

# Installing Virtual Environment
- Open Command Prompt as administrator
- After installing python, type: "pip install virtualenv" in the command prompt

# Opening Project in Visual Studio Code
- Open Visual Studio
- Go to the Top-Left of Visual Code and click on "File"
- Dropdown will appear and click on Open Folder
- New window will pop up and select the project folder "NCHC"
- The project will open through Visual studio Code

# Setting Up Virtual Environment
Opening new Terminals for frontend and backend:
- In the VS Code, click on "Terminal" in the same bar as "File".
- Dropdown will apear and click on New Terminal.

To create new virtual Environment:
- Now type: "virtualenv venv" in the terminal to create new virtual environment named "venv".
- You can see that new venv is added below the backend and frontend folder.

# Setting up Backend
Changing Directories to backend and downloading the required packages
- Type: "venv\Scripts\activate" to activate the virtual environment for backend.
- Type: "cd backend" in the termical to change directory to backend.
- Type: "pip install -r requirements.txt" to install all the packages listed in the requirements.txt file.

Connecting Database:
Code of Database in Settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nchc_db',
        'USER': 'postgres',
        'PASSWORD': 'abiral',
        'HOST': 'localhost'
    }
}
- Make changes in the above code for the database in the settings.py file by changing the user and password according to your configured postgres credentials.

To Make Migration:
- Type: "python manage.py makemigrations"

To Migrate to database:
- Type: "python manage.py migrate"

To Run backend server:
- Type: "python manage.py runserver"


Extra: Creating Super User/Admin:
- Type: "python manage.py createsuperuser" and fill all the required sections to create superuser


# Setting up Frontend
Changing Directories to frontend and downloading the required packages:
- As previously explained, open new terminal.
- Type: "venv\Scripts\activate" to activate the virtual environment for frontend.
- In the new terminal, Type: "cd frontend" in the new terminal to change directory to frontend.
- Type: "npm install" to install all the dependencies(packages) listed in the package.json file of the frontend.

Note: if there are error installing the packages, type: "npm install --force" to force and re-install all packages

- After successfully installing all the packages, type: "npm start" to run the frontend server.









