from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
# 第一个参数一般写路径，是名字
app = Celery('celery_tasks.tasks', broker='redis://192.168.164.140/0')


@app.task
def send_register_active_email(to_who, from_who, token):
    """
    :param to_who:发给谁
    :param from_who: 发件人
    :param token: token信息
    :return:
    """
    subject = '%s天天生鲜欢迎您!' % from_who
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_who]
    html_message = '点击下面链接激活<a href="http://127.0.0.1:8000/user/active/%s">激活...</a>' % token  # 这里面写html可以正确显示
    send_mail(subject, message, sender, receiver, html_message=html_message)
