#!/usr/bin/env python3

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from datetime import datetime
from  sqlalchemy import Table, Column, Integer, String, DateTime, BigInteger

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    number = Column(String(18))
    name = Column(String(36))
    
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

db_credentials = {
    "drivername": "postgres",
    "host": "localhost",
    "port": "5432",
    "username": "kevinmccartney",
    "password": "",
    "database": "testdb"
}

engine = create_engine(URL(**db_credentials))

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

choice = ''

while choice !='n':
    choice = input("Do you want to add a new user to the NYT word of the day subscription?[Y/n]").lower()
    if choice == 'n':
        pass
    elif choice != "y":
        print("Please enter y/n.")
    else: 
        new_user = User()

        print("Please enter the name & phone number of the new user.")

        new_user.name = input("Name: ")
        new_user.number = input("Number: ")
        session.add(new_user)

session.commit()

from prettytable import PrettyTable

table = PrettyTable()

table.add_row(["User ID", "Name", "Number"])

for instance in session.query(User):
    table.add_row([instance.id, instance.name, instance.number])

print(table)
