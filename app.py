from flask import Flask,g,render_template,redirect,flash,url_for
from  flask_login import LoginManager
import  models , forms
app = Flask(__name__,static_folder='static',static_url_path='')
app.secret_key='AWds43adw5d@#^%UYukku.,mnvc6xzvny6mair7aa265732ddW'
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
@login_manager.user_loader
def userload(userid):
    try:
        models.User.get(models.User.username==userid)
    except models.DoesNotExist:
        return  None

@app.before_request
def before():
    g.db = models.Database
    g.db.connect()

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/register',methods=['GET','POST'])
def signup():
    form=forms.regform()
    if form.validate_on_submit():
        flash('Successfully registered','Success')
        models.User.usersignup(form.username.data,form.password.data,form.email.data)
        return redirect(url_for('index'))
    return render_template('register.html',form=form)




@app.after_request
def end(response):
    g.db.close()
    return response

if __name__ == '__main__':
    models.initial()
    models.User.create_table(safe=True)
    models.Database.commit()
    try:
        models.User.usersignup('ali','ali','ali@amir.com',False)
    except ValueError:
        pass
    app.run(debug=True)
