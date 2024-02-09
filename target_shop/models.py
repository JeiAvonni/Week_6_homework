# Password hash for extra security
from werkzeug.security import generate_password_hash
# ORM (Object Relational Mapper)
from flask_sqlalchemy import SQLAlchemy 
# Loading current_user
from flask_login import UserMixin, LoginManager 
# Data timestamp
from datetime import datetime 
# Unique id for data
import uuid 

from flask_marshmallow import Marshmallow


#Instantiate all our classes

# Make database object
db = SQLAlchemy() 
# Makes login object 
login_manager = LoginManager()

ma = Marshmallow() # makes marshmallow object

#login_manager object used to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :parameter unicode user_id: user_id (email) user to retrieve

    """
    # Basic query to bring back a specific User object
    return User.query.get(user_id)

# Admin (keeping track of available products for sale)
class User(db.Model, UserMixin): 
    # CREATE TABLE
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    # INSERT INTO User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 



    # Methods for editting attributes 
    def set_id(self):
        return str(uuid.uuid4())
    

    def get_id(self):
        return str(self.user_id)
    
    
    def set_password(self, password):
        return generate_password_hash(password)
    

    def __repr__(self):
        return f"<User: {self.username}>"
    
class Product(db.Model): 
    prod_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
  

    def __init__(self, name, price, quantity, image="", description=""):
        self.prod_id = self.set_id()
        self.name = name
        self.image = self.set_image(image, name)
        self.description = description
        self.price = price
        self.quantity = quantity 

    
    def set_id(self):
        return str(uuid.uuid4())
    

    def set_image(self, image, name):

        if not image:
            pass

        return image
    
    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):

        self.quantity += int(quantity)
        return self.quantity 
    

    def __repr__(self):
        return f"<Product: {self.name}>"


class ProductSchema(ma.Schema):

    class Meta:
        fields = ['prod_id', 'name', 'image', 'description', 'price', 'quantity']

product_schema = ProductSchema()
products_schema = ProductSchema(many=True) 

 