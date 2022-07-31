from django.conf.urls import include
from django.urls import re_path, path
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'civdj.views.home', name='home'),
    re_path(r'^admin/', admin.site.urls),
    # For now we simply redirect anything to pbspy!
    path('', include('pbspy.urls')),
]
