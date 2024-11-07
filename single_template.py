# SECOND  IMAGE       yaxis= 16.6            xaxis=1.85
# FIRST PRICE         yaxis= 8               rect_width=200
# SECOND TITLE        yaxis= 16.5            rect_width=120             xaxis=4.55
# SECOND PRICE        yaxis= 17.5            rect_width=120             xaxis=4.55
# ELSE :                  D E F A U L T
"""
Programmer : Legend 
"""
import shutil
from scrapy import Selector
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import os
from urllib.parse import urlparse , urljoin
import string
import re
from PIL import ImageDraw, ImageFont
import json
from functools import wraps
from termcolor import colored

def memoize(func):
    cache={}
    @wraps(func)
    def wrapper(*args,**kwargs):
        key = str(args)+str(kwargs)
        if key not in cache:
            cache[key] = func(*args , **kwargs)
        return cache[key]
    return wrapper

@memoize
def check_title(title_to_execute):
    title=title_to_execute.split(' ')
    i=1
    titles=''
    if len(title)>3:
        # titles=title[0]+title[3]+title[2]
        for items in title:
            titles=titles+items+' '
            # print(titles)
            if i==3:
                break
            i+=1
    else:
        titles=title_to_execute
    # elif title[2] == title[-1]:
    return titles

@memoize
def get_best_selling(valid_url):
    best_selling_name1 = None
    best_selling_name2 = None
    best_selling_price1 = None
    best_selling_price2 = None
    best_selling_image_urls1 = []
    best_selling_image_urls2 = []
    # try:
    if True:
        res = requests.get(f"{valid_url}/collections/all?sort_by=best-selling")
        ra = Selector(text=res.text)
        
        # Find the URL of the best-selling product
        try:
            product_url1 = [a for a in ra.css("a::attr(href)").getall() if "collections/all/products" in a][0]
            product_url2 = [a for a in ra.css("a::attr(href)").getall() if "collections/all/products" in a][1]
            product_url2_text = ra.css(f"a[href='{product_url2}']").xpath("text()").extract_first()
            product_url1_text = ra.css(f"a[href='{product_url1}']").xpath("text()").extract_first()
            if product_url1_text==product_url2_text:
                product_url2 = [a for a in ra.css("a::attr(href)").getall() if "collections/all/products" in a][2]
        except:
            product_url = [a for a in ra.css("a::attr(href)").getall() if "products" in a]
            stop=False
            i=0
            while stop==False:
                try:
                    # print(i)
                    product_url1=product_url[i]
                    product_url2=product_url[i+1]
                    i+=1
                    product_url2_text = ra.css(f"a[href='{product_url2}']").xpath("text()").extract_first()
                    product_url1_text = ra.css(f"a[href='{product_url1}']").xpath("text()").extract_first()
                    # Extract JSON data for the best-selling product
                    json_url1 = f'{valid_url}/products/{product_url1.rsplit("/",1)[1].split("?")[0]}.json'
                    # print(json_url1)
                    json_data1 = json.loads(requests.get(json_url1).content)
                    json_url2 = f'{valid_url}/products/{product_url2.rsplit("/",1)[1].split("?")[0]}.json'
                    json_data2 = json.loads(requests.get(json_url2).content)
                    # print(json_data1)
                    # print(json_data2)
                    best_selling_name1 = json_data1['product']['title']
                    best_selling_name2 = json_data2['product']['title']
                    best_selling_price1 = float(json_data1['product']['variants'][0]['price'])
                    best_selling_price2 = float(json_data2['product']['variants'][0]['price'])
                    if best_selling_name1 != best_selling_name2 and "gift card" not in best_selling_name1.lower() and "gift card" not in best_selling_name2.lower():
                        stop=True
                except:
                    # print("Failed")
                    pass
        # print(product_url1)
        # print(product_url2 )
        # print(product_url1_text )
        # print(product_url2_text )
        
        
        # print(json_url1)
        # print(json_url2)
        
        # Extracting product details
        
        # Extracting image URLs
        for image in json_data1['product']['images']:
            if not image or image==[]:
                image=extract_image_urls(f"{valid_url}/collections/all?sort_by=best-selling")
                best_selling_image_urls1.append(image)
            else:
                best_selling_image_urls1.append(image['src'])
        for image in json_data2['product']['images']:
            if not image or image==[]:
                image=extract_image_urls(f"{valid_url}/collections/all?sort_by=best-selling")
                best_selling_image_urls2.append(image)
            else:
                best_selling_image_urls2.append(image['src'])
            # @memoize
    # except Exception as e:
    #     print("Error occurred while scraping:", e)
    if best_selling_name1 !=None: 
        best_selling_name1=check_title(best_selling_name1)
    if best_selling_name2 !=None: 
        best_selling_name2=check_title(best_selling_name2)
    return best_selling_name1,best_selling_name2, best_selling_price1,best_selling_price2, best_selling_image_urls1, best_selling_image_urls2

@memoize
def download_images(image_urls):
    image_url=[]
    for items in image_urls:
        for item in items:
            image_url.append(item)
            break
    image_urls=image_url
    try:
        if os.path.exists("images"):
            shutil.rmtree("images")
            os.mkdir("images")
        if not os.path.exists("images"):
                os.makedirs("images")
        
        # Download images from the provided list of URLs
        i = 0
        for url in image_urls:
            i += 1
            filename = f"Image{i}.jpg"  # Renaming the images sequentially
            filepath = os.path.join("images", filename)  # Saving images inside 'images' folder
            try:
                # Send an HTTP request to get the image content
                response = requests.get(url)
                if response.status_code == 200:
                    # Save the image content to a file
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded image from URL: {url}")
                    if i >= 4:  # Assuming you want to download only 5 images
                        break
                else:
                    print(f"Failed to download image from URL: {url}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Failed to download image from URL: {url}. Error: {e}")
        else:
            print("No more image URLs found for products")
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))

@memoize
def insert_image(url,image_name,yaxis=6.47,xaxis=1.25):
    try:
        print("\nInserting Image.")
        url=url.split("//")[-1].split(".")[0]
        # Open the template
        template = Image.open(url + ".jpg")
        
        # Open the image to be inserted
        image=Image.open("images\\"+image_name)
        
        # Resize the image to fit into the template (optional)
        image = image.resize((100, 100))  # Adjust dimensions as needed
        
        move_distance_px = xaxis * 37.8
        move_distance_px2= yaxis * 37.8
        
        x = int(move_distance_px)
        y = int(move_distance_px2)  
        template.paste(image, (x, y))
        
        # Save the resulting image
        template.save(f"{url}.jpg")
        print("Inserted Image in template.")
    except Exception as e:
        print(colored(f"Sorry: Error occured: {e}"))

@memoize
def remove_unwanted_list(title_divs):
        lst= ['Featured','£to£Apply','£to£Apply','Join Our Newsletter!', 'Further Info.','Specials','Recently viewed','Trending','Deals','Discounts','Categories','Availability','Price','Recently Viewed Products','CloseCustomer LoginIf you are already registered, please log in.','CloseYour Cart0items','Promotions','New Arrivals',  '','Cart','Products', 'menuMenu','Add to cart','Available','New products','Quick view','Main menu','USEFUL LINKS','Collection','Sign up and save','Quick Shop']
        for items in lst:
            if items in title_divs:
                title_divs.remove(items)
            else:
                pass
        return title_divs

@memoize
def insert_text(url,text,yaxis=6.6 ,rect_width=300, xaxis=4.2 , rect_height=20,font_size=20, font_color=(0, 0, 0)):
    try:
        text= f" {text}"
        url=url.split("//")[-1].split(".")[0]
        template = Image.open(url + ".jpg")
        # Create a drawing object
        draw = ImageDraw.Draw(template)
        
        # Define font properties
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # Calculate text position
        move_distance_px = xaxis * 37.8
        move_distance_px2 = yaxis * 37.8
        x = int(move_distance_px)
        y = int(move_distance_px2)
        
        # Get text size
        # text_width, text_height = draw.textbbox(text)
        
        # Define rectangle dimensions
        padding = 5
        rect_width = rect_width + 2 * padding
        rect_height = rect_height + 2 * padding
        
        # Draw white rectangle as background
        draw.rectangle([(x, y), (x + rect_width, y + rect_height)], fill="white")
        
        # Draw text
        draw.text((x + padding, y + padding), text, font=font, fill=font_color)
        
        # Save the resulting image
        template.save(f"{url}.jpg")
        print("Inserted Text in template.")
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))

@memoize
def check_file(url):
    try:
        if not os.path.exists(url):
            
            url=url.split("//")[-1].split(".")[0]
            image = Image.new("RGB", (550, 1080), color="white")
            image.save(f"{url}.jpg")
            image = Image.open(f"{url}.jpg")
            
            template = Image.open(url+".jpg")
            
            # Open the image to be inserted
            image = Image.open("Image1.png")
            
            # Resize the image to fit into the template (optional)
            image = image.resize((570, 1080))  # Adjust dimensions as needed
            
            # Calculate the position to place the image in the center of the template
            x = (template.width - image.width) // 2
            y = (template.height - image.height) // 2
            
            # Paste the image onto the template
            template.paste(image, (x, y))
            
            # Save the resulting image
            template.save(f"{url}.jpg")
        else:
            pass
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))

@memoize
def extract_image_urls(html_content, base_url,title_value2):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        image_urls = []
        for img_tag in soup.find_all('img'):
            # First, try to get the 'src' attribute
            image_url = img_tag.get('src')
            if image_url and not image_url.startswith("data:"):  # Exclude data URLs
                # Insert statement to extract title
                title = img_tag.get('alt','') or img_tag.get('title', '')   # Get the 'alt' or 'title' attribute as title, if available
                image_urls.append((urljoin(base_url, image_url), title))  # Append tuple of image URL and title
                
            # If 'src' attribute is not found, try 'srcset' attribute
            if image_url and image_url.startswith("data:"):
                srcset = img_tag.get('srcset')
                if srcset:
                    # Split srcset by comma and extract the URLs
                    src_urls = srcset.split(',')
                    # Skip the first URL
                    for src in src_urls[1:]:
                        src = src.strip().split(' ')[1]  # Extracting URL and ignoring descriptors
                        if src and not src.startswith("data:"):
                            # Insert statement to extract title
                            title = img_tag.get('alt', '') or img_tag.get('title', '') # Get the 'alt' or 'title' attribute as title, if available
                            image_urls.append((urljoin(base_url, src), title))  # Append tuple of image URL and title
        
        # Filter out image URLs linked from <a> tags with href equal to "/"
        for a_tag in soup.find_all('a', href="/"):
            for img_tag in a_tag.find_all('img'):
                img_src = img_tag.get('src')
                if img_src:
                    image_urls = [(url, title) for url, title in image_urls if url != urljoin(base_url, img_src)]
        image_urls=str(image_urls)
        new_image= image_urls.split(",")
        new_image=str(new_image)
        new_image=new_image.split("'")
        a=filter_image_urls(new_image,title_value2)
        # a=image_urls[0]+image_urls[2]
        # print(a)
        return a
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))

@memoize
def filter_image_urls(image_urls,title_value2):
    try:
        # print(image_urls)
        first_products_url= image_urls[1]
        # print(image_urls)
        # i=0
        f=0
        second_product_url="" 
        for url in image_urls:
            if title_value2 in url:
                second_product_url=image_urls[f-2]
                break
            elif url.startswith("https://"):
                url=url.split("/")[5]
                if url not in first_products_url.split("/")[5]:
                    second_product_url=image_urls[f]
                    break
                

            f+=1
        if not second_product_url:
            # print("parse")
            second_product_url=image_urls[5]
        # print(second_product_url)
        return first_products_url , second_product_url
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))

@memoize
def get_valid_filename(url):
    try:
        # Extract filename from URL and sanitize it
        url_path = urlparse(url).path
        filename = os.path.basename(url_path)
        # Remove invalid characters from the filename
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in filename if c in valid_chars)
        return filename.strip()
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))
while True:
    url= input("\nEnter the url: ")
    if url=="0":
        break
    try:
        domain= "https://"+url+"/collections/all?sort_by=best-selling"
        print(colored(f"\n Our Domain is {domain}","green"))
        print(colored(f"\n Extracting Price","yellow"))
        # price= scrap_text_with_price_class(domain,"price")
        best_selling=get_best_selling(f"https://{url}")
        price_value1=best_selling[2]
        price_value2=best_selling[3]
        print(colored(f"\n Extracting Title","yellow"))
        title_value1= best_selling[0]
        title_value2= best_selling[1]
        
        print(colored("\nChecking Template ","cyan"))
        check_file(domain)
        
        print(colored("\nDownloading Images","blue"))
        download_images(best_selling[-2:])
        # download_image(best_selling[-1],'images\\Image2.jpg')
        
        print(colored("\nInserting First Image","magenta"))
        insert_image(domain, "Image1.jpg")
        
        print(colored("\nInserting Second Image","magenta"))
        insert_image(domain, "Image2.jpg", 16.35, 1.6)
        
        print(colored("\nInserting First Title","cyan"))
        insert_text(domain,title_value1)
        
        print(colored("\nInserting First Price","light_cyan"))
        insert_text(domain,price_value1,7.8,200)
        
        print(colored("\nInserting Second Title","blue"))
        insert_text(domain,title_value2,16.5,120,4.55)
        
        print(colored("\nInserting Second Price","light_blue"))
        insert_text(domain,price_value2,17.635,120,4.55,24)
        
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))
