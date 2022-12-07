import functools
import logging
import os
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, Markup, send_from_directory
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from db import *
from bson.objectid import ObjectId
from copy import deepcopy
import numpy as np

bp = Blueprint('pond', __name__, url_prefix='/')
'''
    This get operation will return the following:
    _id, name, location, shape, material, length, width, diameter, height, is_active 
    '''


@bp.get("/pond")
def pond():
    mgcursor = get_ponds({})
    # row_transform = lambda id, x : x, int.from_bytes(id._ObjectId__id,'little')
    def getId(x): return {'_id': x['_id']._ObjectId__id.hex()}
    def row_transform(x): return {**x, **getId(x)}
    data = [extract_row(d) for d in mgcursor]
    current_app.logger.debug(data)
    return data


""" def getId(x):
    d = {'_id': x['_id']._ObjectId__id.hex()}
    return d


def row_transform(x):
    d = {**x, **mergeDict(deepcopy(x))}
    return d """


def extract_row(row):
    id = row['_id']
    id_str = id._ObjectId__id.hex()
    id_byte = id._ObjectId__id
    id_int = int.from_bytes(id._ObjectId__id, 'little')
    bt = str(id_int).encode()
    row['_id'] = id_int
    return row


@bp.get("/pond/<id>")
def pond_id(id):
    filter = {"_id": id}
    data = get_pond(filter)
    return data


'''
request object will send 
name, location, shape, material, length, width, diameter, height
'''


@bp.post("/pond")
def pond_insertion():
    name = request.form['name']
    shape = request.form['shape']
    material = request.form['material']
    length = request.form['length']
    width = request.form['width']
    from datetime import datetime
    build_time = datetime.now()
    isActive = False
    data = {
        'name': name,
        'shape': shape,
        'material': material,
        'length': length,
        'width': width,
        'build_time': build_time,
        'isActive': False
    }
    row = insert_pond(data)
    if (row > 0):
        return True
    return False
