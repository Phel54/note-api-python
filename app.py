from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from datetime import datetime
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient(
    "mongodb+srv://admin-isichei:adminisichei@cluster0-n4db7.mongodb.net")
db = client.notes
Notes = db["NotesPython"]
Users = db["UserPython"]

def UserExist(username):
    if Users.find({"username": username}).count() == 0:
        return False
    else:
        return True
class CreateNote(Resource):
    def post(self):
        postedData = request.get_json()
        title = postedData["title"]
        note = postedData["note"]

        Notes.insert({
            "title": title,
            "note": note,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()
        })
        retJson = {
            "status": 200,
            "message": "You successfully created a note"
        }

        return jsonify(retJson)


api.add_resource(CreateNote, "/notes")


class RegisterUser (Resource):
    def post(self):


        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        
        

        if UserExist(username):
            retJson = {
                "status":"301",
                "message":"User Exist in DB"
            }
            return jsonify(retJson)
        hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt())

        Users.insert({
            "username": username,
            "password": hashed_pass,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()

        })
        retJson = {
            "status": 200,
            "messages": "You successfully signed up for the API"
        }
        return jsonify(retJson)


api.add_resource(RegisterUser, "/Register")

def verifyPassword(username, password):
    if not  UserExist(username):
        return False
    hashed_pw = Users.find_one({"Username":username})["Password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        False





@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True)
