from django.urls import path
from .views import home
#from django.urls import 
from django.views.generic.base import RedirectView

urlpatterns = [
    path('home/', home, name="home"),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=True), name='index'),
]
