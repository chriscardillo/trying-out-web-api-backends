from app import db

todo_tags = db.Table('todo_tags',
                     db.Column('todo_id', db.Integer, db.ForeignKey('todos.id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)
