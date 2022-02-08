import sqlite3
import io
import numpy as np
dbconnect = sqlite3.connect("projectdb.db");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();

def createdatabase():
    #creating database with table name database
    
    try:
        #cursor.execute("CREATE TABLE courtdb(court INT PRIMARY KEY, points TEXT)");
        cursor.execute("CREATE TABLE courtdatabase(court INT PRIMARY KEY, points array)");
    except Exception as E:
        print('Error: ', E) 
    else:
        print('Table database has been created')
        
def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

#if __name__ == "__main__":
#    createdatabase()
    #arrpt = [(428, 378), (139, 267), (464, 204), (559, 213)]
    #n= [34,56]
    #print(type(n))
    #cursor.execute("INSERT INTO database (court,x1,y1,x2,y2,x3,y3,x4,y4) VALUES (?,?,?,?,?,?,?,?,?)", (1,(arrpt[0][0]),(arrpt[0][1]),(arrpt[1][0]),(arrpt[1][1]),(arrpt[2][0]),(arrpt[2][1]),(arrpt[3][0]),(arrpt[3][1])))
    #dbconnect.commit()
#     print("l")
#     cursor.execute("SELECT * from database")
#     record = cursor.fetchall()
#     for row in record:
#         print(row[0],row[1],row[2])
#     cursor.close()