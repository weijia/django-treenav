from django.conf.urls import url, patterns, include, handler404
from django.http import HttpResponse, HttpResponseNotFound
from django.template import Template, Context

from django.contrib import admin
admin.autodiscover()


def test_view(request, item_slug):
    pslug = request.POST['pslug']
    N = request.POST['N']
    t = Template('{% load treenav_tags %}{% single_level_menu pslug N %}')
    c = Context({
        "request": request,
        "pslug": pslug,
        "N": N,
    })
    return HttpResponse(t.render(c))


def test_404(request):
    return HttpResponseNotFound()


handler404 = test_404  # noqa


urlpatterns = patterns('',  # noqa
    url(r'^admin/', include(admin.site.urls)),
    url(r'^item/(?P<item_slug>[\w-]+)/$', test_view, name='test_view'),
    url(r'^old/', include('treenav.urls')),
)
