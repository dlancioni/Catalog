from dotenv import load_dotenv, find_dotenv
from flask import Flask
from web.routes.home import bp_home
from web.routes.payment import bp_payment
from web.routes.transaction import bp_transaction
from web.routes.arcesium import bp_arcesium
from web.routes.cash_overview import bp_cash_overview
from web.routes.report import bp_report
from web.routes.file import bp_file

def setup_blueprints(app):
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_payment)
    app.register_blueprint(bp_transaction)
    app.register_blueprint(bp_arcesium)
    app.register_blueprint(bp_cash_overview)
    app.register_blueprint(bp_report)
    app.register_blueprint(bp_file)

def create_app():
    app = Flask(__name__,
                static_url_path="",
                static_folder="web/static",
                template_folder="web/templates")
    
    setup_blueprints(app)
    return app

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    app = create_app()
    app.run()