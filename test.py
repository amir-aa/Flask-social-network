from peewee import *
import datetime

db = MySQLDatabase(database='test',host='192.168.1.166', user='root', passwd='020202') #create database to interact with

#create a class for blogposts
class Post(Model):
    id = PrimaryKeyField()
    date = DateTimeField(default = datetime.datetime.now)
    title = CharField()
    text = TextField()

    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Post], safe = True)
    db.close()

initialize_db() #if db tables are not created, create them
post = Post.create(id=66, title="Some 333title", text="some 44text1") #add a new row
post.save() #persist it to db, not necessarily needed