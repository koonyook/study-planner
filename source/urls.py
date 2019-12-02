from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^planner/', include('planner.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Serve static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),        
    (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ADMIN_MEDIA_ROOT}),
    
    # Include core app
    (r'^core/', include('planner.core.urls')),

    # For testing purpose
	(r'^testapp/$', 'planner.testapp.views.index'),
	(r'^testapp/run/$', 'planner.testapp.views.run'),
	(r'^testapp2/$', 'planner.testapp2.views.run'),
)
