from flask_sqlalchemy import SQLAlchemy	
from sqlalchemy_utils import generic_relationship


from dotenv import load_dotenv

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


import datetime