from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, MessageViewSet, MediaUploadView, ReactionViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'media', MediaUploadView, basename='media')
router.register(r'reactions', ReactionViewSet, basename='reaction')

urlpatterns = [
    path('api/', include(router.urls)),
]