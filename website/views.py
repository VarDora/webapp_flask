from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import Posts


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)


@views.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = current_user.first_name
        user_id = current_user.id
        new_post = Posts(title=post_title, content=post_content, author=post_author, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Posts.query.order_by(Posts.date).all()
        return render_template('posts.html', posts=all_posts, user=current_user)


@views.route('/posts/delete/<int:id>')
def delete(id):
    post = Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@views.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Posts.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = current_user.first_name
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post, user=current_user)