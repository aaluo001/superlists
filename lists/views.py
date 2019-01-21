from django.shortcuts import render
from django.http import HttpResponse


def homePage(vRequest):
  return HttpResponse('<html><title>To-Do lists</title></html>')


