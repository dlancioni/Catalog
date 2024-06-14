from flask import Flask
from src.db.config import db, url

from web.blueprints.home import bp_home
from web.blueprints.user import bp_user

def setup_database(app):
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    db.init_app(app)
    
def setup_blueprints(app):
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_user)

def create_app():
    app = Flask(__name__,
                static_url_path="",
                static_folder="web/static",
                template_folder="web/templates")
    
    setup_database(app)
    setup_blueprints(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()