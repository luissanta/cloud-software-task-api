from datetime import datetime
from marshmallow import fields, Schema
from app.databases.database import db


class Task(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(128))
    file_name = db.Column(db.String(255))
    original_extension = db.Column(db.String(128))
    new_extension = db.Column(db.String(128))
    status = db.Column(db.String(128))
    id_user = db.Column(db.Integer)
    id_original_file = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class File(db.Model):
    __tablename__ = 'files'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    original_name = db.Column(db.String(100), nullable=False)
    temporal_name = db.Column(db.String(), nullable=True)
    new_format = db.Column(db.String(), nullable=True)
    compressed_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
        

class GetTaskSchema(Schema):
    class Meta:
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True            
    id = fields.String()
    file_name = fields.String()
    original_extension = fields.String()
    new_extension = fields.String()
    status = fields.String()
    task_id = fields.String()


class PostTaskSchema(Schema):
    class Meta:
        model = Task
        include_relationships = False
        include_fk = False
        load_instance = False
    id = fields.String()
    task_id = fields.String()
    status = fields.String()   


class GetTaskByIdSchema(Schema):
    class Meta:
        model = Task
        include_relationships = False
        include_fk = False
        load_instance = False
    id = fields.String()        
    task_id = fields.String()
    status = fields.String()   
    file_name = fields.String()   
