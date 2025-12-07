from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.models import User

from .forms import ClientRegisterForm
from core.models import Client, Staff, Bouquet, BouquetPosition, Flower, Storage, Orders, OrderPosition
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from datetime import date
from django.contrib import messages



def register_view(request):
    if request.method == "POST":
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email_client"]
            password = form.cleaned_data["password_client"]

            # 1) Создаём Django-пользователя (для login/logout)
            user = User.objects.create_user(
                username=email,          # логин = email
                email=email,
                password=password
            )

            # 2) Создаём запись в таблице client
            Client.objects.create(
                last_name_client=form.cleaned_data["last_name_client"],
                first_name_client=form.cleaned_data["first_name_client"],
                middle_name_client=form.cleaned_data["middle_name_client"],
                phone_number_client=form.cleaned_data["phone_number_client"],
                password_client=password,          # при желании можно шифровать отдельно
                birth_date=form.cleaned_data["birth_date"],
                email_client=email
            )

            # 3) Авторизуем и отправляем в профиль
            login(request, user)
            return redirect("menu")
    else:
        form = ClientRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("username")  # поле name="username" в стандартной форме
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("menu")
        else:
            error = "Неверный email или пароль."
    form = AuthenticationForm(request, data=request.POST or None)
    return render(request, "accounts/login.html", {"form": form, "error": error})

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def menu_view(request):
    email = request.user.email
    is_client = Client.objects.filter(email_client=email).exists()
    is_staff  = Staff.objects.filter(email_staff=email).exists()
    return render(request, "accounts/menu.html", {
        "is_client": is_client,
        "is_staff": is_staff,
    })

@login_required
def profile_view(request):
    email = request.user.email

    is_client = Client.objects.filter(email_client=email).exists()
    is_staff  = Staff.objects.filter(email_staff=email).exists()

    if is_client:
        role = "Клиент"
        profile_obj = Client.objects.get(email_client=email)
    elif is_staff:
        role = "Сотрудник"
        profile_obj = Staff.objects.get(email_staff=email)
    else:
        role = "Неопределено"
        profile_obj = None

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # чтобы не разлогинило после смены пароля
            update_session_auth_hash(request, user)
            msg = "Пароль успешно изменён."
        else:
            msg = "Ошибка при смене пароля."
    else:
        form = PasswordChangeForm(request.user)
        msg = None

    return render(request, "accounts/profile.html", {
        "user": request.user,
        "role": role,
        "profile_obj": profile_obj,
        "is_client": is_client,
        "is_staff": is_staff,
        "form": form,
        "msg": msg,
    })

@login_required
def flowers_list_view(request):
    bouquets = Bouquet.objects.all().order_by("name")
    return render(request, "accounts/flowers_list.html", {"bouquets": bouquets})


@login_required
def flower_detail_view(request, bouquet_id):
    bouquet = Bouquet.objects.get(id_bouquet=bouquet_id)
    positions = BouquetPosition.objects.filter(id_bouquet=bouquet_id)
    # подгружаем цветы
    flowers = []
    for pos in positions:
        flower = Flower.objects.get(id_flower=pos.id_flower)
        flowers.append({
            "name": flower.name_flower,
            "quantity": pos.quantity,
        })
    return render(request, "accounts/flower_detail.html", {
        "bouquet": bouquet,
        "flowers": flowers,
    })


def _get_cart(session):
    return session.setdefault("cart", {})  # {bouquet_id: quantity}


@login_required
@require_POST
def cart_add_view(request, bouquet_id):
    cart = _get_cart(request.session)
    key = str(bouquet_id)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True
    return redirect("cart")


@login_required
def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")

    for key, qty in cart.items():
        b = Bouquet.objects.get(id_bouquet=int(key))
        subtotal = b.price * qty
        total += subtotal
        items.append({
            "bouquet": b,
            "quantity": qty,
            "subtotal": subtotal,
        })

    return render(request, "accounts/cart.html", {
        "items": items,
        "total": total,
    })

@login_required
@require_POST
def cart_clear_view(request):
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("cart")

@login_required
@require_POST
def cart_checkout_view(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Корзина пуста, оформлять нечего.")
        return redirect("cart")

    # 1. Находим клиента по email текущего пользователя
    try:
        client = Client.objects.get(email_client=request.user.email)
    except Client.DoesNotExist:
        messages.error(request, "Для оформления заказа нужно быть клиентом.")
        return redirect("cart")

    # 2. Считаем итоговую сумму
    total = Decimal("0.00")
    for key, qty in cart.items():
        b = Bouquet.objects.get(id_bouquet=int(key))
        total += b.price * qty

    # 3. Создаём заказ (id_staff пока не указываем, если в БД разрешён NULL)
    order = Orders.objects.create(
        id_client=client.id_client,
        id_shop=1,
        total_amount=total,
        status_order="оформлен",
        payment_type="наличные",
        order_date=date.today(),
    )

    # 4. Создаём позиции заказа
    for key, qty in cart.items():
        b = Bouquet.objects.get(id_bouquet=int(key))
        OrderPosition.objects.create(
            id_bouquet=b.id_bouquet,
            id_order=order.id_order,
            quantity=qty,
        )

    # 5. Списание со склада (по только что созданным позициям)
    positions = OrderPosition.objects.filter(id_order=order.id_order)
    for pos in positions:
        bouquet_positions = BouquetPosition.objects.filter(id_bouquet=pos.id_bouquet)
        for bp in bouquet_positions:
            needed = pos.quantity * bp.quantity
            storage_item = Storage.objects.get(id_flower=bp.id_flower)
            storage_item.quantity_flower -= needed
            storage_item.save(update_fields=["quantity_flower"])

    # 6. Очищаем корзину
    request.session["cart"] = {}
    request.session.modified = True

    messages.success(request, f"Заказ №{order.id_order} успешно оформлен. Напишите «оплатить».")
    return redirect("cart")


@login_required
def my_orders_view(request):
    # определяем клиента по email авторизованного пользователя
    try:
        client = Client.objects.get(email_client=request.user.email)
    except Client.DoesNotExist:
        # если это не клиент (например, сотрудник), можно показать пустой список
        orders = []
    else:
        orders = Orders.objects.filter(id_client=client.id_client).order_by("-order_date", "-id_order")

    # собираем краткую информацию по каждому заказу
    data = []
    for order in orders:
        positions = OrderPosition.objects.filter(id_order=order.id_order)
        items = []
        for pos in positions:
            b = Bouquet.objects.get(id_bouquet=pos.id_bouquet)
            items.append({
                "bouquet_name": b.name,
                "quantity": pos.quantity,
            })
        data.append({
            "order": order,
            "items": items,
        })

    return render(request, "accounts/my_orders.html", {"orders_data": data})

@login_required
def staff_free_orders_view(request):
    # проверяем, что это сотрудник
    try:
        staff = Staff.objects.get(email_staff=request.user.email)
    except Staff.DoesNotExist:
        return redirect("menu")

    # заказы без назначенного сотрудника
    orders = Orders.objects.filter(id_staff__isnull=True).order_by("-order_date", "-id_order")

    data = []
    for order in orders:
        positions = OrderPosition.objects.filter(id_order=order.id_order)
        items = []
        for pos in positions:
            b = Bouquet.objects.get(id_bouquet=pos.id_bouquet)
            items.append(f"{b.name} — {pos.quantity} шт.")
        data.append({"order": order, "items": items})

    return render(request, "accounts/staff_free_orders.html", {
        "orders_data": data,
        "staff": staff,
    })


@login_required
@require_POST
def staff_take_order_view(request, order_id):
    try:
        staff = Staff.objects.get(email_staff=request.user.email)
    except Staff.DoesNotExist:
        return redirect("menu")

    order = Orders.objects.get(id_order=order_id)
    if order.id_staff is None:
        order.id_staff = staff.id_staff
        order.status_order = "в обработке"
        order.save(update_fields=["id_staff", "status_order"])

    return redirect("staff_free_orders")

@login_required
def staff_my_orders_view(request):
    try:
        staff = Staff.objects.get(email_staff=request.user.email)
    except Staff.DoesNotExist:
        return redirect("menu")

    orders = Orders.objects.filter(id_staff=staff.id_staff).order_by("-order_date", "-id_order")

    data = []
    for order in orders:
        positions = OrderPosition.objects.filter(id_order=order.id_order)
        items = []
        for pos in positions:
            b = Bouquet.objects.get(id_bouquet=pos.id_bouquet)
            items.append(f"{b.name} — {pos.quantity} шт.")
        data.append({"order": order, "items": items})

    # допустимые статусы (из твоей валидации: оформлен, в обработке, собран, завершен)
    statuses = ["оформлен", "в обработке", "собран", "завершен"]

    return render(request, "accounts/staff_my_orders.html", {
        "orders_data": data,
        "statuses": statuses,
    })


@login_required
@require_POST
def staff_update_order_status_view(request, order_id):
    try:
        staff = Staff.objects.get(email_staff=request.user.email)
    except Staff.DoesNotExist:
        return redirect("menu")

    order = Orders.objects.get(id_order=order_id)

    # проверяем, что этот заказ реально принадлежит текущему сотруднику
    if order.id_staff != staff.id_staff:
        return redirect("staff_my_orders")

    new_status = request.POST.get("status_order")
    if new_status:
        order.status_order = new_status
        order.save(update_fields=["status_order"])

    return redirect("staff_my_orders")