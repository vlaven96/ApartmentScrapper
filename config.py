import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Salitos_28@localhost:5432/apartmentsDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False