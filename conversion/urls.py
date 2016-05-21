from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns('conversion.views',

    url(r'', views.question),
    url(r'^accueil$', views.home),
    url(r'^date$', views.date_actuelle),

                       )