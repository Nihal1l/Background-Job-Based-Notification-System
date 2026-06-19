from django.urls import path

from .views import (
    NotificationCreateView,
    NotificationListView,
    RetryNotificationView,
    # SpectacularAPIView,
    # SpectacularSwaggerView,
    health_check
)

urlpatterns = [
    path(
        '',
        NotificationListView.as_view(),
        name='notification-list'
    ),

    path(
        'create/',
        NotificationCreateView.as_view(),
        name='notification-create'
    ),
    path(
        '<int:pk>/retry/',
        RetryNotificationView.as_view(),
        name='notification-retry'
    ),
    # path(
    #     'api/schema/',
    #     SpectacularAPIView.as_view(),
    #     name='schema',
    # ),

    # path(
    #     'api/docs/',
    #     SpectacularSwaggerView.as_view(
    #         url_name='schema'
    #     ),
    #     name='swagger-ui',
    # ),
    path(
        'health/',
        health_check,
        name='health-check'
    ),
]