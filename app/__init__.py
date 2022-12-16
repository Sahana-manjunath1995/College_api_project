from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "College database"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.errorhandler(404)
def not_found(error):
    """Error page to show on page not found (404) error."""
    return render_template('404.html'), 404

# get and register module blueprints
from app.views.controllers import views as views_module
from app.database.controllers import database as database_module

app.register_blueprint(views_module)
app.register_blueprint(database_module)


