from flask import Flask, render_template, send_from_directory
import flask
import json
from fmapp import app
from fmapp.models import *
from sqlalchemy import desc


@app.route('/home', methods=['GET', 'POST'])
def home():
    transactions_list = Transaction.query.order_by(desc(Transaction.date))
    transactions = json.dumps([x.json_dump() for x in transactions_list])
    categories_list = Category.query.all()
    categories = json.dumps([x.json_dump() for x in categories_list])

    return render_template('home.html', name="Shrey", transactions=json.loads(transactions),
                           categories=json.loads(categories))


@app.route('/bored', methods=['GET'])
def bored():
    transactions = Transaction.query.order_by(desc(Transaction.date))
    categories = Category.query.all()
    tags = json.dumps([x.json_dump() for x in Tag.query.all()])

    return render_template('bored.html', name="Bored", transactions=transactions,
                           categories=categories, tags=json.loads(tags))
