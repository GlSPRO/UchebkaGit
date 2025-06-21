from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from up1.views import first_page, second_page

urlpatterns = [
    path('', first_page),
    path('first_page/', first_page),
    path('second_page/', second_page),
    path('admin/', admin.site.urls),
    path('up1/', include('up1.urls')),  # если у тебя есть маршруты в приложении
]
