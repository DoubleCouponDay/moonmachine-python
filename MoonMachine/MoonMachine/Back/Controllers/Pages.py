from django.http.request import HttpRequest
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.checks import check_user_model
from Back.SelectionOptions.MarketAction import MarketAction
from datetime import *
from decimal import Decimal
from django.views.decorators.gzip import gzip_page

INPUT = 'input'
OUTPUT = 'output'

@gzip_page
def AuthorizedControls(request = HttpRequest):
    if request.user.is_authenticated:
        return render(request, "authorizedcontrols.html")

    else:
        return redirect('/admin')

    return response

@gzip_page
def Index(request = HttpRequest):
    return render(request, "index.html")

@gzip_page
def Portfolio(request = HttpRequest):
    if request.user.is_authenticated:
        return render(request, "portfolio.html")

    else:
        return redirect('/admin')
