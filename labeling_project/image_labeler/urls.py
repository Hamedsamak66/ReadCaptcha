from django.urls import path
from . import views

urlpatterns = [
    path('<int:image_id>/', views.label_image, name='label_image'),
    path('done/', views.done, name='done'),  # ویوی اتمام را بعداً اضافه کنید
    path('', views.index, name='index'),  # مسیر صفحه اصلی
]
        
    