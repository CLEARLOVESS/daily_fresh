from django.conf.urls import url
from apps.user.views import RegisterView,ActiveView,LoginView

urlpatterns = [
    url(r'^register$', RegisterView.as_view()), # 注册
    url(r'^active/(?P<token>.*)', ActiveView.as_view()), # 注册校验

    url(r'^login/$', LoginView.as_view(), name='login'), # 登录页面
    """..."""
    # url(r'^')
]