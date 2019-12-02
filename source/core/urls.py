from django.conf.urls.defaults import *
# from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    # Example:
    # (r'^planner/', include('planner.foo.urls')),
    
    url(r'^$', 'core.views.index', name='core-index'),
    url(r'^profile/$', 'core.views.profile', name='core-profile'),
    url(r'^register/$', 'core.views.register', name='core-register'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='core-login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/core/'}, name='core-logout'),
)
