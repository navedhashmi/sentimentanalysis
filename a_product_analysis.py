from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Amazon_Analysis:

    def __init__(self, product_url):
        self.html_session_amazon = HTMLSession()
        self.product_url = product_url
        self.review_txt_data_list = []
        # Initializing BeautifulSoup // Extract the collection

    def analysis_soup(self):
        product_page = self.html_session_amazon.get(self.product_url)
        product_page.html.render(sleep=1)
        product_soup = BeautifulSoup(product_page.html.html, "html.parser")
        review_url = str(product_soup.find('div', {'id': 'reviews-medley-footer'}).find('a')['href'])
        product_review_url = 'https://www.amazon.in' + review_url
        product_reviews = self.html_session_amazon.get(product_review_url)
        product_reviews.html.render(sleep=1)
        review_soup = BeautifulSoup(product_reviews.html.html, "html.parser")
        #.find('span', {'data-hook': 'review-body'}).find('span').text
        review_data = review_soup.find_all('div', {'class': 'a-section review aok-relative'})
        for number_of_review in range(0, len(review_data)):
            review_comment = review_data[number_of_review].find('span', {'data-hook': 'review-body'}).find('span').text
            self.review_txt_data_list.append(review_comment.strip())
        return self.review_txt_data_list

