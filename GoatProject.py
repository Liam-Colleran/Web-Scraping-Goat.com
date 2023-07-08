import requests
import json
import math
from contextlib import suppress


def search(query, page=1):
    url = f'https://ac.cnstrc.com/search/{query.replace(" ", "%20")}?c=ciojs-client-2.35.2&key=key_XT7bjdbvjgECO5d8&i=dd315c3b-ef56-4b02-bcb0-c565b44efd01&s=8&page={page}'
    print(f'Searching from: {url}')
    print(' ')
    print(f'Page {page}:')
    print(' ')
    html = requests.get(url=url)
    output = json.loads(html.text)
    shoelist = output['response']['results']
    
    return output, shoelist


def info_or_NA(container):
    try:
        result = container
    except KeyError:
        result = 'Data Not Found.'
    return result

# ^^^ https://stackoverflow.com/questions/54959693/avoiding-multiple-try-except-blocks-in-python 


def getinfo(shoelist, repeatamnt=19):
    
    for i in range(repeatamnt):
        try:
            shoelist[i]
        except IndexError:
            print('Number of shoes searched exceeds number of listings.')
            break
        
        with suppress(KeyError):
            name = info_or_NA(shoelist[i]['value'])
            image = info_or_NA(shoelist[i]['data']['image_url'])
            condition = info_or_NA(shoelist[i]['data']['product_condition'].replace('_', ' '))
            retailprice = info_or_NA(shoelist[i]['data']['retail_price_cents'] / 100)
            release = info_or_NA(shoelist[i]['data']['release_date_year'])
            
        # ^^^ https://stackoverflow.com/questions/574730/python-how-to-ignore-an-exception-and-proceed

        print('---------')
        print(f'Shoe #{i + 1}')
        print(f'Name: {name}')
        print(f'Image Link: {image}')
        print(f'Condition: {condition}')
        print(f'Released in: {release}')
        print(f'Retail Price: {retailprice}')
    print('---------')
    print(' ')


print('What would you like to search for?')
query = input('> ')
print(' ')

print('How many shoes do you want to search for?:')
repeat = int(input('> '))
print(' ')

pages = math.ceil(repeat/19) + 1
print(f'Loading {pages} pages...')

for i in range(1, pages):
    output, shoelist = search(query, i)
    if repeat > 19:
        getinfo(shoelist)
        repeat = repeat - 19
    else:
        getinfo(shoelist, repeat)
