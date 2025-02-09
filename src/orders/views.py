from django.views.generic import ListView

from .models import Order


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """Filter orders by table number or status (if specified in the request)"""
        queryset = Order.objects.all()
        table_number = self.request.GET.get('table_number')
        status = self.request.GET.get('status')

        if table_number:
            queryset = queryset.filter(table_number=table_number)
        if status:
            queryset = queryset.filter(status=status)

        return queryset
