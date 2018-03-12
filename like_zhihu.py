from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Comment
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 首页
@app.route('/')
def index():
    context = {
        # 按发布时降序排序
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果想再31天不需要登录
            session.permenent = True
            return redirect(url_for('index'))
        else:
            return '手机号码或密码错误，请确认后再登录！'


# 注册
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        # 手机号码验证，如果注册了，就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号码已被注册，请更换手机号码！'
        else:
            if password != confirm:
                return '两次号码不相同，请核对后在填写！'
            else:
                user = User(telephone=telephone, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录页面
                return redirect(url_for('login'))


# 发布问答
@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


# 问答详情
@app.route('/detail/<question_id>')
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question)


# 评论
@app.route('/comment', methods=['POST'])
@login_required
def comment():
    content = request.form.get('content')
    question_id = request.form.get('question_id')
    comment = Comment(content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    question = Question.query.filter(Question.id == question_id).first()
    comment.question = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


if __name__ == '__main__':
    app.run()
