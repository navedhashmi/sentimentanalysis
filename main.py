from selenium import webdriver
from bs4 import BeautifulSoup
import csv



def get_url(search_term):
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url += '&page={}'
    return url


def product_record(item):
    product_dic.clear()
    product = results[item]
    a_tag = product.h2.a.text  # Name of product
    product_dic['name'] = a_tag

    url = 'https://www.amazon.in' + product.h2.a.get('href')  # URL of product
    product_dic['url'] = url


    try:
        price = product.select_one('.a-price .a-offscreen').text  # Price of product
        product_dic['price'] = float(price[1:].replace(',', ''))
    except AttributeError:
        product_dic['price'] = "Product Not Available"

    try:
        rating = product.i.text  # Rating of product
        product_dic['rating'] = rating[0:3]

        review = product.select_one('.a-size-base').text  # No. of review
        product_dic['review'] = review.replace(',', '')
    except AttributeError:
        product_dic['rating'] = "No Rating"
        product_dic['review'] = "No Review"
    return product_dic


driver = webdriver.Chrome()
url = get_url(input("What you want to search? : "))
Stop = False
product_dic = {}
product_list = []

for x in range(1, 21):
    if Stop == True:
        break
    driver.get(url.format(x))
    #Initializing BeautifulSoup // Extract the collection
    soup = BeautifulSoup(driver.page_source, "html5lib")
    #page = soup.select_one(selector='.rush-component .a-section span').text
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    #Creating Record Dictioniary
    for number_of_products in range(0, len(results)):
        record = product_record(number_of_products).copy()
        if record:
            product_list.append(record)
        else:
            Stop = True
            break

headers = ['name', 'url', 'price', 'rating', 'review']

with open("product_data.csv", 'w', encoding="utf-8", newline="") as csv_file:
    writer = csv.DictWriter(csv_file,fieldnames=headers)
    writer.writeheader()
    for data in product_list:
        writer.writerow(data)

print(product_list)
driver.close()
