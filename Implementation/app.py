from flask import Flask, request, render_template, redirect, url_for
from flask_pymongo import PyMongo
import os
import logging
import secrets


from Model.DatabaseClient import DatabaseClient
from Controller.routes import SessionController
#from flask_cors import CORS, cross_origin

app = Flask(__name__)# static_path='/static')
logging.basicConfig(level=logging.DEBUG)
app.config['SECRET_KEY'] = secrets.token_hex(16)
#cors = CORS(app, resources={r"/foo": {"origins": "http://0.0.0.0:port"}})


def home(): 
	return render_template('home.html')

app.add_url_rule('/', view_func=home)
app.add_url_rule('/home', view_func=home)


sessionController = SessionController.SessionController()
app.add_url_rule('/register', view_func=sessionController.register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=sessionController.login, methods=['GET', 'POST'])
app.add_url_rule('/profile/<user_id>', view_func=sessionController.profile, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=sessionController.logout, methods=['GET', 'POST'])

'''
TODO:
logging framework 
modularity
error handling 

in SessionController
 -> validate the field values ?(password and dates)
 -> medical history should be a json 
 -> check if more fields need to be added

PatientController
 -> patient dashboard 
 -> patient book appointment 

DoctorController
 -> list patients for a day 

AppointmentCOntroller
'''




if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=90, debug=True) 
