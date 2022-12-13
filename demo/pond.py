import functools
import logging
import os
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, Markup, send_from_directory
)

from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from . import db
from bson.objectid import ObjectId
from copy import deepcopy
import numpy as np
from .util import *

bp = Blueprint('pond', __name__, url_prefix='/')
'''
    This get operation will return the following:
    _id, name, location, shape, material, length, width, diameter, height, is_active 
    '''


@bp.get("/pond")
def pond():
    mgcursor = db.get_ponds({})
    data = get_row(mgcursor)
    return data


@bp.get("/pond/<id>")
def pond_id(id):
    filter = {"_id": id}
    data = db.get_pond(filter)
    return get_row(data)


""" def getId(x):
    d = {'_id': x['_id']._ObjectId__id.hex()}
    return d


def row_transform(x):
    d = {**x, **mergeDict(deepcopy(x))}
    return d """


'''
request object will send 
name, location, shape, material, length, width, diameter, height
'''


@bp.post("/pond/insert")
def pond_insertion():
    name = request.form['name']
    shape = request.form['shape']
    material = request.form['material']
    length = ("", request.form.get('length'))[request.form.get('length') is not None] 
    width = ("", request.form.get('width'))[request.form.get('width') is not None] 

    build_time = datetime.now()

    data = {
        'name': name,
        'shape': shape,
        'material': material,
        'length': length,
        'width': width,
        #'build_time': build_time,
        'isActive': 'False'
    }
    row = db.insert_pond(data)
    return get_row(row)
