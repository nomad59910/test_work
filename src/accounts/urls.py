from django.conf.urls import url
from django.contrib.auth.views import login, logout
app_name = 'accounts'

urlpatterns = [
    url(r'^sign-in', login, {'template_name':'accounts/login.html',},
        name='login'),
    url(r'^logout$', logout, {'next_page': 'task:tasks', }, name='logout'),
]
