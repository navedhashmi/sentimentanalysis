from amazon_data import AmazonData
from a_product_analysis import Amazon_Analysis
import boto3
from botocore.exceptions import ClientError

## Put Product Search Term
amazon_record = AmazonData(input("What you want to search? : "))

## Get the URL of the search term with products related to it
url = amazon_record.a_get_url()
amazon_raw_list = amazon_record.a_soupify(url)
product_list = []
review_analysis_list = []

for number_of_products in range(0, len(amazon_raw_list)):
    product_list.append(amazon_record.a_product_record(amazon_raw_list, number_of_products).copy())

amazon_record.a_data_csv(product_list)

print(f"\nNo. of Product = {len(product_list)}\n")

while True:
    for item in range(0, len(product_list)):
        print(f"{item + 1}. {product_list[item]['name']}")

    product_to_analyze = int(input("\n__________________________________________________________________\nPlease select a product to analyze it's reviews :")) - 1
    product_check = input(f"\nCheck if it's the product you selected \n {product_list[product_to_analyze]['url']} \n 'Yes' to continue, 'No' to reselect :")
    if product_check.lower() == "yes":
        a_analysis = Amazon_Analysis(product_list[product_to_analyze]['url'])
        product_page_review_list = a_analysis.analysis_soup()
        #print(product_page_review_list)

        comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')
        print(product_page_review_list)
        sentiment_batch = comprehend.batch_detect_sentiment(TextList=product_page_review_list, LanguageCode='en')
        for number_of_review in range(0, len(sentiment_batch['ResultList'])):
            #print(sentiment_batch['ResultList'][number_of_review])
            review_analysis_list.append(sentiment_batch['ResultList'][number_of_review]['Sentiment'])
        print(review_analysis_list)
        re_run = input("Want to re-run with different Product? 'Yes' to continue, 'No' to reselect :")
        if re_run.lower() == "yes":
            continue
        else:
            break
    else:
        continue
