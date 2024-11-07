import requests  # Import the requests module to handle HTTP requests.
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML.





def get_href(url):
    "Get Hrefs From Url"
    
    print("\nGetting Urls.")  # Inform the user that URLs are being fetched.
    try:
        # Send a GET request to the specified URL.
        response = requests.get(url)
        
        # Check if the request was successful (status code 200).
        if response.status_code == 200:
            # Get the HTML content of the page.
            html_content = response.text
            
            # Parse the HTML content with BeautifulSoup.
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all <div> tags with the class 'blogContent'.
            divs = soup.find_all('div', class_='blogContent')
            
            # Initialize empty lists to store hrefs and the final selection.
            hrefs = []
            final_selection = []
            
            # List of keywords to search for within the <span> tags.
            keywords = ['USD', 'CAD', 'GBP', 'AUD', 'EUR', '(USD', '(CAD', '(GBP', '(AUD', '(EUR']
            
            # Iterate through all found <div> tags.
            for div in divs:
                # Extract text from all <span> tags within each <div>.
                span_texts = [span.get_text() for span in div.find_all("span")]
                
                # Check if any of the keywords are present in the span texts.
                if any(keyword in text for keyword in keywords for text in span_texts):
                    # If a keyword is found, add the <div> to the final selection.
                    final_selection.append(div)
            
            
            # Iterate through the selected <div> elements.
            for items in final_selection:
                # Find the first <a> tag with an href attribute.
                link = items.find('a', href=True)
                
                if link:  # Check if an <a> tag was found.
                    href = link['href']  # Get the href attribute from the <a> tag.
                    
                    # Check if the href starts with '/shop/url/' and process it.
                    if href.startswith('/shop/url/'):
                        hrefs.append(href.split('/shop/url/')[-1])

                    # Check if the href starts with 'shop/url/' and process it.
                    elif href.startswith('shop/url/'):
                        hrefs.append(href.split('shop/url/')[-1])
            
            # Return the list of extracted hrefs.
            return hrefs

        else:
            # Print an error message if the page could not be retrieved.
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    except Exception as e:
        # Print any exceptions that occur during execution.
        print(e)










def write_url(href):
    "Write URLs in urls.txt"
    
    # Open the file 'urls.txt' in append mode.
    with open("urls.txt", "a") as f:
        # Write the href to the file with a newline.
        f.write(f"{href}\n")







# Prompt the user to enter a URL to scrape.
url = input("\nEnter The Url:")

# Call the get_href function to get the list of hrefs from the URL.
hrefs = get_href(url)

print("\nWriting URLs in urls.txt")  # Inform the user that URLs are being written to the file.

# Iterate through the list of hrefs.
for href in hrefs:
    write_url(href)  # Write each href to the file.


print("\nCompleted")  # Inform the user that the process is complete.

# Pause the script and wait for the user to press Enter to exit.
input("Press Enter to Exit . . .")
