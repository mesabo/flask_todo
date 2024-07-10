from flask import Flask
from app.Database.db_config import init_db, get_database
from app.Routers.todo_router import todo_bp
from flasgger import Swagger

app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(app)

# Initialize the MongoDB connection
init_db(app)

# Register the todo blueprint with the Flask application
app.register_blueprint(todo_bp, url_prefix='/api')

@app.route('/')
def home():
    return 'Welcome to the Flask Todo APP!'


@app.route('/test')
def test():
    return 'Test route'


if __name__ == '__main__':
    app.run(debug=False)
