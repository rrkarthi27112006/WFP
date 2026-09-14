def notifications_processor(request):
    """Expose unread notification count and recent notifications to all templates."""
    if request.user.is_authenticated:
        from notifications.models import Notification
        qs = Notification.objects.filter(user=request.user)
        return {
            'nav_unread_count': qs.filter(is_read=False).count(),
            'nav_recent_notifications': qs[:6],
        }
    return {'nav_unread_count': 0, 'nav_recent_notifications': []}
