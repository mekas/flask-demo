def get_row(cursor):
    cursor = ({'_id': cursor}, cursor)[isinstance(cursor,dict)]
    cursor = ([cursor], cursor)[isIterable(cursor) and not isinstance(cursor, dict)]
    print(cursor)
    getId = lambda x: {'_id': x['_id']._ObjectId__id.hex()}
    def row_transform(x): 
        
        return {**x, **getId(x)}

    # row_transform = lambda x : {**x, **getId(x)}
    rows = [row_transform(row) for row in cursor]
    return rows

def isIterable(obj):
    if hasattr(obj, '__iter__'):
        return True

    return False
