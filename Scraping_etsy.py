import requests
from bs4 import BeautifulSoup
import csv
import os
import re

def clean_filename(filename):
    # Remove characters not allowed in filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def scrape_etsy_shop1(shop_url):
    print("\n Started Scraping data. . .")
    listing_urls = []
    response = requests.get(shop_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('a', class_='listing-link')
    for listing in listings:
        href = listing.get('href')
        if href:
            listing_urls.append(href)
    
    # Extract shop name from URL
    shop_name = shop_url.split('/')[-1].split('?')[0]
    # Clean the shop name to remove invalid characters for filenames
    csv_file = f"{clean_filename(shop_name)}_products.csv"
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['TITLE', 'DESCRIPTION', 'PRICE', 'CURRENCY_CODE','IMAGE1', 'IMAGE2', 'IMAGE3', 'IMAGE4', 'IMAGE5', 'IMAGE6', 'IMAGE7', 'IMAGE8', 
                    'IMAGE9', 'IMAGE10']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if the file is newly created
        if os.stat(csv_file).st_size == 0:
            writer.writeheader()

        # Loop through all pages in the shop
        page_num = 1
        while True:
            page_url = f"{shop_url}&page={page_num}" if '?' in shop_url else f"{shop_url}?page={page_num}"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            products = soup.find_all('div', class_='v2-listing-card')
            if not products:
                break  # No more products found, exit the loop

            for product in products:
                product_title = product.find('h3').text.strip()
                description_element = product.find('p', class_='text-gray')
                description = description_element.text.strip() if description_element else ""
                price_element = product.find('span', class_='currency-value')
                price = price_element.text.strip() if price_element else ""
                currency_code = "USD" 

                writer.writerow({'TITLE': product_title,
                                        'DESCRIPTION': description,
                                        'PRICE': price,
                                        'CURRENCY_CODE': currency_code,
                                        })
                for i in range (1,11):
                    try:
                        writer.writerow({
                                        f'IMAGE{i}': listing_urls[i-1] 
                                        })
                    except:
                        writer.writerow({
                                        f'IMAGE{i}': "" 
                                        })
            
            page_num += 1
            print("\nScraping Complete!")


# Provided shop URLs
shop_urls = [
    'https://www.etsy.com/shop/Bestgemdiamond',
    'https://www.etsy.com/shop/VintageafricancraArt?ref=simple-shop-header-name&listing_id=1020593544',
    'https://www.etsy.com/shop/WaKiwi?ref=simple-shop-header-name&listing_id=872846819',
    'https://www.etsy.com/shop/ZawadiGiftBeadke?ref=l2-about-shopname',
    'https://www.etsy.com/shop/BuyNowExpressLLC?ref=l2-about-shopname§ion_id=44298905'
]

while True:
    web = input("""\nEnter 0 to exit:
                1 if you want CVS of 'Bestgemdiamond'
                2 if you want CVS of 'VintageafricancraArt'
                3 if you want CVS of 'WaKiwi'
                4 if you want CVS of 'ZawadiGiftBeadke'
                5 if you want CVS of 'BuyNowExpressLLC'
                OR enter the Url :""")
    
    if web=="0":
        break
    
    elif web=="1":
        scrape_etsy_shop1('https://www.etsy.com/shop/Bestgemdiamond')
    
    elif web=="2":
        scrape_etsy_shop1('https://www.etsy.com/shop/VintageafricancraArt?ref=simple-shop-header-name&listing_id=1020593544')
    
    elif web=="3":
        scrape_etsy_shop1('https://www.etsy.com/shop/WaKiwi?ref=simple-shop-header-name&listing_id=872846819')
    
    elif web=="4":
        scrape_etsy_shop1('https://www.etsy.com/shop/ZawadiGiftBeadke?ref=l2-about-shopname')
    
    elif web=="5":
        scrape_etsy_shop1('https://www.etsy.com/shop/BuyNowExpressLLC?ref=l2-about-shopname§ion_id=44298905')
    
    else:
        try:
            scrape_etsy_shop1(web)
        except:
            print("\nSorry Invalid URL.")