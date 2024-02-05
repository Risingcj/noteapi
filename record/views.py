from django.core.paginator import Paginator
from django.db import models
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Record
from .serializer import RecordSerializer
from django.shortcuts import get_object_or_404


# @api_view(http_method_names=['GET'])
# def display_records(request: Request):
#     records = Record.objects.all()
#     if records:
#         serializer = RecordSerializer(records, many=True)
#         response = {'list of records': serializer.data}
#         return Response(data=response, status=status.HTTP_200_OK)
#     return Response(data='Error', status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET'])
def display_records(request):
    # Create a QuerySet of objects
    records = Record.objects.all()

    # Create a Paginator object with 5 items per page
    paginator = Paginator(records, 5)

    # Get the requested page number
    page_number = request.GET.get('page')

    # Get the Page object for the requested page number
    page_obj = paginator.get_page(page_number)

    # Serialize the Page object
    serializer = RecordSerializer(page_obj, many=True)

    # Create the response data
    response_data = {
        'list of records': serializer.data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'total_pages': paginator.num_pages,
        'current_page_number': page_obj.number,
    }

    # Return the response
    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def save_records(request: Request):
    print(request.data)
    serializer = RecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def display_record(request: Request, record_id: int):
    record = get_object_or_404(Record, pk=record_id)
    serializer = RecordSerializer(instance=record)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['PUT'])
def edit_record(request: Request, record_id: int):
    record = get_object_or_404(Record, pk=record_id)
    serializer = RecordSerializer(instance=record, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['DELETE'])
def delete_record(request: Request, record_id: int):
    record = get_object_or_404(Record, pk=record_id)
    record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(http_method_names=['GET'])
# def search_record(request: Request, record_word: str):
#     record = Record.objects.all()
#     if record_word in record:
#         serializer = RecordSerializer(record, many=True)
#         response = {'list of records': serializer.data}
#         return Response(data=response, status=status.HTTP_200_OK)
#     return (Response(data='Error', status=status.HTTP_404_NOT_FOUND)
#
#

@api_view(http_method_names=['GET'])
def search_record(request: Request):
    query = request.GET.get('q', '')
    if query:
        records = Record.objects.filter(models.Q(header__icontains=query))
    else:
        records = Record.objects.all()
    serializer = RecordSerializer(records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
