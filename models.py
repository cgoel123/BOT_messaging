from peewee import *
import datetime

db = SqliteDatabase('test.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    created_date = DateTimeField(default=datetime.datetime.now)
    first_name = CharField(null=True)
    user_id = CharField(unique=True)

class GroupUsers(BaseModel):
    user = ForeignKeyField(User)
    group_name = CharField(null=True)
    group_id = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        primary_key = CompositeKey('user', 'group_id')

class DataSharing(BaseModel):
    url_text = CharField()
    user = ForeignKeyField(User)
    created_date = DateTimeField(default=datetime.datetime.now)
    shared = BooleanField(default=False)

