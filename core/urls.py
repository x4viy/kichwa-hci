# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include  # add this
import apps.home.views.vw_home
from apps.home.views.vw_home import *

from apps.api.views.vw_api_juego import *

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("100/", include("apps.authentication.urls")), # Auth routes - login / register
    path('', home, name='home'),
    path('100/', include("apps.home.urls")),
    path('200/', include("apps.gen.urls")),
    path('300/', include("apps.sis.urls")),
    path('500/', include("apps.api.urls")),
    path('chat/', include("apps.clasificacion.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)