from peewee import *
import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

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

    class Meta:
         database=DATABASE
        #order_by=('-joinat',)
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
            raise ValueError("User Already Exists!! ")
DATABASE.connect()

DATABASE.create_tables([User],safe=True)
    #db.commit()
DATABASE.close()
"""def initial1():
    DATABASE.connect()

    DATABASE.create_tables([User],safe=True)
    #db.commit()
    DATABASE.close()"""