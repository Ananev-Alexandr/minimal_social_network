# 'Minimal social network'

Blog site where users can create posts and like them.

The user can register, log in and log out of the system. In addition, the creation of posts, obtaining information about the post of interest, editing your posts, liking the posts of other users, and, of course, deleting the created posts are also implemented.

The main interaction with the backend is to send queries to the database via SQLAlchemy. In this project, the database is PostgreSQL.

With the help of OpenAPI, automatic documentation occurs and it becomes possible to send requests through it.
Implemented security through tokens. OpenAPI introduces the ability to log in and out of the system, as well as restrictions on user actions

## Start-up tips

Python version **python3.10** is required for a stable program launch, operation on versions less than 3.10 is possible, but has not been tested

To install the dependencies, run the following command:

`pip install -r requirements.txt`

After installing the dependencies, you can run the project from the main.py file.

To send inquiries, use the address:
http://127.0.0.1:8000/docs#/
