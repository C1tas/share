# Django Tutorial
有条件还是直接读官方文档来的更快~

如果django激发起了你自己写下web的动力，那么文档将是你强有力的陪伴

[文档](https://docs.djangoproject.com/en/1.11/)
## django structure

django 的基本结构是 "project with apps"

下面是一个基本的project结构
``` shell
~/apps/django_test  tree
.
├── django_test
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

1 directory, 5 files

```

增加了app1后的结构

``` shell
✘  ~/apps/django_test  tree 
.
├── app1
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── django_test
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   └── settings.cpython-36.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

4 directories, 14 files

```
- manage.py 用于管理project 运行，生成数据库，调试等等
- settings.py 用于设置project 的基本设置，详见官方文档
- urls.py 用于设置路由，在project和app中作用相同
- wsgi.py 用于设置web网关到python的接口，暂时无用
- admin.py 设置app在admin页面的相关处理
- apps.py 声明了app的全局名字
- models.py 设置app中使用的变量类型，并且根据这个文件设置来生成数据库
- views.py 设置处理相应请求，并如何回显的相关函数

app是project 的一部分，这就意味着，相同的文件名往往具有相同的作用
   
## start write
``` shell
django-admin startproject your_project_name
cd your_project_name
django-admin startapp your_app_name

```
你需要改变你的设置在your_project_name/your_project_name/settings.py

``` python
...

INSTALLED_APPS = [
    'your_project_name.apps.Your_project_nameConfig', # remember to uppercase like PicConfig
    #增加的这行作用为让project 包含该app
    ...
]

...
```

接下来写models.py

``` python
from django.db import models

# Create your models here.
class Pic(models.Model):
    pic_id = models.AutoField(primary_key=True)
    pic_name = models.CharField(max_length=200)
    pic_date = models.DateTimeField(auto_now_add=True)

```
你主要需要明白你需要创建一个class用来声明你会使用到哪些变量

举个例子

你想写个博客，那么变量就应该是标题，日期，标签，分类，内容，作者，等等

这时候你需要查阅官方文档中的field类型来选择适应你所想表示的内容的field

例如日期就是 DateTimeField

!!!重要的事
你需要运行如下命令django才会创建数据库

默认数据库是sqlite3如果你需要改变请在setting中找到相关位置

``` shell
python manager.py makemigrations pic
python manager.py migrate
```

如果没报错那么，就表示django创建数据完成

改变 project/url.py

``` python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^your_app_name/', include('your_app_name.urls')),
]

```
你需要新导入include 用来包含你app中的url文件

改变app/url.py

``` python
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^upload/', views.upload_file, name="upload"),
    url(r'^list/', views.list_file, name="list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

```
url()

这个函数，一个参数是web路由，第二参数是往哪里分发,第三个参数是起的别名

这里的分发在project/urls.py里就是分发到app/urls.py

在app/urls.py中就是分发到views.py中你定义的函数

那么接下来我们就来定义函数

``` python
from django.http import HttpResponse
def index(request):
    return HttpResponse("index")

```
HttpResponse函数的用法有很多，具体还是得见官方文档

第一个参数就是响应内容

这样响应出去的就是纯字符串，如果你想用html以及css来包裹住

那么这时候你需要创建一个templates文件夹在你的app目录下

将响应交由templates渲染的方式有多种，具体选择见官网

这里介绍render

``` python
from django.shortcuts import render
```
保证导入render

然后在你想用templates渲染的输出的地方改为
``` python
return render(request, 'templates_name.html')
```

render的第三个参数，接受用来传入templates的内容

例如你创建了一个

`app/templates/index.html`

```html
{% if list %}
    <ul>
    {% for item in pic_list %}
        <li>{{ item.pic_name }}</li>
    {% endfor %}
    </ul>
{% else %}
    <p>No content</p>
{% endif %}
```

`app/models.py`
``` python
from django.db import models

from django.forms import ModelForm
from django.conf import settings
import uuid
import time
import os

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(time.strftime(settings.DATE_FORMAT), filename)


# Create your models here.
class Pic(models.Model):
    pic_id = models.AutoField(primary_key=True)
    pic_name = models.CharField(max_length=200)
    pic_date = models.DateTimeField(auto_now_add=True)
    pic_content = models.ImageField(upload_to=user_directory_path)

```

`app/views.py`

```python
from django.shortcuts import render
from .models import Pic
def index(request):
    pic_list = Pic.objects.order_by('-pic_id')[:5]
    context = {
        'pic_list': pic_list;,
    }
    return render(request, 'index.html', context)
```

基本的大致就这些

我自己写的练习源码在

[github](https://github.com/C1tas/hack_web)
