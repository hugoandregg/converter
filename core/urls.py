from django.conf.urls import patterns, include, url 

urlpatterns = patterns('core.views',
	url(r'^$', 'index', name='index'),
	url(r'^new/$', 'createSlide', name='createSlide'),
	url(r'^delete/(?P<slide>\w+)/$', 'delete', name='delete'),
	url(r'^(?P<username>\w+)/$', 'showProfile', name='showProfile'),
	url(r'^(?P<username>\w+)/download/$', 'downloadZip', name='downloadZip'),
	url(r'^(?P<username>\w+)/(?P<slide>\w+)/$', 'show', name='show'),
	url(r'^(?P<username>\w+)/(?P<slide>\w+)/download/$', 'download', name='download')
)