from . import db
from datetime import datetime
from sqlalchemy.sql import func
from pytz import timezone

timezone('EST').localize(datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S %Z%z')

class Stock(db.Model):
    __tablename__ = 'Stock_Info'
    id = db.Column(db.Integer, primary_key = True)
    # time = db.Column(db.TIMESTAMP(timezone = True), default = datetime.now(timezone('EST')))
    time = db.Column(db.TIMESTAMP(timezone = True), default=lambda: datetime.now(timezone('EST')))
    name = db.Column(db.String(16))
    price = db.Column(db.Integer)