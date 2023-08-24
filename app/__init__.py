from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__, template_folder='../templates')
app.secret_key = 'secret'
CORS(app)  # This will enable CORS for your entire app


from . import routes
