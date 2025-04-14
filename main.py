import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, send_file
sk, render_template, request, redirect, url_for, flash, Blueprint, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite for simplicity
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Set the login view for unauthorized access

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Blog Post model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# Blueprints
auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
blog = Blueprint('blog', __name__)
contact = Blueprint('contact', __name__)

# Authentication routes
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.signup'))

        new_user = User(first_name=first_name, last_name=last_name, age=age, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))  # Redirect to home page after login
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Main application routes
@main.route('/')
def index():    
    return render_template('index.html')
@main.route('/courses')
def courses():
    return render_template('courses.html')

@main.route('/course/<int:course_id>')
def course_detail(course_id):
    return render_template('course_detail.html')

# Blog routes
@blog.route('/blog', methods=['GET', 'POST'])
def blog_list():
    
    posts = BlogPost.query.order_by(BlogPost.publication_date.desc()).all()
    return render_template('blog/index.html', posts=posts)

@blog.route('/blog/<int:post_id>')
def blog_post(post_id):
    
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)

# Contact routes
@contact.route('/contact', methods=['GET', 'POST'])
def contact_form():
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Handle the form submission here
        # For example, send an email or store the message in a database
        print(f"Name: {name}, Email: {email}, Subject: {subject}, Message: {message}")

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact.contact_form'))

    return render_template('contact.html')



#Register the new blog blueprint


# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(blog, url_prefix='/')
app.register_blueprint(contact, url_prefix='/')

def main():
    app.run(debug=True, port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
