from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from .models import Search

BASE_CRAIGSLIST_URL = 'https://toronto.craigslist.org/search/sss?query={}'
# Create your views here.

def home(request):
    return render(request, template_name='base.html')


def new_search(request):

    search = request.POST['search']
    Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    # print(data)
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price,))

    context = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', context)