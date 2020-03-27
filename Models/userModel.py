from app import db, ma
from sqlalchemy import func
from werkzeug.security import check_password_hash



class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    tasks = db.relationship('TaskModel', backref='user', lazy=True)

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
    
    @classmethod
    def validate_password(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return True
        else:
            return False
    
    @classmethod
    def does_email_exists(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return True
        else:
            return False
    
    @classmethod
    def get_user_id(cls, email):
        return cls.query.filter_by(email=email).first().id
    

class UsersSchema(ma.Schema):
    class Meta:
        fields = ("id", "full_name", "email", "created_at", )

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)