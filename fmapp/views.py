from flask import Flask, request, redirect, url_for, render_template
from flask_login import login_required, login_user, current_user, logout_user
import flask
import json
from fmapp import app, db
from fmapp.models import *
from fmapp.forms import *


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Looking for %s ?' % path


@app.route('/shrey', methods=['GET', 'POST'])
def hello_shrey():
    return 'Hello, This is Shrey route!'

#Wallet URLs

@app.route('/wallets', methods=['GET'])
def get_wallets():
    wallets = Wallet.query.all()
    return json.dumps([x.json_dump() for x in wallets])


@app.route('/add/wallets/<name>', methods=['GET'])
def add_empty_wallet(name):
    wallet = Wallet()
    wallet.name = name
    wallet.balance = 0
    db.session.add(wallet)
    db.session.commit()
    return json.dumps(wallet.json_dump())


@app.route('/add/wallets/<name>/<int:balance>', methods=['GET'])
def add_wallet(name, balance):
    wallet = Wallet()
    wallet.name = name
    wallet.balance = balance
    db.session.add(wallet)
    db.session.commit()
    return json.dumps(wallet.json_dump())


@app.route('/getbalance/<wallet>/', methods=['GET'])
def getbalance(wallet):
    wallet = Wallet.query.filter(Wallet.name == wallet).first()
    return str(wallet.balance)


#Transaction URLs


@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return json.dumps([x.json_dump() for x in transactions])


@app.route('/add/<name>/<int:amount>/<int:wallet_id>/<int:category_id>', methods=['GET'])
def deposit(name, amount, wallet_id, category_id):
    transaction = Transaction(name, amount, wallet_id, category_id)
    wallet = Wallet.query.get(wallet_id)
    wallet.balance += int(amount)
    db.session.add(wallet)
    db.session.add(transaction)
    db.session.commit()
    return "Created"


@app.route('/sub/<name>/<int:amount>/<int:wallet_id>/<int:category_id>', methods=['post'])
def withdraw(name, amount, wallet_id, category_id):
    transaction = Transaction(name, amount, wallet_id, category_id)
    wallet = Wallet.query.get(wallet_id)
    wallet.balance -= int(amount)
    db.session.add(wallet)
    db.session.add(transaction)
    db.session.commit()


def getCategory(name):
    rule = CRule.query.filter(CRule.transaction_name == name).first()
    if not rule:
        category_id = Category.query.filter(Category.name == "Uncategorized").first().id   # or directly use 1
    else:
        category_id = rule.category_id

    return category_id


@login_required
@app.route('/sub', methods=['post'])
def withdraw_client():
    name = request.form.get('name')
    amount = request.form.get('amount')
    wallet_id = request.form.get('wallet_id', 1)
    category_id = getCategory(name)
    transaction = Transaction(name, amount, wallet_id, category_id)
    wallet = Wallet.query.get(wallet_id)
    wallet.balance -= int(amount)
    db.session.add(wallet)
    db.session.add(transaction)
    db.session.commit()

    return "Transaction recorded"


@app.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated():
        return "You are already logged in"
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            user, authenticated = User.authenticate(form.username.data, form.password.data)
            if user:
                if authenticated:
                    login_user(user, remember=form.remember_me.data)
                    return redirect(url_for('home'))
                else:
                    error += "User Not authenticated"
            else:
                return "No user found with this name"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    logout_user()
    return "Successfully logged out"
