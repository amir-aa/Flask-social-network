from flask import Flask,g,render_template,redirect,flash,url_for,request,session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import  models , forms,os

from flask_bcrypt import check_password_hash
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
#----------------------configs------------------------------
app = Flask(__name__,static_folder='static',static_url_path='')
app.secret_key='AWds43adw5d@#^%UYukku.6,mnvc6xzvny6mair7aa265732ddW'
uploadfolder="\imgprofiles"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = uploadfolder
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024

from werkzeug.wsgi import SharedDataMiddleware

aut=False

LoginManager.login_view = "profile"
app.config['TESTING'] = False
#.........................................
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
    g.user=current_user

@app.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return 'salam'

listusers=[]
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/register',methods=['GET','POST'])
def signup():
    form=forms.regform()
    if form.validate_on_submit():
        #models.User.usersignup()
        f=form.image.data
        models.User.usersignup(form.username.data,form.password.data,form.email.data,str(f.filename),form.gender.data)
        filename = secure_filename(f.filename)

        f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        flash('Successfully registered', 'Success')
        return redirect(url_for('login'))
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
                aut=True
                #a=models.User.is_authenticated

                listusers.append(current_user.username)
                #current_user.isauthenticated=True
                #print(a)
                session['un1111']='loggedin'
                #session.pop('us',None)

                session['nam']=current_user.username
                #session.pop('nam', None)
                flash("successfully signed in","success")
                #return render_template('user-area/02-ProfilePage.html')
                return redirect(url_for('profile'))
            else:
                flash("Does not Match", "error")
            return render_template('main.html',form=form)
    return render_template('main.html', form=form)
@app.route('/profile',methods=['GET','POST'])
def profile():
    if session['un1111']=='loggedin':
        a=session['nam']

        user = models.User.get(models.User.username == a)
        login_user(user)
        stream = models.Post.select().limit(50)
        
        # image=models.User.get(models.User.username==a)
        # qt=models.User.select(models.User.image).where(models.User.username==user)
        return render_template('user-area/02-ProfilePage.html', args=a, pic=user.image, stream=stream)
    else:
        return 'access denied'
@app.route('/post',methods=['GET','POST'])
def newpost():
    if session['un1111'] == 'loggedin':
        a = session['nam']
        user = models.User.get(models.User.username == a)
        login_user(user)
        form=forms.post_form()
        if form.validate_on_submit():
            models.Post.create(user=g.user._get_current_object(),content=form.content.data.strip())
            flash("Content has Posted",'success')
            return redirect(url_for('profile'))
        return render_template('Newfeed.html',form=form)
    else:
        return redirect(url_for('login'))
@app.route('/logout')
@login_required
def logout():
    session['un1111'] = 'off'
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
