import os
from flask_sqlalchemy import SQLAlchemy


def database(app):
    databaseConnectionUrl = os.path.join('sqlite3:', 'C:\\', 'sqlite3', 'sqlitemarkoski.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = databaseConnectionUrl
    db = SQLAlchemy(app)
    db.create_all()

    return db
