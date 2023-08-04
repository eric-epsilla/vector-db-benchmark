#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example
# 1. docker run --pull=always -d -p 8888:8888 epsilla/vectordb
# 2. pip3 install --upgrade pyepsilla
# 3. python3 simple_example.py
#

from pyepsilla import vectordb
import random, string, time
import h5py


## Connect to Epsilla VectorDB
c = vectordb.Client(host='127.0.0.1', port='8888')
# c = vectordb.Client(host='3.209.6.179', port='8888', db_name='default')

## Check VectorDB Status
status_code, response = c.welcome()
status_code, response = c.state()

## Load DB with path
status_code, response= c.load_db(db_name="myDB", db_path="/tmp/epsilla")

## Set DB to current DB
c.use_db(db_name="myDB")


c.rebuild(db_name="myDB")

## Unload DB
# c.unload(db_name="myDB")


## Query Vectors
# query_field = "Embedding"
# query_vector = Embedding[-1]
# print(Docs[-1], query_vector)
# response_fields = ["Doc"]
# limit = 2
# status_code, response = c.query(table_name="MyTable", query_field=query_field, query_vector=query_vector, response_fields=response_fields, limit=limit)
# print("status_code", status_code, "response", response)



## gist-960-euclidean.hdf5
import h5py
f = h5py.File('gist-960-euclidean.hdf5', 'r')
print(list(f.keys()))
training_data = f["train"]
size = training_data.size
records_num, dimensions = training_data.shape

## create table
id_field = {"name": "id", "dataType": "INT"}
vec_field = {"name": "vector", "dataType": "VECTOR_FLOAT", "dimensions": dimensions}
fields = [id_field, vec_field]
status_code, response = c.create_table(table_name="gist_960_euclidean", table_fields=fields)

## insert data into table
## a_tolist = a.tolist()
# records_data = [ {"id": i, "vector": training_data[i].tolist()} for i in range(100000)]
# records_data = [ {"id": i, "vector": training_data[i].tolist()} for i in range(records_num)]
# status_code, response = c.insert(table_name="gist_960_euclidean", records=records_data)


indexs = [ i for i in range(0, records_num+10000, 10000)]

for i in range(len(indexs)-1):
    print(indexs[i], indexs[i+1])
    records_data = [{"id": i, "vector": training_data[i].tolist()} for i in range(indexs[i], indexs[i+1])]
    c.insert(table_name="gist_960_euclidean", records=records_data)
    time.sleep(2)

## Drop table
#status_code, response = c.drop_table("MyTable")

## Drop db
#status_code, response = c.drop_db("myDB")