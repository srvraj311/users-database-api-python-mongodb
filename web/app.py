"""
Registration of users
Each users get tokens
store a sentence on out database for 1 tokens
retrieve his stored sentence ou out database for 1 token

password hashing and storage

"""
from flask import Flask , jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

# Creating a new Flask class
app = Flask(__name__)

#Creating a neww api class
api = Api(app)

# Creating a new database Class
client = MongoClient("mongodb://db:27017")

# url should have same name as in docker and port is 27017
db = client.SentencesDatabase
users = db["Users"]


class Resgister(Resource):
	def post(self):
		# Get posted data by the user
		posted_data = request.get_json()

		# get the data
		username = posted_data["Username"]
		password = posted_data["Password"]

		# hashing hash(password + salt) = husgdfgsvsugfusdfnvsduv
		hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

		# store username and password into the database
		users.insert_one({
			"Username":username,
			"Password":hashed,
			"Sentence":"",
			"Tokens":6
		})

		#return the user a Message
		retJson = {
			"status":200,
			"Message":"Succesfully Signed up"
		}
		return jsonify(retJson)

# Function to mach password - used in Stored Class
def verifyPw(username, password):
	try:
		hashed_pw = users.find({
			"Username":username
		})[0]["Password"]
		if bcrypt.hashpw(password.encode("utf-8"),hashed_pw) == hashed_pw:
			return True
		else:
			return False
	except:
		return False

# function to return the no of tokens , Stored Class
def countTokens(username):
	tokens = users.find({
		"Username":username
	})[0]["Tokens"]
	return tokens


class Store(Resource):
	def post(self):
		# Step1 get the posted data
		posted_data = request.get_json()

		username = posted_data["Username"]
		password = posted_data["Password"]
		sentence = posted_data["Sentence"]

		# verify username and Password
		correct_pw = verifyPw(username, password)
		if not correct_pw :
			retJson = {
				"Status Code":302,
				"Message":"Invalid Credentials"
			}
			return jsonify(retJson)
		# verify tokens
		num_tokens = countTokens(username)
		if num_tokens <= 0:
			retJson = {
				"Status Code":301,
				"Message":"Out of tokens"
			}
			return jsonify(retJson)
		# make user Pay


		# store the sentence, take a token away and return status:200
		users.update_one({
			"Username":username,
		}, {
			"$set":{
				"Sentence":str(sentence),
				"Tokens":num_tokens-1
			}
		})

		retJson = {
			"Status Code":200,
			"Message":"Sentence Saved Succesfully"
		}
		return jsonify(retJson)


class Get(Resource):
	def post(self):
		posted_data = request.get_json()
		username = posted_data["Username"]
		password = posted_data["Password"]

		# match Password
		correct_pw = verifyPw(username, password)
		if not correct_pw :
			retJson = {
				"Status Code":302,
				"Message":"Invalid Credentials"
			}
			return jsonify(retJson)


		num_tokens = countTokens(username)
		if num_tokens <= 0:
			retJson = {
				"Status Code":301,
				"Message":"Out of tokens"
			}
			return jsonify(retJson)
		users.update_one({
		"Username":username
		}, {
			"$set":{
				"Tokens":num_tokens - 1
			}
		})

		sentence = users.find({"Username":username})[0]["Sentence"]

		retjson = {
			"Status Code":200,
			"Sentence":sentence
		}
		return jsonify(retjson)

api.add_resource(Resgister, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")

if __name__ == "__main__":
	app.run(host="0.0.0.0")
