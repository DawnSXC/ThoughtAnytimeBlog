import logging

from app import init_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import render_template, request, redirect, url_for


from app.post.models import Post
from app.user.models import User, Suggestion
from config import Config, DevelopementConfig, ProductionConfig

app = init_app("dev")

# 使用终端脚本工具启动和管理flask
manager = Manager(app)

# 启用数据迁移工具
Migrate(app, db)
# 添加数据迁移的命令到终端脚本工具中
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    uid = request.cookies.get('uid', None)
    if uid:
        user = User.query.get(uid)
        return render_template("index.html", user=user)
    else:
        return render_template("index.html")


@app.route('/blog')
def blog():
    cur_uid = request.cookies.get('uid', None)
    post = Post.query.order_by(-Post.post_time).all()
    if cur_uid:
        cur_u = User.query.get(cur_uid)
        return render_template('blog.html', user=cur_u, post=post)
    else:
        return render_template('blog.html', post=post)


@app.route('/categoryblog/<int:category_id>')
def categoryblog(category_id):
    cur_uid = request.cookies.get('uid', None)
    post = Post.query.filter(Post.category_id == category_id).all()
    if cur_uid:
        cur_u = User.query.get(cur_uid)
        return render_template('blog.html', user=cur_u, post=post)
    else:
        return render_template('blog.html', post=post)


@app.route('/displayuser/<int:user_id>')
def displayuser(user_id):
    user = User.query.get(user_id)
    post = Post.query.filter(Post.user_id == user_id).all()
    logging.info(f'=========User check the information of {user.username}============')
    return render_template('displayuser.html', user=user, post=post)


@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    if request.method == 'POST':
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        title = request.form.get('title', None)
        des = request.form.get('des', None)
        if name and email and title and des:
            suggestion = Suggestion()
            suggestion.username = name
            suggestion.email = email
            suggestion.title = title
            suggestion.description = des
            db.session.add(suggestion)
            db.session.commit
            logging.info(f'User: {name} complaints or problems, please deal with them as soon as possible')
            return redirect(url_for('index'))
        else:
            return render_template('suggestion.html', msg='Please input all information.')

    return render_template('suggestion.html')



if __name__ == '__main__':
    manager.run()
