from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.checks import check_user_model
from back.SelectionOptions.marketaction import marketaction
from datetime import *
from decimal import Decimal
from django.views.decorators.gzip import gzip_page

INPUT = 'input'
OUTPUT = 'output'

@gzip_page
def AuthorizedControls(request = HttpRequest):
    if request.user.is_authenticated:
        return render(request, "authorizedcontrols.html")

    return redirect('/admin')

@gzip_page
def Index(request = HttpRequest):
    return render(request, "index.html")

@gzip_page
def Portfolio(request = HttpRequest):
    if request.user.is_authenticated:
        return render(request, "portfolio.html")

    return redirect('/admin')
