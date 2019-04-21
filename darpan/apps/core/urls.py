app_name = "core"

from django.urls import path

from .views import *

urlpatterns = [
    path("", view = MessageCreate.as_view(), name="home"),
    #path("", view=user_list_view, name="list"),
    #path("~redirect/", view=user_redirect_view, name="redirect"),
    #path("~update/", view=user_update_view, name="update"),
    #path("~update/", view=user_update_view, name="update"),
    path("message/list/", view=MessageList.as_view(), name="message-list"),
    path("message/<int:pk>/", view=MessageDetail.as_view(), name="message-detail"),
]
