from flask import Flask, render_template, send_from_directory
import flask
import json
from fmapp import app, db
from fmapp.models import *


@app.route('/home', methods=['GET', 'POST'])
def home():
    trans = Transaction.query.all()
    transactions = json.dumps([x.json_dump() for x in trans])
    return render_template('home.html', name="Shrey", transactions=json.loads(transactions))
