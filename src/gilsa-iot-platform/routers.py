from rest_framework import routers

import iotdevice.api.v1.urls
import iotauth.api.v1.urls

api_v1_router = routers.DefaultRouter()

iotdevice.api.v1.urls.register_urls(api_v1_router)
iotauth.api.v1.urls.register_url(api_v1_router)
