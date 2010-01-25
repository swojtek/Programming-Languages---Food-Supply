from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^se/', include('se.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    #Index page, it maps to / . Once the page is called it will look in se/net/views.py for a function called index
    (r'^$', 'se.net.views.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^taskcompleted', 'se.net.views.taskcompleted'),
    (r'^taskslist/$', 'se.net.views.taskslist'),
    (r'^reportgen/$', 'se.net.views.reportgen'),
    (r'^repgenmanager/$', 'se.net.views.repgenmanager'),
    (r'^repgenagent/', 'se.net.views.repgenagent'),
    (r'^resp/', 'se.net.views.resp'),
)
