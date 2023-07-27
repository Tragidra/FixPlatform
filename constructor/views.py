import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from classes.Converter import DB
from .models import Users, Repair_packets, Orders, Orders_fields_values
from .serializers import *


@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        customers = Users.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(customers, 5)
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
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    try:
        customer = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersSerializer(customer, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsersSerializer(customer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def final_price(request):
    # data = json.loads(request.body)
    # order_id = data['order_id']
    # repair_packets_id = data['repair_packets_id']
    repair_packets_id = 1
    order_id = 2
    Converter = DB()
    price = Converter.queryset_to_values(Repair_packets.objects.filter(id=repair_packets_id).values('price'), 'price')
    square = Converter.queryset_to_values(Orders.objects.filter(id=order_id).values('square'), 'square')
    price = price * square
    print(Orders_fields_values.objects.filter(order_id=order_id).values())
    orders_fields_values = Converter.queryset_to_values(
        Orders_fields_values.objects.filter(order_id=order_id).values('value', 'size'))
    additional_price = 0
    for i in range(orders_fields_values):
        additional_price += orders_fields_values[i]['size'] * orders_fields_values[i]['value']
    price = price + additional_price
    return Response({'price': price})
