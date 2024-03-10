from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functions import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '78665fhgg'

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

# Create a user model with secure password hashing
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Replace with your actual user authentication logic (e.g., database access)
users = {

    "admin": User(1, "admin", generate_password_hash("admin"))

}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

#login route
@app.route('/', methods=['GET', 'POST'])
def login():
    #login form logic
    if request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')
        
        print('i: {} {} '.format(username,password))
        user = users.get(username)
        
        if user and user.verify_password(password):
            login_user(user)
            
            print('Called login')
            return render_template('dashboard.html', system_info=get_system_info())
        else:
            return render_template('login.html', error="Invalid username or password")
            
    return render_template('login.html')

#home route --> Dashboard
@app.route('/home')
@login_required
def home():
    return render_template('dashboard.html', system_info=get_system_info())
    

#logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


#command route
@app.route('/control', methods=['POST'])
def control():
    if request.method == 'POST':
        data = request.get_json()
        cmd_inp = data.get('command')
        
        print(cmd_inp)
        command_out = run_command(cmd_inp)
        print(command_out)
        
        return {'command':cmd_inp,'output':command_out}

@app.route('/info', methods=['GET'])
def info():
    if request.method == 'GET':
        return {'info':get_system_info()}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

