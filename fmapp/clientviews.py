from flask import Flask, render_template, send_from_directory
import flask
import json
from fmapp import app
from fmapp.models import *


@app.route('/home', methods=['GET', 'POST'])
def home():
    transactions_list = Transaction.query.all()
    transactions = json.dumps([x.json_dump() for x in transactions_list])
    categories_list = Category.query.all()
    categories = json.dumps([x.json_dump() for x in categories_list])
    return render_template('home.html', name="Shrey", transactions=json.loads(transactions),
                            categories=json.loads(categories))
