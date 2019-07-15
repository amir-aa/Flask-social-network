from peewee import *
import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from app import LoginManager
DATABASE= MySQLDatabase(database='social',host='192.168.1.166', user='root', passwd='020202')



class User(UserMixin, Model):

    username=CharField(unique=True)
    password=CharField(unique=True)
    Email=CharField(unique=False)
    joinat=DateTimeField(default=datetime.datetime.now())
    isadmin=BooleanField(default=False)
    is_active=BooleanField(default=True)
    image=CharField(default='user.png')
    gender = CharField()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username

    class Meta:
         database=DATABASE
        #order_by=('-joinat',)
    def get_posts(self):
        return Post.select().where(Post.user==self)

    #select post that we want
    def get_stream(self):
        return Post.select().where((Post.user==self))
    @classmethod
    def usersignup(cls,username,password,email,image,gender,admin=False):
        try:
            cls.create(
                username=username,
                Email=email,
                isadmin=admin,
                password=generate_password_hash(password,16),
                image=image,
                gender=gender)

        except IntegrityError:
            #DATABASE.rollback()
            raise ValueError("User Already Exists!! or maybe Validation Error!")

class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now())
    user=ForeignKeyField(rel_model=User,related_name='posts',model=User,backref='posts')
    content = TextField()
    class Meta:
         database=DATABASE
DATABASE.connect()

DATABASE.create_tables([User,Post],safe=True)

    #db.commit()
DATABASE.close()
"""def initial1():
    DATABASE.connect()

    DATABASE.create_tables([User],safe=True)
    #db.commit()
    DATABASE.close()"""