from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'talus_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^docs/', include('rest_framework_swagger.urls')),
	url(r'^api/', include('api.urls')),
	url(r'^code_cache/', include('code_cache.urls'))
)
