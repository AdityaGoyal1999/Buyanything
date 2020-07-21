from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests

BASE_CRAIGSLIST_URL = 'https://toronto.craigslist.org/search/sss?query={}'
# Create your views here.

def home(request):
    return render(request, template_name='base.html')


def new_search(request):

    search = request.POST['search']
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    print(data)
    context = {
        'search': search,
    }

    return render(request, 'my_app/new_search.html', context)