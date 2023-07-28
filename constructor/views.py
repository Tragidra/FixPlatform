import json
import random
import string
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Users, Repair_packets, Orders, Orders_fields_values, Checks_fields
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from classes.Converter import DB
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Converter = DB()


@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        users = Users.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = UsersSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        request.data._mutable = True
        data = request.data
        data['password'] = Converter.data_to_hash(data['password'])
        request.data._mutable = False
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, id):
    try:
        user = Users.objects.get(pk=id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersSerializer(user, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_user = user
        data = request.data
        if 'name' in data.keys():
            user.name = data['name']
        if 'password' in data.keys():
            user.password = data['password']
        if 'passport' in data.keys():
            user.passport = data['passport']
        if 'phone' in data.keys():
            user.phone = data['phone']
        if 'email' in data.keys():
            user.email = data['email']
        if 'address' in data.keys():
            user.address = data['address']
        if 'role_id' in data.keys():
            user.role_id = data['role_id']
        if 'referral_id' in data.keys():
            user.referral_id = data['role_id']
        if 'bonus' in data.keys():
            user.role_id = data['role_id']
        if user != old_user:
            user.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        user.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def final_price(request):
    # data = json.loads(request.body)
    # order_id = data['order_id']
    # repair_packets_id = data['repair_packets_id']
    repair_packets_id = 1
    order_id = 1
    price = Converter.queryset_to_values(Repair_packets.objects.filter(id=repair_packets_id).values('price'), 'price')
    square = Converter.queryset_to_values(Orders.objects.filter(id=order_id).values('square'), 'square')
    price = price * square
    print(price)
    orders_fields_values = Converter.queryset_to_values(
        Orders_fields_values.objects.filter(order_id=order_id).values('value', 'size'))
    additional_price = 0
    for i in range(len(orders_fields_values)):
        additional_price += int(orders_fields_values[i]['size']) * int(orders_fields_values[i]['value'])
    price = price + additional_price
    return Response({'price': price})


@api_view(['GET', 'POST'])
def orders_interaction(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        customers = Orders.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(customers, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = OrdersSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_interraction(request, id):
    try:
        customer = Orders.objects.get(id=id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrdersSerializer(customer, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrdersSerializer(customer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def authorize(request):
    data = request.data
    password = Converter.data_to_hash(data['password'])
    user = Users.objects.filter(email=data['email'], password=password)
    if user is not None:
        try:
            letters_and_digits = string.ascii_letters + string.digits
            rand_string = ''.join(random.sample(letters_and_digits, 8))
            msg = MIMEMultipart()
            msg['From'] = 'testforauthorization@gmail.com'
            msg['To'] = 'trutovictrut@@gmail.com'
            msg['Subject'] = 'Авторизация на платформе FixP'
            message = 'Ваш код подтверждения - ' + rand_string
            msg.attach(MIMEText(message))

            mailserver = smtplib.SMTP('smtp.gmail.com', 587)
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.ehlo()
            mailserver.login('testforauthorization@gmail.com', 'd043j24p')
            mailserver.sendmail('testforauthorization@gmail.com', 'trutovictrut@@gmail.com', msg.as_string())
            mailserver.quit()
            return Response({'status': 'ok'})
        except:
            return Response(
                {'status': 'error', 'message': 'Что-то пошло не так, пожалуйста, проверьте указанную вами почту'})
    else:
        return Response({'status': 'error', 'message': 'Пользователь с введёнными вами данными не найден'})

@api_view(['GET', 'POST'])
def check_fields_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        checks_fields = Checks_fields.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(checks_fields, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Checks_fieldsSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Checks_fieldsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def check_fields_detail(request, id):
    try:
        checks_fields = Checks_fields.objects.get(pk=id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Checks_fieldsSerializer(checks_fields, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_checks_fields = checks_fields
        data = request.data
        if 'name' in data.keys():
            checks_fields.name = data['name']
        if 'price' in data.keys():
            checks_fields.password = data['password']
        if checks_fields != old_checks_fields:
            checks_fields.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        checks_fields.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        checks_fields.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view([''])
