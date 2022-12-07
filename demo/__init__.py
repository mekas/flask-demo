from flask import Flask, render_template, request
import os
from pymongo import *
from db import *
from . import pond 

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile('settings.cfg', silent=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(pond.bp)   

    @app.get("/pond_activation")
    def pond_activation():
        return
        
    @app.get("/pond_activation/<id>")
    def pond_activation_by_id(id):
        return  

    
    '''
    Post object format:
    Pond = {
        'name' : <string>, 
        'location' : <string> 
        'material' : <string> 
        'shape' : <string> 
    }
    '''
    @app.post('/api/v1/register_pond')
    def register_pond(): 
        
        name = request.form['name']
        location = request.form['location']
        material = request.form['material']
        shape = request.form['shape']
        pond = {
            'name' : name,
            'location' : location, 
            'material' : material, 
            'shape' : shape
        }
        
        pond = request.form['pond']
        
        app.logger.debug("Pond name", name)
        
        client = MongoClient("localhost", 27017)
        db = client.fishdb
        db.pond.insert_one(pond)
        return True 
        
    return app
