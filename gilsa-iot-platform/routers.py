from rest_framework import routers

import iotdevice.api.v1.urls

api_v1_router = routers.DefaultRouter()

iotdevice.api.v1.urls.register_urls(api_v1_router)