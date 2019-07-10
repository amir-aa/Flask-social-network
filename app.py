from flask import Flask,g,render_template,redirect,flash,url_for
from  flask_login import LoginManager,login_user,logout_user,login_required
import  models , forms
from flask_bcrypt import check_password_hash
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
    g.db = models.DATABASE
    g.db.connect()

@app.route('/')
def index():
    return 'Hello World!'



@app.route('/register',methods=['GET','POST'])
def signup():
    form=forms.regform()
    if form.validate_on_submit():
        flash('Successfully registered','Success')
        models.User.usersignup(form.username.data,form.password.data,form.email.data,form.image.data,form.gender.data)
        return redirect(url_for('index'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    #return render_template('main.html')
    form=forms.Loginform()
    if form.validate_on_submit():
        try:
            user=models.User.get(models.User.username==form.username.data)

        except models.DoesNotExist:
            flash("Does not Match","error")
        else:

            if check_password_hash(user.password,form.password.data):
                login_user(user)
                flash("successfully signed in","success")
                return redirect(url_for('index'))
            else:
                flash("Does not Match", "error")
            return render_template('main.html',form=form)
    return render_template('main.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged Out!!')
    return redirect(url_for('index'))

@app.after_request
def end(response):
    g.db.close()
    return response
try:
    models.User.usersignup('amir','01','amir_ahmadabadi2000@outlook.com','boy.png','boy',True)
except:
    pass
if __name__ == '__main__':
    models.initial1()
    #models.User.create_table(safe=True)
    #models.Database.commit()


    app.run(debug=True)
