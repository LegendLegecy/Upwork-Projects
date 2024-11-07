
def get_description_links(url):
    import requests
    from bs4 import BeautifulSoup

    url = url+'.json' if not url.endswith(".json") else url
    import requests

    # Send a GET request to fetch the JSON data
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON data
        product = data.get('product', {})
        body_html = product.get("body_html", {})
        
        final_src= []
        initial_src= body_html.split(' src="')[1:]
        for items in initial_src:
            final_src = final_src.append( items.split('"')[0])
    else:
        print("Failed to retrieve the data. Status code:", response.status_code)
    
    if not final_src:
        # Send a GET request to fetch the HTML data
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all div tags with a class containing the word 'description'
            divs = soup.find_all('div', class_=lambda c: c and 'description' in c)
            
            final_src = []
            for div in divs:
                # Find all img tags within the div
                imgs = div.find_all('img')
                for img in imgs:
                    # Get the src attribute
                    src = img.get('src')
                    if src:
                        final_src.append(src)
                        
        else:
            print("Failed to retrieve the data. Status code:", response.status_code)
            return []
    return final_src



def get_description(url):
    import requests
    from bs4 import BeautifulSoup
    # Send a GET request to fetch the HTML data
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all div tags with a class containing the word 'description'
        divs = soup.find_all('div', class_=lambda c: c and 'description' in c)
        
        final_para = []
        for div in divs:
            # Find all img tags within the div
            paragraphs = div.find_all('p')
            for paragraph in paragraphs:
                # Get the src attribute
                para = paragraph.get_text()
                if para:
                    final_para.append(para)
                    
        return final_para



a=get_description("https://grabfastdeals.com/products/hair.json")
for items in a:
    print(items)