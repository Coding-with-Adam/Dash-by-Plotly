import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient

# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")

# Create database called animals
mydb = client["animals"]

# Create Collection (table) called shelterA
collection = mydb.shelterA

# Create the documents (rows)
record = {
    "animal": "cat",
    "breed": "shorthair",
    "age": 2,
    "health": "good",
    "neutered": "false"
}

# Insert documents (rows) into the database's collection (table)
collection.insert_one(record)

# View the documents
# testing = collection.find_one()
# print(testing)

# Convert the Collection (table) date to a pandas DataFrame
# df = pd.DataFrame(list(collection.find()))
# print(df)
# print("----------------------------")
# print(df.iloc[:, 1:])
