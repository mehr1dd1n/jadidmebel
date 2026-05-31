from main.models import Order


def dashboard_stats(request):
    if request.path.startswith('/dashboard/') and request.user.is_authenticated:
        return {'new_orders_count': Order.objects.filter(status='new').count()}
    return {'new_orders_count': 0}
