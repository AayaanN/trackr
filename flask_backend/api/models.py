from . import db
from datetime import datetime
from sqlalchemy.sql import func
from pytz import timezone

timezone('EST').localize(datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S')

class Stock(db.Model):
    __tablename__ = 'Stock_Info'
    id = db.Column(db.Integer, primary_key = True)
    # time = db.Column(db.TIMESTAMP(timezone = True), default = datetime.now(timezone('EST')))
    time = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone('EST')))
    name = db.Column(db.String(16))
    price = db.Column(db.Float)
    prev_price = db.Column(db.Float)
    change = db.Column(db.Float)
    percent_change = db.Column(db.Float)
    amount = db.Column(db.Float)
    price_bought_at = db.Column(db.Float)
    average_price = db.Column(db.Float)
    value = db.Column(db.Float)

class Portfolio_Log(db.Model):
    __tablename__ = 'Portfolio_Logs'
    id = db.Column(db.Integer, primary_key = True)
    # time = db.Column(db.TIMESTAMP(timezone = True), default = datetime.now(timezone('EST')))
    time = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone('EST')))
    value = db.Column(db.Float)
    initial_value = db.Column(db.Float)
    change = db.Column(db.Float)
    percent_change = db.Column(db.Float)





