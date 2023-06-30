# Description: Sitemap view
from django.shortcuts import render

def sitemap(request):
    return render(request, "sitemap.xml")