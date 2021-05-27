from django.shortcuts import render
from celery import shared_task


@shared_task
def hello():
    print("Hello there!")
# Create your views here.
