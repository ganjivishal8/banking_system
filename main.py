from flask import Flask, request, url_for, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rkthxgajmiaada:057d1ae5ca7404b4e70a8ee95e746a83266f031145cc0579c93c36a1166db10e@ec2-3-231-69-204.compute-1.amazonaws.com:5432/d90kt797to37s0'
db = SQLAlchemy(app)
app.secret_key = 'dont'


# table transactions
class Transactions(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    send_name = db.Column(db.String(80), nullable=False)
    receive_name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(80))


# table customers for storing users
class Customers(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Integer, nullable=False)


@app.route('/')
def hello_world():
    return render_template("home.html")


# for viewing all customers
@app.route('/user/', methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        result = Customers.query.all()
        print(result)
        return render_template('user.html', result=result)


# to transfer amount to another customer
@app.route('/transactions/', methods=['GET', 'POST'])
def transactions():
    trans = Customers.query.all()
    if request.method == 'POST':
        sender = request.form.get('sname')
        receiver = request.form.get('rname')
        amount = request.form.get('balance')
        entry = Transactions(send_name=sender, receive_name=receiver, amount=amount, date=datetime.now())
        if receiver != sender:
            edited = db.session.query(Customers).filter_by(email=receiver).one()
            edited.balance += int(amount)
            edited3 = db.session.query(Customers).filter_by(email=sender).one()

            # if balance is greater than amount to be transferred only then transaction occurs
            if edited3.balance >= int(amount):
                edited3.balance -= int(amount)
                db.session.add(entry)
                db.session.commit()
                result = Transactions.query.all()
                print(result)
                return render_template('transhist.html', result=result)
    return render_template('transactions.html', trans=trans)


@app.route('/adduser/', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        cname = request.form.get('name')
        cemail = request.form.get('email')
        cbalance = request.form.get('balance')
        entry = Customers( name=cname, email=cemail, balance=cbalance)
        if(cname!= "" or cemail!= "" or cbalance!=""):
            db.session.add(entry)
            db.session.commit()
            res = Customers.query.all()
            return render_template('user.html', result=res)
    return render_template('adduser.html')


@app.route('/transhist/', methods=['GET', 'POST'])
def mers():
    if request.method == 'GET':
        result = Transactions.query.all()
        print(result)
        return render_template('transhist.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
