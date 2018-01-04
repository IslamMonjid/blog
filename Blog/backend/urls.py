from django.conf.urls import url

from . import views
from views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^patients/$', views.patients, name='patients'),
    url(r'^patient/$', views.patient, name='patient'),
    url(r'^patient/add/$', views.patient, name='patient'),
    url(r'^patient/edit/(?P<patient_id>.+)/$', views.patient, name='patient-id'),
    #url(r'^accounts/login/$', views.patient, name='patient'),
    url(r'^$', HomeView.as_view(), name='home'),
]