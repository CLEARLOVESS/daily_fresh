from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
from django.core.urlresolvers import reverse  # 反向解析

from itsdangerous import TimedJSONWebSignatureSerializer as serializer  # 导入加密模块
from itsdangerous import SignatureExpired  # 导入解析秘钥过期异常

from django.views.generic import View

from django.core.mail import send_mail  # 导入发邮件模块

from apps.user.models import User

from django.conf import settings  # 导入setting模块，获取秘钥
# Create your views here.


# /user/register
class RegisterView(View):
    """试图函数类"""
    def get(self, request):
        """get请求方式"""
        return render(request, 'register.html')

    def post(self, request):
        """post请求方式"""
        # 1.接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        is_on = request.POST.get('allow')

        # 2.校验数据
        if not all([username, password, email]):
            return render(request, 'register.html', {'errormsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormsg': '邮箱不合法'})
            # 校验勾选协议
        if is_on != 'on':
            return render(request, 'register.html', {'errormsg': '请勾选协议'})

        # 判断用户名是否已经存在,不存在的话抛出异常，接受异常判断不存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 说明不存在
            user = None
        if user:
            return render(request, 'register.html', {'errormsg': '用户名已存在'})

        # 3.业务处理，用户注册,注册到user表中，可以手动创建注册，这里使用django默认的注册方法
        new_user = User.objects.create_user(username, email, password)
        # 刚刚注册完的用户先不激活
        new_user.is_active = 0
        new_user.save()

        # 加密用户身份信息，生成激活token
        ser = serializer(settings.SECRET_KEY, 3600)
        info = {'confirm':new_user.id}
        token = ser.dumps(info)
        token = token.decode() # 默认解码utf8

        # 发送邮件
        subject = '%s天天生鲜欢迎您!' % username
        message = ''
        sender = settings.EMAIL_FROM
        receiver = [email]
        html_message = '点击下面链接激活<a href="http://127.0.0.1:8000/user/active/%s">激活...</a>' % token# 这里面写html可以正确显示
        send_mail(subject, message, sender, receiver, html_message=html_message)
        # 4.返回页面
        return redirect(reverse('goods:index'))

        # 使用celery异步发送邮件
        # from celery_tasks.tasks import send_register_active_email
        # send_register_active_email.delay(email, username, token)

# /user/active
class ActiveView(View):
    """用户激活类"""
    def get(self, request, token):
        # 解密
        # 1.获取激活的用户信息
        ser = serializer(settings.SECRET_KEY, 3600)
        try:
            info = ser.loads(token)
            # 获取解密的信息
            user_id = info['confirm']

            # 根据id激活账户
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 重定向到index页面
            return redirect(reverse('user:login'))

        except SignatureExpired:
            return HttpResponse('链接已过期...')

# /user/login
class LoginView(View):
    """登录试图类"""
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'login.html', {'username':username})

    def post(self, request):
        """post登录处理"""
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errormsg':'数据不完整'})

        # 业务处理：登录校验
        # 使用django内置校验函数
        # 判断是否记住密码
        response = render(request, 'login.html')
        rem = request.POST['remember']
        if rem == 'on':
            response.set_cookie('username', username, max_age=7*24*3600)
        else:
            response.delete_cookie('username')
        return response
        # 返回应答

# /user
class UserInfoView(View):
    """用户中心--信息页面"""
    def get(self, request):
        return render(request, 'user_center_info.html')

# /user/order
class UserOrderView(View):
    """用户中心--订单页面"""
    def get(self, request):
        return render(request, 'user_center_order.html')

# /user/address
class AddressView(View):
    """用户中心--地址页面"""
    def get(self, request):
        return render(request, 'user_center_site.html')
