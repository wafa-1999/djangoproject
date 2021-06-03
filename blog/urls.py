from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
  path('blog/', views.frontpage, name='frontpage'),
  path('<slug:slug>/', views.post_detail, name='post_detail')
    
    
    
]

#from django.urls import path,include
#from django.conf.urls import url
#from . import views

#urlpatterns=[
 #   path('postList/',views.index),
  #  path('<slug:post>/',views.post_detail,name="post_detail"),
#]