"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView
from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicLoginView, RegisterView
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt  # 取消csrf token验证
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT

import xadmin


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name='index'),  # name字段 方便html页面进行跳转
    path('login/', LoginView.as_view(), name='login'),
    path('d_login/', csrf_exempt(DynamicLoginView.as_view()), name='d_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # 配置上传文件的访问url (字典内传递全局变量)
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^captcha/', include('captcha.urls')),  # include使此正则包括指定url路径
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name='send_sms'),  # 此方法可混合正则表达式使用
    url(r'^org/', include(("apps.organizations.urls", 'organizations'), namespace='org')),  # 管理url，namespace给各个app加上前缀 例如 org/list
    url(r'^op/', include(("apps.operations.urls", 'operations'), namespace='op')),

    url(r'^course/', include(("apps.courses.urls", 'courses'), namespace='course')),

]
