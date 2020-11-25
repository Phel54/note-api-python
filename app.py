from flask import Flask,jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from datetime import datetime, time

app = Flask(__name__)
api = Api(app)

client= MongoClient("mongodb+srv://admin-isichei:adminisichei@cluster0-n4db7.mongodb.net")
db=client.notes
Notes = db["NotesPython"]

class CreateNote(Resource):
    def post(self):
        postedData = request.get_json()
        title = postedData["title"]
        note = postedData["note"]

        

        Notes.insert({
            "title":title,
            "note":note,
            "createdAt":datetime.now(),
            "updatedAt":datetime.now()
        })
        retJson = {
            "status":200,
            "message":"You successfully created a note"
        }

        return jsonify(retJson)
    

api.add_resource(CreateNote, "/notes")


@app.route('/')
def hello_world():
    return 'Hello, World!'




if __name__ == "__main__":
    app.run(debug=True)