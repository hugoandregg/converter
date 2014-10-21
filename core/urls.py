from django.conf.urls import patterns, include, url 

urlpatterns = patterns('core.views',
	url(r'^$', 'index', name='index'),
	url(r'^new/$', 'create', name='create'),
	url(r'^delete/(?P<slide>\w+)$', 'delete', name='delete'),
	url(r'^(?P<username>\w+)/(?P<slide>\w+)$', 'show', name='show'),
	url(r'^(?P<username>\w+)$', 'showProfile', name='showProfile')
)