from django.conf.urls.defaults import *
from django.conf import settings
#import haystack
from django.contrib import admin
from django.http import HttpResponse

#haystack.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
#    (r'^search/', include('haystack.urls')),
)

if settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
    )

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
    url(r'^robots.txt', lambda request: HttpResponse("User-agent: *\nAllow: /\n")),
)


