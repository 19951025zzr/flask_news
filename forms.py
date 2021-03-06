from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired


# 定义表单
class NewsForm(FlaskForm):
    title = StringField(label='新闻标题', validators=[DataRequired('请输入标题')],
                        description='请输入标题',
                        render_kw={'required': 'required', 'class': 'form-control'})
    content = TextAreaField(label='新闻内容', validators=[DataRequired('请输入内容')],
                            description='请输入内容',
                            render_kw={'required': 'required', 'class': 'form-control'})
    types = SelectField('新闻类型',
                        choices=[('推荐', '推荐'), ('百家', '百家'), ('本地', '本地'), ('图片', '图片')],
                        render_kw={'class': 'form-control'})
    image = StringField(label='新闻图片',
                        description='请输入图片地址',
                        render_kw={'required': 'required', 'class': 'form-control'})
    # image = FileField(label='新闻图片',
    #                   description='请输入图片地址',
    #                   render_kw={'required': 'required', 'class': 'form-control'})
    submit = SubmitField('提交', render_kw={
        'class': 'btn-success'
    })