import sqlite3
import io
import numpy as np
import json
import pickle
from itertools import chain
#from azure.storage.blob import BlobPermissions

dbconnect = sqlite3.connect("projectdb.db");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();
#print(np.__version__)
def createdatabase():
    #creating database with table name database
    
    try:
        cursor.execute("CREATE TABLE courtdb(court INT PRIMARY KEY, points TEXT)");
        #cursor.execute("CREATE TABLE courtdatabase(court INT PRIMARY KEY, points BLOB)");
    except Exception as E:
        print('Error: ', E) 
    else:
        print('Table database has been created')
        
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
    

def convert_array(text):
    out = io.BytesIO(text)

    out.seek(0)
    #return np.load(out, mmap_mode = None,allow_pickle = True, fix_imports = True, encoding = 'bytes')
    return np.load(out)

#
def update():
    #output = ' '
    #createdatabase()
    arrpt = [(428, 378), (139, 267), (464, 204), (559, 213)]
    #pickle.dump(arrpt, output) #print(bytes(chain.from_iterable(tuples)))
    cursor.execute('''UPDATE courtdata SET (pointsx,pointsy) values (?,?) WHERE court= 1''',bytes([arrpt]))
    dbconnect.commit()
    
#sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
#sqlite3.register_converter("array", convert_array)
 
#if __name__=="__main__":
#    createdatabase()

#     cursor.execute("SELECT * from courtdb")
#     record = cursor.fetchall()
#     for row in record:
#         courtid = row[0]
#         courtarray = row[1].decode()
#         print("ca",courtarray)     
#     
# #    createdatabase()
#     try:
#         newa = [json.dumps(arrpt)]
#         #print(type(newa))
#         cursor.execute('''UPDATE courtdb SET points = ? WHERE court=1''',adapt_array(arrpt))             
#         dbconnect.commit()
#         #print(adapt_array(arrpt))
       
#             #allow_pickle=True
#             #ca = row[1]
#             #courtarray = json.loads(row[1])
#             courtarray = convert_array(row[1])
#             print("row1", row[1])
             
#     except:
#         print("nope")
# #     #n= [34,56]
# #     #print(type(n))
# #     #cursor.execute("INSERT INTO database (court,x1,y1,x2,y2,x3,y3,x4,y4) VALUES (?,?,?,?,?,?,?,?,?)", (1,(arrpt[0][0]),(arrpt[0][1]),(arrpt[1][0]),(arrpt[1][1]),(arrpt[2][0]),(arrpt[2][1]),(arrpt[3][0]),(arrpt[3][1])))
# #     #dbconnect.commit()
# # #     print("l")
# # #     cursor.execute("SELECT * from database")
# # #     record = cursor.fetchall()
# #     for row in record:
# #         print(row[0],row[1],row[2])
# #     cursor.close()