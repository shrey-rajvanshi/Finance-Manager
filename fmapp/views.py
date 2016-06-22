from flask import Flask
import flask
import json
from fmapp import app, db
from fmapp.models import *

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


# UI URLs
