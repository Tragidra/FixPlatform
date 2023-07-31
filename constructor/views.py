import json
import random
import string
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Users, Repair_packets, Orders, Orders_fields_values, Checks_fields, Customers_payments, \
    Orders_work_stages, Orders_checks_fields_values
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
            user.referral_id = data['referral_id']
        # if 'bonus' in data.keys():
        #     user.role_id = data['bonus']
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
    orders_checks_fields_values = Converter.queryset_to_values(
        Orders_checks_fields_values.objects.filter(order_id=order_id).values('value', 'size'))
    additional_price = 0
    for i in range(len(orders_checks_fields_values)):
        additional_price += int(orders_checks_fields_values[i]['size']) * int(orders_checks_fields_values[i]['value'])
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
            user_id = Converter.queryset_to_values(Users.objects.filter(id=request.data['user_id']).values('id'), 'id')
            user_referral_owner = Users.objects.get(id=user_id)
            user_referral_owner.bonus = user_referral_owner.bonus + (float(request.data['square']) * 1000)
            user_referral_owner.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_interraction(request, id):
    try:
        orders = Orders.objects.get(id=id)
    except Orders.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrdersSerializer(orders, context={'request': request})
        return Response(serializer.data)


    elif request.method == 'PUT':

        old_orders = orders

        data = request.data

        if 'user_id' in data.keys():
            orders.user_id = data['user_id']

        if 'tyoe' in data.keys():
            orders.tyoe = data['type']

        if 'address' in data.keys():
            orders.address = data['address']

        if 'square' in data.keys():
            orders.square = data['square']

        if 'packet_id' in data.keys():
            orders.packet_id = data['packet_id']

        if 'numbers_rooms' in data.keys():
            orders.numbers_rooms = data['numbers_rooms']

        if 'numbers_doors' in data.keys():
            orders.numbers_doors = data['numbers_doors']

        if 'numbers_toilets' in data.keys():
            orders.numbers_toilets = data['numbers_toilets']

        if orders != old_orders:
            orders.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")

        orders.save()

        return Response({'status': 'ok'})

    elif request.method == 'DELETE':
        orders.delete()
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

        serializer = Checks_fields_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Checks_fields_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def check_fields_detail(request, id):
    try:
        checks_fields = Checks_fields.objects.get(pk=id)
    except Checks_fields.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Checks_fields_Serializer(checks_fields, context={'request': request})
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


@api_view(['GET', 'POST'])
def payments_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        customers_payments = Customers_payments.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(customers_payments, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Customers_payments_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Customers_payments_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def payments_details(request, id):
    try:
        customers_payments = Customers_payments.objects.get(pk=id)
    except Customers_payments.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Customers_payments_Serializer(customers_payments, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_customers_payments = customers_payments
        data = request.data
        if 'user_id' in data.keys():
            customers_payments.user_id = data['user_id']
        if 'order_id' in data.keys():
            customers_payments.order_id = data['order_id']
        if 'sum' in data.keys():
            customers_payments.sum = data['sum']
        if 'status' in data.keys():
            customers_payments.status = data['status']
        if 'number' in data.keys():
            customers_payments.number = data['number']
        if customers_payments != old_customers_payments:
            customers_payments.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        customers_payments.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        customers_payments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def work_stages_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        work_stages = Work_stages.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(work_stages, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Work_stages_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Work_stages_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def work_stages_details(request, id):
    try:
        work_stages = Work_stages.objects.get(pk=id)
    except Work_stages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Work_stages_Serializer(work_stages, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_work_stages = work_stages
        data = request.data
        if 'text' in data.keys():
            work_stages.text = data['text']
        if work_stages != old_work_stages:
            work_stages.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        work_stages.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        work_stages.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) @ api_view(['GET', 'POST'])


@api_view(['GET', 'POST'])
def orders_work_stages_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        orders_work_stages = Orders_work_stages.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(orders_work_stages, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Orders_work_stages_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Orders_work_stages_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def orders_work_stages_details(request, id):
    try:
        orders_work_stages = Orders_work_stages.objects.get(pk=id)
    except Orders_work_stages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Orders_work_stages_Serializer(orders_work_stages, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_orders_work_stages = orders_work_stages
        data = request.data
        if 'work_stages_id' in data.keys():
            orders_work_stages.work_stages_id = data['work_stages_id']
        if 'order_id' in data.keys():
            orders_work_stages.order_id = data['order_id']
        if 'status' in data.keys():
            orders_work_stages.status = data['status']
        if orders_work_stages != old_orders_work_stages:
            orders_work_stages.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        orders_work_stages.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        orders_work_stages.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_qr(request):  # При создании ссылки на переход добавить в хедер почту и имя
    data = request.data
    Converter.create_qr(data['name'], data['email'])
    return Response({'status': 'ok'})


@api_view(['GET', 'POST'])
def chats_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        chats = Chats.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(chats, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Chats_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Chats_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def chats_details(request, id):
    try:
        chats = Chats.objects.get(pk=id)
    except Chats.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Chats_Serializer(chats, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_chats = chats
        data = request.data
        if 'client_id' in data.keys():
            chats.client_id = data['client_id']
        if 'manager_id' in data.keys():
            chats.manager_id = data['manager_id']
        if 'chat_texts_id' in data.keys():
            chats.chat_texts_id = data['chat_texts_id']
        if chats != old_chats:
            chats.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        chats.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        chats.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def chat_texts_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        chat_texts = Chat_texts.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(chat_texts, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Chat_texts_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Chat_texts_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def chat_texts_details(request, id):
    try:
        chat_texts = Chat_texts.objects.get(pk=id)
    except Chat_texts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Chat_texts_Serializer(chat_texts, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_chat_texts = chat_texts
        data = request.data
        if 'chat_id' in data.keys():
            chat_texts.chat_id = data['chat_id']
        if 'text' in data.keys():
            chat_texts.text = data['text']
        if 'autor' in data.keys():
            chat_texts.autor = data['autor']
        if chat_texts != old_chat_texts:
            chat_texts.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        chat_texts.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        chat_texts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''Непонятно, как проводить верификацию, плэтому пока ограничусь базовыми методами'''

@api_view(['GET', 'POST'])
def passports_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        passports = Passports.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(passports, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Passports_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Passports_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def passports_details(request, id):
    try:
        passports = Passports.objects.get(pk=id)
    except Passports.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Passports_Serializer(passports, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_passports = passports
        data = request.data
        if 'series' in data.keys():
            passports.series = data['series']
        if 'number' in data.keys():
            passports.number = data['number']
        if 'user_id' in data.keys():
            passports.user_id = data['user_id']
        if 'date_of_birth' in data.keys():
            passports.date_of_birth = data['date_of_birth']
        if 'registration_place' in data.keys():
            passports.registration_place = data['registration_place']
        if passports != old_passports:
            passports.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        passports.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        passports.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''Получение рефов и прибыли с них для юзера, пока не нужно'''
# @api_view(['POST'])
# def get_referrals(request):
#     data = request.data
#     user_id = data['user_id']
#     profit = Converter.queryset_to_values(Users.objects.filter(id=user_id).values('bonus'), 'bonus')
#     profit = Users.objects.filter(referral_id=user_id).all()
#     for i in range(len(profit))

'''Работа с файлами, сделано до ТЗ, поэтому после его получения придётся переписывать большую часть, так как сейчас
даже нет определённости по поводу хранения файлов'''

@api_view(['GET', 'POST'])
def files_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        files = Files.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(files, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = Files_Serializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/customers/?page=' + str(nextPage),
                         'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        data = request.data
        serializer = Files_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def passports_details(request, id):
    try:
        files = Files.objects.get(pk=id)
    except Files.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Files_Serializer(files, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        old_files = files
        data = request.data
        if 'order_id' in data.keys():
            files.order_id = data['order_id']
        if 'user_id' in data.keys():
            files.user_id = data['user_id']
        if 'path' in data.keys():
            files.path = data['path']
        if 'comment' in data.keys():
            files.comment = data['comment']
        if 'orders_work_stages' in data.keys():
            files.orders_work_stages = data['orders_work_stages']
        if files != old_files:
            files.updated_at = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        files.save()
        return Response({'status': 'ok'})


    elif request.method == 'DELETE':
        files.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
