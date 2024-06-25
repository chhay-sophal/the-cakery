from django.shortcuts import render, render

def home_page(request): 
    return render(request, "base/base.html")