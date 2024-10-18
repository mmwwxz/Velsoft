from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt


from .models import (
    Product,
    SoldProduct
)
from .forms import (
    ProductCreateForm,
    SoldProductForm,
    SoldProductUpdateForm,
    UserLoginForm,
    UserRegisterForm
)
from .filters import ProductFilter


def index_view(request):
    products = Product.objects.all().order_by('-id')[:8]
    sold_products = SoldProduct.objects.all().order_by('-id')[:4]

    return render(
        request=request,
        template_name='product/index.html',
        context={
            'products': products,
            'sold_products': sold_products,
        }
    )


def product_list_view(request):
    # Создаем экземпляр фильтра
    product_filter = ProductFilter(request.GET, queryset=Product.objects.all().order_by('-id'))

    # Получаем отфильтрованные продукты
    products = product_filter.qs

    if 'search' in request.GET:
        search_query = request.GET['search']
        products = products.filter(Q(title__iregex=search_query) | Q(description__iregex=search_query))

    # Пагинация
    paginator = Paginator(products, 16)  # 16 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/product_list.html', {
        'products': page_obj,
        'filter': product_filter,
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = SoldProductForm(request.POST)

        if form.is_valid():
            sold_product_quantity = form.cleaned_data['quantity']
            sold_product_total = form.cleaned_data['total_price']
            product_quantity = product.quantity

            if sold_product_quantity > product_quantity:
                messages.error(request, "Недостаточно товара на складе.")

            elif sold_product_total <= 0:
                messages.error(request, 'Сумма продажи не может быть меньше или равна 0')

            else:
                sold_product = form.save(commit=False)
                sold_product.product = product
                product.quantity -= sold_product_quantity
                product.save()
                sold_product.save()

                messages.success(request, "Операция успешно выполнена.")
                return redirect('index')

        else:
            messages.error(request, 'Повторите попытку, убедитесь, что поля заполнены в правильном формате.')

    else:
        form = SoldProductForm()

    return render(
        request=request,
        template_name='product/product_detail.html',
        context={
            'product': product,
            'form': form
        }
    )


@login_required(login_url='login')
def product_create_view(request):

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Операция успешно выполнена.")
            return redirect('index')
        else:
            messages.error(request, 'Повторите попытку, убедитесь, что поля заполнены в правильном формате.')
    form = ProductCreateForm()

    return render(
        request=request,
        template_name='product/product_create.html',
        context={
            'form': form
        }
    )


@login_required(login_url='login')
def product_report_list_view(request):
    sold_products = SoldProduct.objects.all().order_by('-id')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date', now().strftime('%Y-%m-%d'))

    if start_date:
        sold_products = sold_products.filter(sale_date__gte=start_date)

    if end_date:
        sold_products = sold_products.filter(sale_date__lte=end_date)

    # Вычисляем общую сумму продаж
    total_sold_price = sold_products.aggregate(total=Sum('total_price'))['total']

    # Вычисляем общую закупочную стоимость проданных товаров
    total_purchase_cost = sold_products.annotate(
        total_cost=F('product__purchase_price') * F('quantity')
    ).aggregate(total=Sum('total_cost'))['total']

    # Вычисляем чистую прибыль
    net_profit = total_sold_price - total_purchase_cost if total_sold_price and total_purchase_cost else 0

    context = {
        'sold_products': sold_products,
        'total_purchase_cost': total_purchase_cost,
        'total_sold_price': total_sold_price,
        'net_profit': net_profit,
        'request': request,  # Передаём объект запроса для доступа к параметрам GET
    }

    return render(
        request=request,
        template_name='product/report.html',
        context=context
    )


@login_required(login_url='login')
def sold_product_detail_view(request, pk):
    sold_product = get_object_or_404(SoldProduct, pk=pk)

    if request.method == 'POST':
        form = SoldProductUpdateForm(request.POST, instance=sold_product)

        if form.is_valid():
            form.save()
            messages.success(request, "Товар успешно изменен.")
            return redirect('sold_product_detail', sold_product.id)
        else:
            messages.error(request, 'Повторите попытку, убедитесь, что поля заполнены в правильном формате.')

    else:
        form = SoldProductUpdateForm(instance=sold_product)

    return render(
        request=request,
        template_name='product/sold_product_detail.html',
        context={
            'sold_product': sold_product,
            'form': form,
        }
    )


def user_login_views(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            user_password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=user_password
            )

            if user:
                login(request, user)
                messages.success(request, "Вы успешно авторизованы.")
                return redirect('index')
            messages.error(request, 'Неправильный логин или пароль.')

        messages.error(request, 'Повторите попытку, убедитесь, что поля заполнены в правильном формате.')
    else:
        form = UserLoginForm()

    return render(request, 'product/user_login.html', {'form': form})


@login_required(login_url='login')
def user_logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")

    return redirect('index')


def user_sign_up_view(request):
    # Права доступа
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('index')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались. Теперь вы можете войти в систему.')
            return redirect('index')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
        else:
            print(form.errors)
    form = UserRegisterForm()

    return render(request, 'product/user_sign_up.html', {'form': form})


@csrf_exempt
def custom_page_not_found_view(request, exception):
    return render(request, 'product/404.html', status=404)


@csrf_exempt
def custom_server_error_view(request):
    return render(request, 'product/500.html', status=500)
