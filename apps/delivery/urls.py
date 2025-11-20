from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    # 配送员相关
    path('persons/', views.DeliveryPersonListView.as_view(), name='delivery-person-list'),
    path('persons/create/', views.DeliveryPersonCreateView.as_view(), name='delivery-person-create'),
    path('persons/<int:pk>/', views.DeliveryPersonDetailView.as_view(), name='delivery-person-detail'),
    
    # 配送记录相关
    path('', views.DeliveryListView.as_view(), name='delivery-list'),
    path('<int:pk>/', views.DeliveryDetailView.as_view(), name='delivery-detail'),
    path('assign/', views.assign_delivery, name='assign-delivery'),
    path('location/update/', views.update_delivery_location, name='update-delivery-location'),
    path('track/<int:order_id>/', views.delivery_track, name='delivery-track'),
    
    # 配送轨迹
    path('<int:delivery_id>/tracks/', views.DeliveryTrackListView.as_view(), name='delivery-track-list'),
    
    # 配送评价
    path('<int:delivery_id>/ratings/', views.DeliveryRatingListView.as_view(), name='delivery-rating-list'),
    path('ratings/create/', views.DeliveryRatingCreateView.as_view(), name='delivery-rating-create'),
    
    # 统计
    path('stats/', views.delivery_stats, name='delivery-stats'),
]
