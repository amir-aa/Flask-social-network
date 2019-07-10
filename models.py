from peewee import *
import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

Database= MySQLDatabase(database='social',host='192.168.1.166', user='root', passwd='020202')
class User(UserMixin, Model):
    username=CharField(unique=True)
    password=CharField(unique=True)
    Email=CharField(unique=False)
    joinat=DateTimeField(default=datetime.datetime.now())
    isadmin=BooleanField(default=False)

    class Meta:
        database = Database
        order_by=('-joinat',)
    @classmethod
    def usersignup(cls,username,passw,email,admin=False):
        try:
            cls.create(
                username=username,
                Email=email,
                isadmin=admin,
                password=generate_password_hash(passw,16))
        except IntegrityError:
            raise ValueError("User Already Exists!! ")
def initial():
    Database.connect()
    Database.create_tables([User],safe=True,fail_silently=False)
    Database.commit()
    Database.close()