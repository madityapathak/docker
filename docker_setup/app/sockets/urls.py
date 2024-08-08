from django.urls import path
from . import views


app_name = 'sockets'

urlpatterns = [
	 path('<str:pk>/',views.testview, name='testview'),
]


