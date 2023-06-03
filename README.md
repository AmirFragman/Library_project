# Library_project

This project is a Library Management Site

the site can be seen here: 
https://libraryamir.onrender.com/index.html

Git:
https://github.com/AmirFragman/Library_project 

Actions for using github:

1. git clone https://github.com/AmirFragman/Library_project.git

2. pip install -r requirements.txt

Create virtual enviroment:

1. pip install virtualenv > env
2. Create virtualenv in the directory you are in: 
   virtualenv  "env_name" (common used as venv)
3. Activate virtualenv: "env_name"\Scripts\activate

run the app:

1. python app.py
2. enter the local server host

A small guide:

On the top right of the top nav-bar you are able to choose which table to view (Customers, Books, Loans and Late loans)

On the left nav-bar you can do the following actions:
Go home

Add a customer (form) - add name, city, age - the id will be created by itself - check Customers table
Delete a customer (form) - add customer id to delete (active=False) the customer will not appear anymore in the table - check Customers table
Update a customer (form) - you can change any of the table Column - if an input is empty, it will not change the saved data. (see if you can restore my brother by changing Active=True with customer ID = 2)

Add a book (form) - add name, author, year published and book type - the id will be created by itself - check Books table
Delete a book (form) - add book id to delete (active=False) the book from its table
Update a book (form) - you can change any of the table Column - if an input is empty, it will not change the saved data.

Add a new loan (form) - add a customer ID and Book ID to create a loan - the loan ID will be created by itself
Return a book (form) - enter loan ID to make book active.


