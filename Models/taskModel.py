from app import db, ma
from sqlalchemy import func


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    completed = db.Column(db.Integer,nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()
    
    @classmethod
    def fetch_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "completed", "created_at", "user_id")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)