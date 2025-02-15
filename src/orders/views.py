from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView

from .models import Order
from .forms import OrderForm, DishFormSet


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """Filter orders by table number or status (if specified in the request)"""
        queryset = Order.objects.all().order_by('-id')
        table_number = self.request.GET.get('table_number')
        status = self.request.GET.get('status')
        if table_number:
            queryset = queryset.filter(table_number=table_number)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        return context


class OrderCreateView(View):
    template_name = "orders/order_form.html"

    def get(self, request, *args, **kwargs):
        order_form = OrderForm()
        dish_formset = DishFormSet()
        return render(request, self.template_name, {
            'order_form': order_form,
            'dish_formset': dish_formset,
        })

    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        dish_formset = DishFormSet(request.POST)
        if order_form.is_valid() and dish_formset.is_valid():
            order = order_form.save(commit=False)
            items = []
            total_price = 0
            for form in dish_formset:
                name = form.cleaned_data.get("name")
                price = form.cleaned_data.get("price")
                quantity = form.cleaned_data.get("quantity")
                # Check empty forms
                if name and price and quantity:
                    items.append({
                        "name": name,
                        "price": float(price),
                        "quantity": quantity
                    })
                    total_price += float(price) * quantity
            order.items = items
            order.total_price = total_price
            order.save()
            return redirect('order_list')
        return render(request, self.template_name, {
            'order_form': order_form,
            'dish_formset': dish_formset,
        })


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')


class OrderRevenueView(View):
    def get(self, request):
        total_revenue = Order.get_total_revenue()
        return render(request, 'orders/order_revenue.html', {'total_revenue': total_revenue})
