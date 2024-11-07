import requests
from bs4 import BeautifulSoup
import csv

def get_hotel_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract hotel name
        hotel_name_tag = soup.find('h2', class_='hp__hotel-name')
        if hotel_name_tag:
            hotel_name = hotel_name_tag.text.strip()
        else:
            hotel_name = "N/A"
        
        # Find and click on "Our guest experience"
        guest_experience_link = soup.find('a', string='Our guest experience')
        if guest_experience_link:
            guest_experience_url = 'https://www.booking.com' + guest_experience_link['href']
            
            # Fetch data from "Our guest experience" page
            guest_response = requests.get(guest_experience_url)
            if guest_response.status_code == 200:
                guest_soup = BeautifulSoup(guest_response.content, 'html.parser')
                
                # Extract rating point
                rating_point = guest_soup.find('div', class_='bui-review-score__badge').text.strip()
                
                # Extract number of reviews
                num_reviews = guest_soup.find('div', class_='bui-review-score__text').text.strip()
                
                return hotel_name, rating_point, num_reviews
            else:
                return None
        else:
            return None
    else:
        return None

# Example URLs
urls = [
    "https://www.booking.com/hotel/in/oyo-rooms-near-100-feet-road-madhapur.html",
    "https://www.booking.com/hotel/in/oyo-flagship-70318-royal-park.html",
    "https://www.booking.com/hotel/in/oyo-flagship-80974-grand-stay.html"
]

# Open CSV file in write mode
with open('hotel_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Hotel Name', 'Rating Point', 'Number of Reviews'])
    
    for url in urls:
        hotel_info = get_hotel_info(url)
        if hotel_info:
            csv_writer.writerow(hotel_info)

print("Data saved to hotel_data.csv file.")
