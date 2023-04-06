# library
Features
1.	User registration: Users can register by providing their username, email, and password.
2.	User login: Registered users can log in using their username and password.
3.	Password hashing: Passwords are hashed and salted (so if two or more users have same password they will have different scripted password in the database) using Flask-Bcrypt, making them secure and preventing unauthorized access.
4.	User authentication: Authenticated users are allowed to access their dashboard and view their favorite books.
5.	User dashboard: Authenticated users can view their dashboard, where they can view a list of books and mark books as favorites.
6.	Book search: Users can search for books by title or author.
7.	Book details: Users can view details of a book, including its title, author, description, and cover image.
8.	Book favorites: Users can mark books as favorites and remove them from their favorites list.
9.	Admin panel: only admin can access the admin panel, where they can add new users, new admins and view existing users.
10.	Logging: The app logs user activities, such as login/logout attempts, also if some user try to access admin panel illegally , to a log file using Python's logging module.
11.	Model-view-controller (MVC) architecture: The app follows the MVC pattern, separating the application logic into models, views, and controllers.
12.	Form validation: The app uses Flask-WTF to validate user input in registration and login forms.
13.	SQL database: The app uses SQLite database to store user information and book details.
14.	Flask-Admin: The app uses Flask-Admin to provide a user interface for managing the database.

Use technology
•	Flask: a Python web framework for building web applications
•	SQLAlchemy: an Object Relational Mapper (ORM) for communicating with databases in Python
•	Flask-Login: a Flask extension that provides user session management, authentication, and authorization
•	Flask-WTF: a Flask extension that provides integration with the WTForms library for building HTML forms in Python
•	Flask-Bcrypt: a Flask extension that provides password hashing and verification functionality
•	Flask-Admin: a Flask extension that provides an admin panel for managing the app's models and data
•	SQLite: a relational database management system used for storing data in the app's database
•	Python logging module: a built-in Python library for logging messages from the app, which is being used in the code to log user login attempts and other events
•	Jinja2/HTML/CSS: for the frontend part and design 


