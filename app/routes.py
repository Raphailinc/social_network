from flask import render_template, redirect, url_for, flash, request, abort, Blueprint, jsonify, session, current_app
from .models import db
from .forms import RegistrationForm, LoginForm, PostForm, CommentForm
from .models import User, Post, Comment
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user, logout_user, login_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
import os


bp = Blueprint('app', __name__)

UPLOAD_FOLDER = 'static/profile_pics'
UPLOAD_POST_FOLDER = 'static/post_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please enter matching passwords.', 'danger')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('app.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different username.', 'danger')

    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('Login successful!', 'success')
            login_user(user)
            session['profile_image'] = user.profile_image
            return redirect(url_for('app.home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('app.home'))


@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data, post_id=post.id, user=current_user)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('app.view_post', post_id=post_id))
    return render_template('view_post.html', post=post, form=form)


@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, user=current_user)
        if form.image.data:
            image = form.image.data
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_POST_FOLDER'], filename))
            new_post.image = filename
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('app.home'))
    return render_template('create_post.html', form=form)


@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.user:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_POST_FOLDER'], filename))
                post.image = filename
        else:
            post.image = form.current_image.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('app.home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.current_image.data = post.image
    return render_template('edit_post.html', form=form, post=post)


@bp.route('/all_posts')
def all_posts():
    search_query = request.args.get('search', '')

    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        posts = Post.query.join(User).filter(User.id == Post.user_id).filter(Post.title.ilike(f'%{search_query}%')).options(joinedload(Post.user)).paginate(page=page, per_page=per_page, error_out=False)
    else:
        posts = Post.query.join(User).filter(User.profile_image != None).options(joinedload(Post.user)).paginate(page=page, per_page=per_page, error_out=False)
    
    form = CommentForm()
    return render_template('all_posts.html', all_posts_with_profile=posts, form=form)


@bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    with current_app.test_request_context():
        post = Post.query.get_or_404(post_id)
        if current_user != post.user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('app.home'))


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user._get_current_object()

    posts = Post.query.filter_by(user_id=user.id).all()

    if request.method == 'POST':
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    user.profile_image = filename
                    db.session.commit()
                    flash('Profile picture uploaded successfully!', 'success')
                    return redirect(url_for('app.profile'))
                else:
                    flash('Invalid file format. Please upload an image file.', 'danger')

    for post in posts:
        post.comments

    db.session.add(user)

    return render_template('profile.html', user=user, posts=posts)


@bp.route('/update_profile_image', methods=['POST'])
@login_required
def update_profile_image():
    user = current_user
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file.filename != '':
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                user.profile_image = filename
                db.session.commit()
                profile_image_url = url_for('static', filename=f'profile_pics/{filename}')
                session['profile_image'] = filename
                return jsonify({'profile_image_url': profile_image_url})
            else:
                return jsonify({'error': 'Invalid file format. Please upload an image file.'}), 400
    return jsonify({'error': 'No file uploaded.'}), 400


@bp.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user != comment.user:
        abort(403)
    form = CommentForm(obj=comment)
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Comment updated successfully!', 'success')
        return redirect(url_for('app.view_post', post_id=comment.post.id))
    return render_template('edit_comment.html', form=form, comment=comment)


@bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user != comment.user:
        abort(403)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('app.view_post', post_id=post_id))