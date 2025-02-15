from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['dish_formset'] = DishFormSet(self.request.POST)
        else:
            context['dish_formset'] = DishFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        dish_formset = context['dish_formset']
        if dish_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.items = [dish_form.cleaned_data for dish_form in dish_formset if dish_form.cleaned_data]
            self.object.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class OrderUpdateView(UpdateView):
    """Edit entire order (table, dishes, status)"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()

        if self.request.method == 'POST':
            context['dish_formset'] = DishFormSet(self.request.POST)
        else:
            initial_data = order.items if order.items else []
            context['dish_formset'] = DishFormSet(initial=initial_data)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        dish_formset = context['dish_formset']
        if dish_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.items = [dish_form.cleaned_data for dish_form in dish_formset if dish_form.cleaned_data]
            self.object.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class OrderStatusUpdateView(UpdateView):
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
