from django.urls import path
from .views import (
    trade_list_view,
    trade_detail_view,
    trade_delete_view,
    image_create_view,
    image_delete_view,
)

urlpatterns = [
    path("trades/", trade_list_view, name="trade-list"),
    path("trades/<int:pk>/", trade_detail_view, name="trade-detail"),
    path("trades/<int:pk>/delete/", trade_delete_view, name="trade-delete"),
    path("trades/<int:pk>/images/", image_create_view, name="image-create"),
    path("trades/<int:pk>/images/<int:image_pk>/delete/", image_delete_view, name="image-delete"),
]