from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import NewsForm

# 构造对象
app = Flask(__name__)
#  对 应用 加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:1234@localhost:3306/net_news?charset=utf8'
app.config['SECRET_KEY'] = 'a random string'

#  构造新对象
db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000),  nullable=False)
    types = db.Column(db.String(10),  nullable=False)
    image = db.Column(db.String(300))
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean)

    def __repr__(self):
        return '<News %r>' % self.title


# 新闻首页
@app.route('/')
def index():
    #  Flask 会在 templates 文件夹里寻找模板。所以，
    # 如果你的应用是个模块，这个文件夹在模块的旁边；如果它是一个包，那么这个文件夹在你的包里面
    news_list = News.query.filter_by(is_valid=1)
    return render_template('index.html', news_list=news_list)


# 新闻类别
@app.route('/cat/<name>/')
def cat(name):
    #  函数的作用是渲染模板 你需要做的所有事就是将模板名和你想作为关键字的参数传入模板的变量
    #  查询类别为 name 的新闻数据
    news_list = News.query.filter(News.types == name)
    return render_template('cat.html', name=name, news_list=news_list)


#  限制模板接收的变量类型
@app.route('/detail/<int:pk>/')
def detail(pk):
    # 新闻详情信息
    new_obj = News.query.get(pk)
    return render_template('detail.html', new_obj=new_obj)


@app.route('/admin/')
@app.route('/admin/<int:page>/')
def admin(page=None):
    #  新闻管理首页
    #  如果没有传page
    if page is None:
        page = 1
    news_list = News.query.filter_by(is_valid=1).paginate(page=page, per_page=5)
    return render_template('admin/index.html', news_list=news_list)


# get到添加页面，post提交表单
@app.route('/admin/add/', methods=('GET', 'POST'))
def add():
    #  渲染出空的表单
    form = NewsForm()
    #  如果是有效提交
    if form.validate_on_submit():
        #  获取数据 保存数据
        new_obj = News(
            title=form.title.data,
            content=form.content.data,
            types=form.types.data,
            image=form.image.data,
            created_at=datetime.now()
        )
        db.session.add(new_obj)
        db.session.commit()
        #  页面跳转
        return redirect(url_for('admin'))
    return render_template('admin/add.html', form=form)


@app.route('/admin/update/<int:pk>/', methods=('GET', 'POST'))
def update(pk):
    # 更新一条新闻
    new_obj = News.query.get(pk)
    # 如果没有取到数据，跳转后台管理页面
    if not new_obj:
        return redirect(url_for('admin'))
    #  修改前的记录渲染出来
    form = NewsForm(obj=new_obj)
    if form.validate_on_submit():
        #  获取数据
        new_obj.title = form.title.data
        new_obj.content = form.content.data
        new_obj.types = form.types.data
        #  更改记录
        db.session.add(new_obj)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/update.html', form=form)


@app.route('/admin/delete/<int:pk>/', methods=('GET', 'POST'))
def delete(pk):
    # 删除一条新闻
    new_obj = News.query.get(pk)
    if not new_obj:
        return 'no'
    new_obj.is_valid = False
    db.session.add(new_obj)
    db.session.commit()
    return 'yes'

if __name__ == '__main__':
    app.run()
