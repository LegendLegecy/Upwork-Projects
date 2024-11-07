from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy import Selector
import re
import json
import time
import shutil
from scrapy import Selector
from PIL import Image
import os
from urllib.parse import urlparse , urljoin
from PIL import ImageDraw, ImageFont
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

def Cart_template(website_url):
    # @memoize
    def initial():
        try:
            if not os.path.exists(url):
                # Extracting the domain from the URL
                # background image                
                image= Image.open("static\\image.jpg")
                # Opening the Image1.jpg to use as a background
                background_image = Image.open("Image1.png")
                # Resizing the background image to fit into the white background (optional)
                background_image = background_image.resize((570, 1080))
                # Pasting the background image onto the white background
                image.paste(background_image, (0, 0))
                # Saving the resulting image with the domain name as image.jpg
                image.save(f"static\\image.jpg")
            else:
                pass
        except Exception as e:
            print(colored(f"Error occurred: {e}", "red"))


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
    
    # @memoize
    
    def get_best_selling(website_url):
        best_selling_name1 = None
        best_selling_name2 = None
        best_selling_price1 = None
        best_selling_price2 = None
        best_selling_image_urls1 = []
        best_selling_image_urls2 = []

        try:
            res = requests.get(f"{website_url}/collections/all?sort_by=best-selling")
            ra = Selector(text=res.text)

            json_data1 = ''
            json_data2 = ''

            product_url = [a for a in ra.css("a::attr(href)").getall() if "products" in a]
            i = 0
            while i < len(product_url) - 1:
                product_url1 = product_url[i]
                product_url2 = product_url[i + 1]
                i += 1
                json_url1 = f'{website_url}/products/{product_url1.rsplit("/", 1)[1].split("?")[0]}.json'
                json_url2 = f'{website_url}/products/{product_url2.rsplit("/", 1)[1].split("?")[0]}.json'

                # Fetch JSON data for the first product
                try:
                    json_data1 = json.loads(requests.get(json_url1).content)
                    best_selling_name1 = json_data1['product']['title']
                    best_selling_price1 = float(json_data1['product']['variants'][0]['price'])
                except Exception as e:
                    print(f"Error fetching JSON data for product 1: {e}")

                # Fetch JSON data for the second product
                try:
                    json_data2 = json.loads(requests.get(json_url2).content)
                    best_selling_name2 = json_data2['product']['title']
                    best_selling_price2 = float(json_data2['product']['variants'][0]['price'])
                except Exception as e:
                    print(f"Error fetching JSON data for product 2: {e}")

                # Check if names are different and not gift cards
                if best_selling_name1 != best_selling_name2 and "gift card" not in best_selling_name1.lower() and "gift card" not in best_selling_name2.lower():
                    break

        except Exception as e:
            print(f"Error occurred while fetching data: {e}")

        # Apply check_title function to non-empty titles
        if best_selling_name1 and best_selling_name1.strip():
            best_selling_name1 = check_title(best_selling_name1)
        if best_selling_name2 and best_selling_name2.strip():
            best_selling_name2 = check_title(best_selling_name2)

        # Extract image URLs
        for image in json_data1.get('product', {}).get('images', []):
            if not image or image == []:
                image = extract_image_urls(f"{website_url}/collections/all?sort_by=best-selling")
                best_selling_image_urls1.append(image)
            else:
                best_selling_image_urls1.append(image['src'])

        for image in json_data2.get('product', {}).get('images', []):
            if not image or image == []:
                image = extract_image_urls(f"{website_url}/collections/all?sort_by=best-selling")
                best_selling_image_urls2.append(image)
            else:
                best_selling_image_urls2.append(image['src'])

        return best_selling_name1, best_selling_name2, best_selling_price1, best_selling_price2, best_selling_image_urls1, best_selling_image_urls2

    # @memoize
    def download_images(image_urls):
        image_url=[]
        for items in image_urls:
            for item in items:
                image_url.append(item)
                break
        image_urls=image_url
        try:
            
            
            # Download images from the provided list of URLs
            i = 0
            for url in image_urls:
                i += 1
                filename = f"Image{i}.jpg"  # Renaming the images sequentially
                filepath = os.path.join("static", filename)  # Saving images inside 'images' folder
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
    # @memoize
    def insert_image(url, image_name, yaxis=6.47, xaxis=1.52):
        try:
            print("\nInserting Image.")
            url = url.split("//")[-1].split("/")[0]
            # Open the template
            template = Image.open(f"static\\image.jpg")

            # Open the image to be inserted
            image = Image.open("static\\" + image_name)

            # Resize the image to fit into the template (optional)
            image = image.resize((100, 100))  # Adjust dimensions as needed

            move_distance_px = xaxis * 37.8
            move_distance_px2 = yaxis * 37.8

            x = int(move_distance_px)
            y = int(move_distance_px2)
            template.paste(image, (x, y))

            # Save the resulting image
            template.save(f"static\\image.jpg")
            print("Inserted Image in template.")
        except Exception as e:
            print(colored(f"Sorry: Error occurred: {e}"))

    # @memoize
    def insert_text(url, text, yaxis=6.6, rect_width=300, xaxis=4.2, rect_height=20, font_size=20, font_color=(0, 0, 0)):
        try:
            text = f" {text}"
            url = url.split('//')[-1].split('/')[0]
            template = Image.open(f"static\\image.jpg")
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
            template.save(f"static\\image.jpg")
            print("Inserted Text in template.")
        except Exception as e:
            print(colored(f"Error occurred: {e}", "red"))
    def check_file(url):
        try:
            if not os.path.exists("static\\image.jpg"):
                # Create a new template image if it doesn't exist
                image = Image.new("RGB", (550, 1080), color="white")
                image.save("static\\image.jpg")
        except Exception as e:
            print(colored(f"Error occurred: {e}", "red"))

    # @memoize
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
    
    # @memoize
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
    
    try:
        url=website_url
        domain= url+"/collections/all?sort_by=best-selling"
        initial()
        print(colored(f"\n Our Domain is {domain}","green"))
        print(colored(f"\n Extracting Price","yellow"))
        # price= scrap_text_with_price_class(domain,"price")
        best_selling=get_best_selling(url)
        price_value1=best_selling[2]
        price_value2=best_selling[3]
        print(colored(f"\n Extracting Title","yellow"))
        title_value1= best_selling[0]
        title_value2= best_selling[1]
        print(title_value1)
        print(title_value2)
        print(price_value1)
        print(price_value2)
        print(colored("\nChecking Template ","cyan"))
        check_file(domain)
        
        print(colored("\nDownloading Images","blue"))
        download_images(best_selling[4:])
        # download_image(best_selling[-1],'images\\Image2.jpg')
        
        print(colored("\nInserting First Image","magenta"))
        insert_image(domain, "Image1.jpg")
        
        print(colored("\nInserting Second Image","magenta"))
        insert_image(domain, "Image2.jpg", 16.35, 1.87)
        
        print(colored("\nInserting First Title","cyan"))
        insert_text(domain,title_value1)
        
        print(colored("\nInserting First Price","light_cyan"))
        insert_text(domain,price_value1,7.8,200)
        
        print(colored("\nInserting Second Title","blue"))
        insert_text(domain,title_value2,16.5,120,4.55)
        
        print(colored("\nInserting Second Price","light_blue"))
        insert_text(domain,price_value2,17.635,120,4.55,24)
        return title_value1 , price_value1
    except Exception as e:
        print(colored(f"Error occured: {e}","red"))


def processing(website_url):
    @memoize
    def analyze_speed_combined(url, timeout=120):
        start_time = time.time()  # Get the current time
        if True:
        # Perform your operation here (e.g., fetching the URL)
            print("Analyzing speed using PageSpeed Insights API...")
            try:
                # Construct the command
                command = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}"
                # print(command)
                result= requests.get(command)
                # Check if result.stdout is not None
                if result.text is not None:
                    # Parse the JSON output
                    output_json = json.loads(result.text)
                    # print("load")
                    # Extract speed analysis data
                    speed_score = output_json['lighthouseResult']['categories']['performance']['score']
                    print("Speed Score (PageSpeed Insights API):", speed_score)
                    
                    # Extract specific performance metrics
                    metrics = output_json['lighthouseResult']['audits']
                    fcp = metrics['first-contentful-paint']['displayValue']
                    tti = metrics['interactive']['displayValue']
                    print("First Contentful Paint (PageSpeed Insights API):", fcp)
                    print("Time to Interactive (PageSpeed Insights API):", tti)
                    
                    # You can extract more metrics as needed
                    
                    # Analyze speed with web scraping
                    print("\nAnalyzing speed with web scraping...")
                    
                    # Send a GET request to the URL
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                    
                    # Parse the HTML content of the webpage
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract specific performance-related information from the webpage
                    # For example, you can extract the size of the webpage, number of requests, etc.
                    page_size = len(response.content) / 1024  # Size of the page in KB
                    num_requests = len(soup.find_all(['img', 'script', 'link', 'iframe', 'object', 'video']))  # Number of requests
                    
                    print("Page Size (Web Scraping):", page_size, "KB")
                    print("Number of Requests (Web Scraping):", num_requests)
                    
                    # You can perform additional analysis or extract more information as needed
                    
                    return speed_score, fcp, tti, page_size, num_requests
                
                else:
                    print("Error:No output from curl command")
                    # return None, None, None, None, None
            
            except requests.exceptions.RequestException as e:
                # If there's an error with the request, print it
                print("Error with web scraping:", e)
                return None, None, None, None, None
            
            # Replace this with your actual code
            
        elapsed_time = time.time() - start_time  # Calculate the elapsed time
        # print(elapsed_time)
        # Check if the elapsed time exceeds the timeout
        if elapsed_time > timeout:
            print("Operation timed out")
            # Handle the timeout scenario (e.g., raise an exception, return an error code)
        else:
            print("Operation completed within the timeout")
    @memoize
    def analyze_email_optimization(html_content):
        print("\nAnalyzing Email Optimization.")
        # Check for Klaviyo or Omnisend scripts
        if "klaviyo" in html_content.lower():
            # print("Email Optimization Advice:Klaviyo detected")
            return "Klaviyo detected"
        elif "omnisend" in html_content.lower():
            # print( "Email Optimization Advice:Omnisend detected")
            return "Omnisend detected"
        else:
            print( "Email Optimization Advice:Install Omnisend or Klaviyo")
            return "Install Omnisend or Klaviyo"
    @memoize
    def extract_boomer_values_from_html(url):
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all <script> tags
            script_tags = soup.find_all('script',class_="boomerang")

            # Initialize variables to store theme name and version
            themename = None
            themeversion = None

            # Iterate through <script> tags to find relevant JavaScript code
            for script in script_tags:
                # print(script)
                # Check if the script contains window.boomer.themename and window.boomer.themeversion
                if 'window.BOOMR.themeName' in script.text:
                    # Extract theme name using regular expression
                    themename_match = re.search(r'window\.BOOMR\.themeName\s*=\s*["\']([^"\']+)["\']', script.text)
                    if themename_match:
                        # print(1)
                        themename = themename_match.group(1)
                if 'window.BOOMR.themeVersion' in script.text:
                    # Extract theme version using regular expression
                    themeversion_match = re.search(r'window\.BOOMR\.themeVersion\s*=\s*["\']([^"\']+)["\']', script.text)
                    if themeversion_match:
                        # print(2)
                        themeversion = themeversion_match.group(1)
            div_tags=soup.find_all("div",id=lambda x :x and "shopify-section-template" in x)
            # if div_tags==0 or div_tags==None or div_tags=="0" or div_tags==[] or div_tags=='':
                # div_tags=soup.find_all("div",id=lambda x :"shopify-section-template" and x in x)
            num=0
            for div in div_tags:
                num+=1
            if num==0:
                num="few"
            return themename, themeversion,num
    @memoize
    def get_best_selling(valid_url):
        best_selling_name = None
        best_selling_price = None
        try:
            res = requests.get(f"{valid_url}/collections/all?sort_by=best-selling")
            ra = Selector(text=res.text)
            
            # Find the URL of the best-selling product
            try:
                product_url = [a for a in ra.css("a::attr(href)").getall() if "collections/all/products" in a][0]
            except:
                product_url = [a for a in ra.css("a::attr(href)").getall() if "products" in a][0]
            
            # Extract JSON data for the best-selling product
            json_url = f"{valid_url}/products/{product_url.rsplit('/',1)[1].split('?')[0]}.json"
            json_data = json.loads(requests.get(json_url).content)
            
            # Extracting product details
            best_selling_name = json_data['product']['title']
            best_selling_price = float(json_data['product']['variants'][0]['price'])

        except Exception as e:
            print("Error occurred while scraping:", e)

        return best_selling_name, best_selling_price

    for i in range (2):
        # try:
            response = requests.get(website_url)
            if response.status_code == 200:
                print("\nStep 1")
                html_content = response.text
                print("\nStep 2")
                speed_advice = analyze_speed_combined(website_url)  # Analyze speed using the combined function
                
                print("\nStep 3")
                email_advice = analyze_email_optimization(html_content)
                print("\nStep 4")
                print("\nStep 5")
                boomer= extract_boomer_values_from_html(website_url)
                best_selling= get_best_selling(website_url)
                # Generate HTML report
                website_url=website_url.split("//")[-1]
                print("\nDONE")
                # print(website_url,speed_advice[0],speed_advice[1],speed_advice[2],speed_advice[3],speed_advice[4],email_advice,best_selling[0],best_selling[1],boomer[0],boomer[1],boomer[2],website_url,website_url)
                # print( f"Analyzed {website_url}",f"Speed Score: {speed_advice[0]}",f"First Contentful Paint: {speed_advice[1]}",f"Time to Interactive: {+speed_advice[2]}",f"Page Size: {speed_advice[3]}",f"Number of Requests: {speed_advice[4]}",email_advice,best_selling[0],best_selling[1],f"Theme Name: {boomer[0]}",f"Theme Version: {boomer[1]}",f"Templates Present: {boomer[2]}",website_url,website_url)
                l=[ f"Analyzed {website_url}:",f"Its Speed Score is {speed_advice[0]}.",f"Our Analysis also found First Contentful Paint i.e {speed_advice[1]}.",f"We found that Time to Interact is {speed_advice[2]}",f"If you are looking for Page Size, it is {speed_advice[3]}",f"and Number of Requests are {speed_advice[4]}",email_advice,best_selling[0],best_selling[1],f"Theme Name is {boomer[0]}.",f"Theme Version is {boomer[1]}.",f"Furthermore Templates Present are {boomer[2]}.",website_url,website_url]
                return l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11],l[12],l[13]
                # return l
            else:
                print("Error:Unable to fetch website content")
            break
            
            # print(report_html)
        # except Exception as e:
        #     print('Sorry Error Occured:',e)

app = Flask(__name__)


@app.route('/shopify-conversion-analyzer')
def index():
    return render_template('index.html')


@app.route('/analyzing', methods=['POST'])
def analyzing():
    website_url = request.form['website_url']
    with open ("url","w") as f:
        f.write(website_url)
    url=website_url.split("//")[-1]
    return render_template('processed.html')

@app.route("/Report-by-EcomRolodex")
def report():
    with open ("url","r") as f:
        website_url=f.readlines()
        if not isinstance(website_url, str):
            for items in website_url:
                website_url=items
                break
    f=Cart_template(website_url)
    a=processing(website_url)
    return render_template("result.html",website= a[0],name=a[9],version=a[10],
                        score=a[1],paint=a[2],time=a[3],size=a[4],
                        requests=a[5],templates=a[11],klaviyo=a[6],
                        title=f[0],price=f[1])
if __name__ == '__main__':
    app.run(debug=True)