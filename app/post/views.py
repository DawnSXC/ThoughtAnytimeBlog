import logging
import os.path
import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, g, jsonify

from werkzeug.utils import secure_filename
from wtforms import csrf

from app import db, user
from app.user.forms import RegistrationForm
from app.user.models import User
from app.post.models import Post, Comment, Category, Collect
from config import Config

post_bp = Blueprint("post", __name__, url_prefix='/post')

File = ['jpg', 'png', 'bmp', 'JPG', 'PNG', 'BMP']


@post_bp.route('/newpost', methods=['GET', 'POST'])
def newpost():
    cur_uid = request.cookies.get('uid')
    cur_u = User.query.get(cur_uid)
    if request.method == 'POST':
        title = request.form.get('title',None)
        category = request.form.get('category',None)
        text = request.form.get('text',None)
        if text and title and category:
            post_img = request.files.get('post_img')
            img_name = post_img.filename

            filetype = img_name.rsplit('.')[-1]
            if filetype in File:
                img_name = secure_filename(img_name)
                file_path = os.path.join(Config.UPLOAD_DIR, img_name)
                post_img.save(file_path)
            user_id = cur_uid
            newpost = Post()
            newpost.title = title
            newpost.category_id = category
            newpost.text = text
            newpost.user_id = user_id
            if img_name:
                path = 'upload/'
                newpost.post_img = os.path.join(path, img_name)

            db.session.add(newpost)
        else:
            return render_template('post.html', user=cur_u,msg="Please enter the post content, title and category.")
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        logging.info(f'User{cur_u.username} post a new blog{newpost.title}')
        return redirect(url_for('user.center'))
    return render_template('post.html', user=cur_u)


@post_bp.route('/detail', methods=['GET', 'POST'])
def detail():
    pid = request.args.get('pid')
    post_detail = Post.query.get(pid)
    post_detail.browsing_times += 1
    db.session.commit()
    uid = request.cookies.get('uid', None)
    if uid:
        user = User.query.get(uid)
        logging.info(f'User:{user.username} read the blog {post_detail.title}.')
        return render_template('detail.html', user=user, post=post_detail)
    return render_template('detail.html', post=post_detail)

@post_bp.route('/collect', methods=['GET', 'POST'])
def collect():
    post_id = request.args.get('pid')
    post = Post.query.get(post_id)
    uid = request.cookies.get('uid')
    u = User.query.get(uid)
    if u:
        collect = Collect()
        collect.user_id = uid
        collect.post_id = post_id
        db.session.add(collect)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return render_template('detail.html', user=u, post=post)
    else:
        return redirect(url_for('user.login'))
    return render_template('detail.html', post=post, user=u)



@post_bp.route('/comment', methods=['GET', 'POST'])
def comment():
    post_id = request.form.get('pid')
    post = Post.query.get(post_id)
    uid = request.cookies.get('uid')
    u = User.query.get(uid)
    if request.method == 'POST':
        if u:
            comment_text = request.form.get('comment',None)
            if comment_text:
                comment = Comment()
                comment.comment = comment_text
                comment.user_id = uid
                comment.post_id = post_id
                db.session.add(comment)
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                return render_template('detail.html', user=u, post=post)
            else:
                return render_template('detail.html',user=u,post=post,msg="Cannot leave blank comments.Please input your comment.")
        else:
            return redirect(url_for('user.login'))
    return render_template('detail.html', post=post, user=u)


@post_bp.route('/deletecomment', methods=['GET', 'POST'])
def deletecomment():
    cid = request.args.get('cid')
    uid = request.cookies.get('uid')
    user = User.query.get(uid)
    com = Comment.query.get(cid)
    post = Post.query.get(com.post_id)

    db.session.delete(com)
    db.session.commit()
    logging.info(f'User:{user.username} delete comment.')
    return render_template('detail.html', user=user, post=post)


@post_bp.route('/like', methods=['GET', 'POST'])
def like():

    post_id = request.args.get('pid')
    post = Post.query.get(post_id)
    post.like_times += 1

    db.session.commit()

    logging.info(f'User like the post {post.title}')
    return jsonify(likenum=post.like_times)

@post_bp.route('/dislike')
def dislike():
    post_id = request.args.get('pid')
    post = Post.query.get(post_id)
    post.dislike_times += 1
    db.session.commit()
    return jsonify(dislikenum=post.dislike_times)


@post_bp.route('/search', methods=['GET', 'POST'])
def search():
    cur_uid = request.cookies.get('uid')
    cur_u = User.query.get(cur_uid)
    if request.method == 'POST':
        search_content = request.form.get('search_content')
        found_post = Post.query.filter(Post.title.contains(search_content) | Post.text.contains(search_content)).all()
        return render_template('blog.html', user=cur_u, post=found_post)

