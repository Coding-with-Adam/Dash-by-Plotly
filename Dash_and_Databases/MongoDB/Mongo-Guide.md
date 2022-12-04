See instruction below or download them here: 
https://drive.google.com/file/d/1Z94SArM9azTcykVdNxmPQPAXeLfNtjJJ/view?usp=sharing
# Install Mongo and Build Local Server

1.	Download Mongo according to your Operating System: [https://www.mongodb.com/try/download/community ](https://www.mongodb.com/try/download/community)
2.	Install Mongo on your computer
3.	Create a "data" folder and a "db" folder in your C drive
4.	Open a new Command Prompt and go to the folder where Mongo was installed - `cd C:\Program Files\MongoDB\Server\5.0\bin`
5.	Run the following command to start the MongoDB server: `mongod`
6.	Open a new Command Prompt and cd to the same folder as in step 4.
7.	Run the following command to open the mongo shell that will interact with the client: `mongo`
8.	Download and install `mongosh` on your computer because `mongodb` is deprecated. [https://www.mongodb.com/try/download/shell?jmp=docs](https://www.mongodb.com/try/download/shell?jmp=docs)
9.	Set up Environment Variable to run mongo from anywhere on your computer, by opening the “Edit the System Environment Variables” window. Then go to Advanced System Settings -> Environment Variables -> Path(Under System Variables) -> Edit -> New. Now add the path of your folder where Mongo is installed from step 4.
10.	Close all Command Prompts. Now open a new Command Prompt and type `mongod`. Then, open another Command Prompt and type `mongosh`.
* Once you restart your computer, you will not need to run a separate shell 
with mongod before running mongosh, because when we installed mongo we checked the box that said “Install mongoD as a service”. Just open a new Command Prompt and type `mongosh`.

# Build your Mongo Database (`test_mongo.py`)

1. Open PyCharm (or any Python IDE) and `pip install pymongo`
1. Use `test_mongo.py` as an example of connecting to server and creating a database
1. See new table that you just created by going back to `mongosh` shell and typing: 
    1. use DatabaseName
    1. `db.CollectionName.find()`
1. Better option is to build the database and table with the shell, and use the Python Dash code  to add, update, or delete data. To build the database go ahead and type: use DatabaseName
    1. Then, create a collection (table) by typing: `db.createCollection(“shelterA”)`
    1. Then, insert data into the collection:
        ```
        db.shelterA.insertOne(
            {
            "animal": "cat", 
            "breed": "shorthair"
            "age": 2
            "health": "good"
            "neutered": False
            }
        )
        ```
    1. Ensure data was entered by typing: `db.shelterA.find()`

**Sample Code:**
* Connect your Dash App to Local Mongo Server (`mongo_dash.py`)
* Connect Dash DataTable to Local Mongo Server (`mongo_dash_datatable.py`)

# For more articles, tutorials on the topic:

Download and Install Mongo: 
* [https://www.youtube.com/watch?v=FwMwO8pXfq0](https://www.youtube.com/watch?v=FwMwO8pXfq0)

Getting started with Mongo: 
1. [https://www.freecodecamp.org/news/learn-mongodb-a4ce205e7739/](https://www.freecodecamp.org/news/learn-mongodb-a4ce205e7739/)
1. [https://docs.mongodb.com/manual/reference/operator/](https://docs.mongodb.com/manual/reference/operator/)
1. [https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_pyMongo_tutorial_Range_Queries_Counting_Indexing.php](https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_pyMongo_tutorial_Range_Queries_Counting_Indexing.php)

Set up Mongo Server in the cloud:
* [https://www.guru99.com/mongodb-atlas-cloud.html](https://www.guru99.com/mongodb-atlas-cloud.html)
