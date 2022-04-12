#@author Chhavi Sujeebun updated
#importing required libraries 
import sqlite3
import io
import numpy as np
import json
import pickle
from itertools import chain

#creating a cursor to the the database courtdb
dbconnect = sqlite3.connect("projectdb.db");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();

#createdatabase creates a table courtdb with 2 columns court and points
#court is a primary key and stores the court id
#points stores the reference points selected for each court
def createdatabase():
    #creating database with table name database
    
    try:
        cursor.execute("CREATE TABLE courtdb(court INT PRIMARY KEY, points TEXT)");
        
    except Exception as E:
        print('Error: ', E) 
    else:
        print('Table database has been created')

#param arr is the array of reference points selected'
#allows MySQL database to store array as BLOB
def adapt_array(arr):
    #"""
    #http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    #"""
    #print(type(arr))
    out = io.BytesIO()
    np.save(out, arr)
            
    out.seek(0)
    #print(type(out.read()))
    return sqlite3.Binary(out.read())
    #string = ' '.join([str(item) for item in arr])
    #return ([json.dumps(arr)])
    
#@param text is the data read from the datbase
#converts the data read from MySQL back to an array
def convert_array(text):
    out = io.BytesIO(text)

    out.seek(0)
    #return np.load(out, mmap_mode = None,allow_pickle = True, fix_imports = True, encoding = 'bytes')
    return np.load(out)


