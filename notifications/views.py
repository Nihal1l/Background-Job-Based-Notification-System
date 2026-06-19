from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .tasks import process_notification
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView


@api_view(['GET'])
def health_check(request):

    return Response({
        "status": "healthy"
    })

class NotificationCreateView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        notification = serializer.save(
            user=self.request.user
        )



class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

        status_param = self.request.query_params.get(
            'status'
        )

        if status_param:
            queryset = queryset.filter(
                status=status_param
            )

        return queryset




class RetryNotificationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            notification = Notification.objects.get(
                id=pk,
                user=request.user
            )

        except Notification.DoesNotExist:

            return Response(
                {
                    "error": "Notification not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent retrying successful notifications
        if notification.status == NotificationStatus.SENT:

            return Response(
                {
                    "error": (
                        "Cannot retry sent notification"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent retrying permanently failed notifications
        if (
            notification.status
            == NotificationStatus.PERMANENTLY_FAILED
        ):

            return Response(
                {
                    "error": (
                        "Notification permanently failed"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent infinite retries
        if notification.retry_count >= 3:

            notification.status = (
                NotificationStatus.PERMANENTLY_FAILED
            )

            notification.save()

            return Response(
                {
                    "error": "Retry limit exceeded"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reset status
        notification.status = NotificationStatus.PENDING
        notification.save()

        process_notification.delay(notification.id)

        return Response(
            {
                "message": (
                    "Notification retry queued"
                )
            },
            status=status.HTTP_200_OK
        ) 

        if notification.status == NotificationStatus.PROCESSING:

            return Response(
                {
                    "error": (
                        "Notification already processing"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )           
