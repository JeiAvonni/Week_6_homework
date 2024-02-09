from flask import Flask
from flask_migrate import Migrate

# Internal imports
from config import Config
from .models import login_manager, db
from .blueprints.site.routes import site
from .blueprints.auth.routes import auth


# Instantiate my flask Target
app = Flask(__name__)

# Telling my Target (app) what class my config is in
app.config.from_object(Config)


# Wrapping Target in login manager
login_manager.init_app(app)
login_manager.login_view = 'auth.sign_id'
login_manager.login_message = "Log in now to get points!"
login_manager.login_message_category = 'warning'

# Rating first route using the route decorator
# @Target.route("/")
# def Welcome_to_Target():
#    return "<p>Welcome_to_Target!</p>"

# Registering blueprint site
app.register_blueprint(site)
app.register_blueprint(auth)

# Instantiate database and wrap Target
db.init_app(app)
migrate = Migrate(app, db)