from flask import Flask , request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger, swag_from

import logging

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SWAGGER"] = {"title": "Book API",'uiversion': 3}

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Logging
logging.basicConfig(filename="app.log", level=logging.INFO)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}, {self.author}>'

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/api/books', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Book created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string'
                    },
                    'author': {
                        'type': 'string'
                    },
                    'year': {
                        'type': 'integer'
                    }
                }
            }
        },
        500: {
            'description': 'Error creating book'
        }
    }
})
def create_book():
    
      try:
          data = request.get_json()
          title = data.get("title")
          author = data.get("author")
          year = data.get("year")
          
          new_book = Book(title =title, author=author, year = year)
          db.session.add(new_book)
          db.session.commit()
          
          logging.info(f"created new book: {new_book}")
          return jsonify({
                          "title": new_book.title,
                          "author": new_book.author,
                          "year": new_book.year
                          }), 201
      except Exception as e:
          db.session.rollback()
          logging.error(f"Error creating book: {e}")
          return jsonify({"message": "error creating book"}), 500
      
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "BOOK API"})


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)  