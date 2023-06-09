from io import BytesIO
from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.tasks import TaskService
from app.services.files import FileService
from app.data_transfer_objects.file import FileTypeDTO
from app.validators.file import validate_get_file

api_routes = Blueprint('api', __name__)


@api_routes.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    max_tasks = request.args.get('max', None)
    order_tasks = request.args.get('order', None)
    id_user = get_jwt_identity()
    service = TaskService()
    return service.get_task(id_user, max_tasks, order_tasks)


@api_routes.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    fetched_file = request.files['file']
    new_format = request.form.get('newFormat', None)

    if new_format is None:
        return "The newFormat is required", 422

    name_file = fetched_file.filename
    file_data = fetched_file.read()
    id_user = get_jwt_identity()
    service = TaskService()    
    return service.post_task(id_user, name_file, file_data, new_format), 201


@api_routes.route('/tasks/<id_task>', methods=['GET'])
@jwt_required()
def get_task(id_task: str):
    service = TaskService()
    return service.get_task_by_id(id_task)


@api_routes.route('/tasks/<id_task>', methods=['DELETE'])
@jwt_required()
def delete_task(id_task: str):
    service = TaskService()            
    if service.delete_task_by_id(id_task):
        return {}, 204
    else:
        return {'response': 'Status not able to be deleted'}, 422


@api_routes.route('/files/<int:file_id>', methods=['GET'])
@jwt_required()
def get_file(file_id: int):
    file_type = FileTypeDTO(request.args.get('type'))
    validate_get_file(file_type)

    service = FileService()
    data, name = service.get_file(file_id, file_type)

    return send_file(BytesIO(data), download_name=name), 200
