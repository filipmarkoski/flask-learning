from flask import Flask, request
import json
import os
import uuid
from datetime import datetime

from sqlalchemy_utils import UUIDType
from flask_cors import CORS
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin
from flask_restful import reqparse

app = Flask(__name__)
sqlite3DatabasePath = os.path.join('C:\\', 'sqlite3', 'sqlitemarkoski.db')
databaseConnectionUrl = f'sqlite:///{sqlite3DatabasePath}'
app.config['SQLALCHEMY_DATABASE_URI'] = databaseConnectionUrl
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model, SerializerMixin):
    __tablename__ = 'Task'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    Description = db.Column(db.String, nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    DateModified = db.Column(db.DateTime, nullable=True)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    UUID = db.Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)

    def __repr__(self):
        return f'{self.ID}-{self.Name}'


cors = CORS(app)
api = Api(app)


class TaskListResource(Resource):
    def get(self):
        tasks = [task.to_dict() for task in Task.query.all()]
        if len(tasks) > 0:
            return tasks
        abort(404, message='No tasks found in the database.')

    def post(self):
        requestJson = request.get_json()
        print(requestJson)
        Name = requestJson['Name']
        Description = requestJson['Description']
        task = Task(Name=Name, Description=Description)
        db.session.add(task)
        db.session.commit()
        return task.to_dict()


class TaskResource(Resource):

    def __init__(self):
        self.requestParser = reqparse.RequestParser()
        self.requestParser.add_argument('Name', type=str, required=True, help='No Task Name provided.', location=json)
        super(TaskResource, self).__init__()

    def get(self, taskID=None):
        if isinstance(taskID, int):
            task = Task.query.get(taskID)
            if task is not None:
                return task.to_dict()
        abort(404, message=f'Task with taskID={taskID} does not exist.')

    def delete(self, taskID=None):
        print('deleting')
        if isinstance(taskID, int):
            task = Task.query.get(taskID)
            if task is not None:
                db.session.delete(task)
                db.session.commit()
                return {'ID': task.ID}
        abort(404, message=f'Task with taskID={taskID} does not exist.')


TASKS_ENDPOINT = '/api/tasks/'
api.add_resource(TaskListResource, TASKS_ENDPOINT, endpoint='tasks')
api.add_resource(TaskResource, os.path.join(TASKS_ENDPOINT, '<int:taskID>'), endpoint='task')

if __name__ == '__main__':
    print(f'Using database: {databaseConnectionUrl}')
    app.run(debug=True)
