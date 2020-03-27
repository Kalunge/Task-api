from app import api, fields, Resource, jwt_required, get_jwt_identity
from Models.taskModel import TaskModel, tasks_schema, task_schema
from Models.userModel import UserModel



task_nameSpace = api.namespace('tasks', description='All operations dealing with tasks')

task_model = api.model('Task', {
    'title' :fields.String(),
    'description' :fields.String(),
})


@task_nameSpace.route('')
class TaskList(Resource):
    @jwt_required
    def get(self):
        '''Get a List of REsources by acertain user'''
        user_id = get_jwt_identity()
        user = UserModel.fetch_by_id(user_id)
        tasks = user.tasks
        return tasks_schema.dump(tasks)

    @api.expect(task_model)
    @jwt_required
    def post(self):
        ''''POst a task to the list of tasks by a certain user'''
        data = api.payload
        task = TaskModel(**data, user_id=get_jwt_identity())
        task.save_to_db()
        return task_schema.dump(task)


@task_nameSpace.route('/<int:id>')
class Tasks(Resource):
    def get(self, id):
        '''Get a specific task by a specific user by its id'''
        task = TaskModel.fetch_by_id(id)
        return task_schema.dump(task), 200

    @api.expect(task_model)
    def put(self, id):
        data = api.payload
        task = TaskModel.fetch_by_id(id)
        if u'title' in data:
            task.title = data['title']
        if u'description' in data['description']:
            task.description = data['description']
        return task_schema.dump(task), 201
    
    def delete(self, id):
        '''Deletes a task from a specific user by its id'''
        task = TaskModel.fetch_by_id(id)
        if task:
            task.delete_from_db()
            return {'message':'task deleted successfully'}
        else:
            {'message':'task does not exist'}, 404

        


