from selenium import webdriver
from bs4 import BeautifulSoup
import csv


class AmazonData:

    def __init__(self, search_term):
        self.amazon_temp_product_dic = {}
        self.amazon_product_list = []
        self.search_term = search_term

    def a_get_url(self):
        template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_2'
        search_term = self.search_term.replace(' ', '+')
        url = template.format(search_term)
        url += '&page={}'
        return url

    def a_soupify(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        # Initializing BeautifulSoup // Extract the collection
        soup = BeautifulSoup(driver.page_source, "html5lib")
        return soup.find_all('div', {'data-component-type': 's-search-result'})

    def a_product_record(self, raw_list, product_no):
        self.amazon_temp_product_dic.clear()
        result = raw_list
        product = result[product_no]
        a_tag = product.h2.a.text  # Name of product
        self.amazon_temp_product_dic['name'] = a_tag

        url = 'https://www.amazon.in' + product.h2.a.get('href')  # URL of product
        self.amazon_temp_product_dic['url'] = url

        try:
            price = product.select_one('.a-price .a-offscreen').text  # Price of product
            self.amazon_temp_product_dic['price'] = price[1:].replace(',', '')
        except AttributeError:
            self.amazon_temp_product_dic['price'] = "Product Not Available"

        try:
            rating = product.i.text  # Rating of product
            self.amazon_temp_product_dic['rating'] = rating[0:3]

            review = product.select_one('.a-size-base').text  # No. of review
            self.amazon_temp_product_dic['review'] = review.replace(',', '')
        except AttributeError:
            self.amazon_temp_product_dic['rating'] = "No Rating"
            self.amazon_temp_product_dic['review'] = "No Review"
        return self.amazon_temp_product_dic

    def a_data_csv(self, product_list):
        headers = ['name', 'url', 'price', 'rating', 'review']

        with open("product_data.csv", 'w', encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            for data in product_list:
                writer.writerow(data)
