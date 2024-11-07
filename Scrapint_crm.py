import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape data from a single page
def scrape_page(url):
    headers = {
        'User-Agent': 'Your User Agent String Here'  # You may need to set a user agent string
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Replace these selectors with the actual selectors from the CRM's webpage
        names = [name.text.strip() for name in soup.select('your_name_selector')]
        emails = [email.text.strip() for email in soup.select('your_email_selector')]
        # Similarly, extract other fields like phone number, company name, etc.
        return list(zip(names, emails))  # Adjust this based on the fields you're scraping
    else:
        print("Failed to fetch page:", url)
        return []

# Function to scrape data from multiple pages
def scrape_all_pages(base_url, num_pages):
    all_records = []
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}&page={page_num}"  # Modify this to fit the pagination scheme of your CRM
        page_records = scrape_page(url)
        all_records.extend(page_records)
    return all_records

def main():
    base_url = 'https://example.com/your_crm_data_endpoint?'  # Replace with your CRM's data endpoint
    num_pages = 10  # Adjust this based on the number of pages in your CRM
    records = scrape_all_pages(base_url, num_pages)
    
    # Write the scraped data to a CSV file
    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Email']  # Add other fields as needed
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({'Name': record[0], 'Email': record[1]})  # Adjust this based on the fields you're scraping

if __name__ == "__main__":
    main()
