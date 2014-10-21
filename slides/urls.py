from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slides.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
	url(r'^', include('core.urls', namespace='slides')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
