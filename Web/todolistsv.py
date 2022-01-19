#!python3
from datetime import datetime
from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from sqlalchemy import and_

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    login_account = db.Column('login_account', db.String(length=100),unique=True, nullable=False)
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(length=255), nullable=True)

    def __init__(self, login_account, name):
        self.login_account = login_account
        self.name = name

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class ToDoItem(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    content = db.Column('content', db.String(255), nullable=False)
    status = db.Column('status', db.Boolean)
    created = db.Column('created', db.DATETIME, default=datetime.now, nullable=False)
    modified = db.Column('modified', db.DATETIME, default=datetime.now, nullable=False)

    def __init__(self, user_id, content=''):
        self.user_id = user_id
        self.content = content
        self.status = False
        now = datetime.now()
        self.created = now
        self.modified = now

class ToDoItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ToDoItem
        load_instance = True

    created_at = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')
    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')

class Login(Resource):
    def get(self):
        """
        ログインしてユーザ情報を取得する
        """
        login_account = request.args.get('login_account')
        user = User.query.filter_by(login_account=login_account).first()
        
        if user: 
            # ユーザ情報を返却
            return jsonify(
                {'status': 'ok', 
                'user': UserSchema(many=False).dump(user)
                })

        else:
            # 存在しないユーザIDが指定された
            abort(404)

class ToDoList(Resource):
    def get(self, user_id, todo_id=None):
        """
        ユーザーのTODOを取得する
        """
        if not todo_id :
            to_do_item = ToDoItem.query.filter_by(user_id=user_id).all()
        else :
            to_do_item = ToDoItem.query.filter(and_(ToDoItem.user_id == user_id, ToDoItem.id == todo_id)).all()
        if to_do_item: 
            return jsonify(
                {'status': 'ok', 
                'todo': ToDoItemSchema(many=True).dump(to_do_item)
                })
        else:
            return jsonify(
                {'status': 'ok', 
                'todo': []
                })
    
    def post(self, user_id):
        """
        TODOを追加する
        """
        try:
            json = request.get_json(force = True)
            content = json['content']
            to_do_item = ToDoItem(user_id, content)
            db.session.add(to_do_item)
            db.session.commit()
            return jsonify(
                {'status': 'ok', 
                'todo': ToDoItemSchema(many=False).dump(to_do_item)
                })
        except:
            return jsonify(
                {'status': 'ng'
                })

    def put(self, user_id, todo_id):
        """
        ユーザーのTODOを更新する
        """
        try:
            json = request.get_json(force = True)
            to_do_item = ToDoItem.query.filter(and_(ToDoItem.user_id == user_id, ToDoItem.id == todo_id)).first()
            if not to_do_item:
                return jsonify(
                {'status': 'ng',
                    'error_msg': 'Not found'
                })
            if 'content' in json:
                content = json['content']
                to_do_item.content = content
            if 'status' in json:
                status = json['status']
                to_do_item.status = status
            now = datetime.now() 
            to_do_item.modified = now
            db.session.flush()
            db.session.commit()
            return jsonify(
                {'status': 'ok', 
                'todo': ToDoItemSchema(many=False).dump(to_do_item)
                })
        except:
            return jsonify(
                {'status': 'ng',
                    'error_msg': 'Error Pram'
                })

    def delete(self, user_id, todo_id):
        """
        ユーザーのTODOを削除する
        """
        try:
            to_do_item = ToDoItem.query.filter(and_(ToDoItem.user_id == user_id, ToDoItem.id == todo_id)).first()
            if not to_do_item:
                return jsonify(
                {'status': 'ng',
                    'error_msg': 'Not found'
                })
            db.session.delete(to_do_item)
            db.session.commit()
            return jsonify(
                {'status': 'ok'
                })
        except:
            return jsonify(
                {'status': 'ng',
                    'error_msg': 'Error Pram'
                })

def init_user():
    user = User('abc', 'エービーシー')
    db.session.add(user)
    user = User('123', '一二三四')
    db.session.add(user)
    db.session.commit()

def init_todo_item():
    todo_item = ToDoItem(1, 'TEST')
    db.session.add(todo_item)
    todo_item = ToDoItem(1, 'テスト2')
    db.session.add(todo_item)
    db.session.commit()


api.add_resource(Login, '/login')
api.add_resource(ToDoList, '/todolist/<int:user_id>', '/todolist/<int:user_id>/<int:todo_id>')

if __name__ == '__main__':
    db.create_all()
    cnt = User.query.count()
    if cnt <= 0:
        init_user()
    cnt = ToDoItem.query.count()
    if cnt <= 0:
        init_todo_item()
    app.run(port=8888, debug=True)
