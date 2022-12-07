import click
import pymongo
from flask import current_app, g, request
from flask.cli import with_appcontext

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    db = dbclient[current_app.config['DATABASE']]
    return db

def get_collection(table_name):
    if 'db' not in g:
        g.db = get_db()
    return g.db[table_name]

"""
Helper function to query all user on system 
"""
def get_ponds(filter={}):
    collection = get_collection("pond")    
    return collection.find(filter)
    
def get_pond(filter={}):
    collection = get_collection("ponds")
    return collection.find_one(filter)
    
def insert_pond(data):
    collection = get_collection("ponds")
    row = collection.insert_one(data)
    return row

def close_db(e=None):
    db = g.pop(current_app.config['DATABASE'], None)
    
    if db is not None:
        db.close() 

def init_db():
    """clear the existing data and create new tables."""    
    db = get_db()    
    db.client.drop_database(current_app.config['DATABASE'])
    
@click.command('init-db')
def init_db_command():    
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

