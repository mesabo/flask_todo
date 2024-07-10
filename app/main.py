from flask import Flask
from app.Database.db_config import init_db, get_database
from app.Routers.todo_router import todo_bp

app = Flask(__name__)

# Initialize the MongoDB connection
init_db(app)

# Register the todo blueprint with the Flask application
app.register_blueprint(todo_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
