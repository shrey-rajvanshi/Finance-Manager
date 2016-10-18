from fmapp import db
from datetime import datetime


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    balance = db.Column(db.Integer)

    def __init__(self, name="No name given", balance=0):
        self.name = name
        self.balance = balance

    def json_dump(self):
        return dict(name=self.name, amount=self.balance)


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id'))
                )


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))
    date = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('transactions', lazy='dynamic'))

    def __init__(self, name="", amount=0, wallet_id=1, category_id=1):
        self.name = name
        self.amount = amount
        self.wallet_id = wallet_id
        self.category_id = category_id

    def __repr__(self):
        return str(self.amount) + ": "+self.name

    def json_dump(self):
        return dict(name=self.name, amount=self.amount, category=self.category_id, date=self.date.strftime('%d-%m-%Y'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return self.name

    def json_dump(self):
        return dict(id=self.id, name=self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return self.name

    def json_dump(self):
        return dict(id=self.id, name=self.name)
