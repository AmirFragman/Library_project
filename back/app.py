import json
import flask
from flask import Flask, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date, timedelta
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SECRET_KEY'] = "SECRET_KEY_CODE"

script_path = os.path.realpath(__file__)
script_directory = os.path.dirname(script_path)
db_path = os.path.join(script_directory, 'library.db')

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///' + db_path
db = SQLAlchemy(app)
CORS(app)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

# <---------------------------------creating tables with classes-------------------------------------------------------------->

# Customers table - columns: id (PK), name, city, age, active
class Customers(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer: ('{self.id}', '{self.name}','{self.city}','{self.age}', {self.active})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "age": self.age,
            "active": self.active
        }
    
# Books table - columns: id(PK), name, author, year, book_type, active
class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default = True)

    def __init__(self, name, author, year, book_type):
        self.name = name
        self.author = author
        self.year = year
        self.book_type = book_type

    def __repr__(self):
        return f"Books('{self.id}', '{self.name}','{self.author}','{self.year}','{self.book_type}', {self.active})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year': self.year,
            'book_type': self.book_type,
            'active': self.active
        }
# Loans table - columns: id(PK), cust_id(FK), book_id(FK), loan_date, return_date, active. relationships: customer, book
class Loans(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key= True)
    cust_id = db.Column(db.Integer, db.ForeignKey(Customers.id))
    book_id = db.Column(db.Integer, db.ForeignKey(Books.id))
    loan_date = db.Column(db.String, nullable=False)
    return_date = db.Column(db.String)
   
    customer = db.relationship("Customers", backref="custLoans")
    book = db.relationship("Books", backref="bookLoans")

    def __init__(self, cust_id, book_id, loan_date):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loan_date = loan_date

    def __repr__(self):
        return f"Loans('{self.id}, {self.cust_id}, {self.book_id}', '{self.loan_date}','{self.return_date}')"  
    def to_dict(self):
        return {
            'id': self.id,
            'cust_id': self.cust_id,
            'book_id': self.book_id,
            'loan_date': self.loan_date,
            'return_date': self.return_date
        }
    
# <---------------------------------END of creating tables-------------------------------------------------------------->    

# <---------------------------------server routes and methods----------------------------------------------------------->   
# MY_SERVER = http://127.0.0.1:5000

# Homepage
@app.route("/", methods = ['GET'])
def homepage():
    return redirect("/index.html")

#Customers
#http://127.0.0.1:5000/customers 
@app.route('/customers', methods = ['GET'])
def get_all_customers():
    customers = Customers.query.filter_by(active=1).all()
    return flask.jsonify([customer.to_dict() for customer in customers])

#Customer addition
#http://127.0.0.1:5000/customers
@app.route('/customers', methods = ['POST'])
def new_customer():
    data = request.get_json()
    name= data["name"]
    city= data["city"]
    age= data["age"]

    if not name or not city or not age:
        return flask.jsonify({'error': 'Missing required fields'})

    newCustomer = Customers(name, city, age)
    db.session.add(newCustomer)
    db.session.commit()

    return flask.jsonify({'message': 'Customer created successfully'})

#Customer update
#http://127.0.0.1:5000/customers/<id>
@app.route('/customers/<id>', methods = ['POST'])
def update_customer(id):
    data = request.get_json()
    updated_row = Customers.query.filter_by(id=id).first()
    if updated_row:
        if len(data["name"])>0:
            updated_row.name= data["name"]
        if len(data["city"])>0:
            updated_row.city= data["city"]
        if len(data["age"]) > 0:
            updated_row.age= data["age"]
        updated_row.active= data["active"]
        db.session.commit()
        return f"Customer ID:{id}, Name: {updated_row.name} got updated"
    return "The customer does not exist"

#Customer deletion
#http://127.0.0.1:5000/customers/<id>
@app.route('/customers/<id>', methods = ['DELETE'])
def delete_customer(id):
    delete_row = Customers.query.filter_by(id=id).first()
    if delete_row:
        delete_row.active = False
        db.session.commit()
        return f"Customer ID number:{delete_row.id} got deleted"
    return "The customer does not exist"

#Books
#http://127.0.0.1:5000/books 
@app.route("/books", methods = ['GET'])
def show_books():
    books = Books.query.filter_by(active=1).all()
    return flask.jsonify([book.to_dict() for book in books])

#Book addition
#http://127.0.0.1:5000/books
@app.route('/books', methods = ['POST'])
def new_book():
    data = request.get_json()
    name= data["name"]
    author= data["author"]
    year= data["year"]
    book_type = data["book_type"]

    if not name or not author or not year or not book_type:
        return flask.jsonify({'error': 'Missing required fields'})

    newBook = Books(name = name, author = author, year = year, book_type = book_type)
    db.session.add(newBook)
    db.session.commit()

    return flask.jsonify({'message': 'Book created successfully'})

#Book update
#http://127.0.0.1:5000/books/<id>
@app.route('/books/<id>', methods = ['POST'])
def update_book(id):
    data = request.get_json()
    updated_row = Books.query.filter_by(id=id).first()
    if updated_row:
        if len(data["name"])>0:
            updated_row.name= data["name"]
        if len(data["author"])>0:
            updated_row.author= data["author"]
        if len(data["year"]) > 0:
            updated_row.year= data["year"]
        if len(data["book_type"]) > 0:
            updated_row.book_type= data["book_type"]
        updated_row.active= data["active"]
 
        db.session.commit()
        return f"Book ID:{id}, Name: {updated_row.name} got updated"
    return "The book does not exist"

#Book deletion
#http://127.0.0.1:5000/books/<id>
@app.route('/books/<id>', methods = ['DELETE'])
def delete_book(id):
    delete_row = Books.query.filter_by(id=id).first()
    if delete_row:
        delete_row.active = False
        db.session.commit()
        return f"Book ID:{id} got deleted"
    return "The book does not exist"

#Loans
#http://127.0.0.1:5000/loans 
@app.route("/loans", methods=['GET'])
def show_loans():
    loans = Loans.query.all()

    return flask.jsonify([loan.to_dict() for loan in loans])

#late loans
#http://127.0.0.1:5000/loans/late 
@app.route("/loans/late", methods=['GET'])
def show_late_loans():
    unreturned_loans = Loans.query.filter_by(return_date = None).all()
    late_loans = []

    for loan in unreturned_loans:
        book = Books.query.filter_by(id = loan.book_id).first()
        # loan.loan_date + book_type <today
        book_type = book.book_type
        if book_type == 1:
            return_date = datetime.strptime(loan.loan_date, '%Y-%m-%d') + timedelta(days=10)
        elif book_type == 2:
            return_date = datetime.strptime(loan.loan_date, '%Y-%m-%d') + timedelta(days=5)
        elif book_type == 3:
            return_date = datetime.strptime(loan.loan_date, '%Y-%m-%d') + timedelta(days=2)
        if return_date < datetime.today():
            late_loans.append(loan)

    return flask.jsonify([loan.to_dict() for loan in late_loans])

#http://127.0.0.1:5000/loans
# New loan
@app.route('/loans', methods = ['POST'])
def new_loan():
    data = request.get_json()
    cust_id = data["cust_id"]
    book_id = data["book_id"]



    cust_id = int(cust_id)
    book_id = int(book_id)

    loan_date = datetime.now().strftime('%Y-%m-%d')
    newLoan = Loans(cust_id=cust_id, book_id=book_id, loan_date=loan_date)

    db.session.add(newLoan)
    db.session.commit()
    return "New loan was added."

#Return book
#http://127.0.0.1:5000/loans/return/<id>
@app.route('/loans/return/<id>', methods = ['POST'])
def delete_loan(id):
    return_loan = Loans.query.filter_by(id=id).first()
    if return_loan:
        return_loan.return_date = datetime.today().strftime('%Y-%m-%d')
        db.session.commit()
        return f"Loan ID:{id} got returned"
    return "The loan does not exist"

# <---------------------------------END of server routes and methods-------------------------------------------------------------------> 

if __name__ == '__main__':
    app.run(debug=True)
