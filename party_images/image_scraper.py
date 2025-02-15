import os
import requests
from bs4 import BeautifulSoup

# Get the base directory name directly
base_directory_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# URL of the Wikipedia page
url = "https://de.wikipedia.org/wiki/Liste_der_politischen_Parteien_in_Deutschland"

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table by its class name
table = soup.find('table', {'class': 'wikitable'})

# Function to download an image
def download_image(image_url, image_name):
    try:
        # Send a GET request to fetch the image
        img_response = requests.get(image_url)
        img_response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Get the image content
        img_data = img_response.content
        
        # Save the image to a file
        with open(image_name, 'wb') as f:
            f.write(img_data)
        print(f"Downloaded {image_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {image_url}: {e}")

# Initialize a list to store the party details
party_details = []

# Iterate over each row in the table
for row in table.find_all('tr')[1:]:  # Skip the header row
    # Find all table data cells in the row
    cells = row.find_all('td')
    if len(cells) > 1:
        # The party name is in the second cell
        party_name_cell = cells[1]
        # Find the link within the party name cell
        link = party_name_cell.find('a')
        if link:
            # Get the href attribute of the link
            href = link.get('href')
            # Construct the full URL
            party_url = f"https://de.wikipedia.org{href}"

            # Send a GET request to fetch the party page content
            party_response = requests.get(party_url)
            party_response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the party page content with BeautifulSoup
            party_soup = BeautifulSoup(party_response.text, 'html.parser')

            # Find the infobox containing the party's logo and chair images
            infobox = party_soup.find('table', {'class': 'infobox'})

            if infobox:
                # Create a folder for each party
                party_name = link.get_text(strip=True)
                party_folder = os.path.join(base_directory_name, party_name)
                os.makedirs(party_folder, exist_ok=True)

                # Create subfolders for the logo and chairs
                logo_folder = os.path.join(party_folder, 'logo')
                chairs_folder = os.path.join(party_folder, 'chairs')
                os.makedirs(logo_folder, exist_ok=True)
                os.makedirs(chairs_folder, exist_ok=True)

                # Find the first image (the logo)
                logo_img_tag = infobox.find('img')
                logo_url = None
                if logo_img_tag:
                    logo_src = logo_img_tag.get('src')
                    if logo_src:
                        logo_url = f"https:{logo_src}"

                # Download the logo image
                if logo_url:
                    logo_image_name = os.path.join(logo_folder, 'logo.jpg')
                    download_image(logo_url, logo_image_name)

                # Find all other images in the infobox (these are the chair(s))
                chair_images = []
                # Get all image tags in the infobox
                all_img_tags = infobox.find_all('img')
                # Skip the first image (logo), process the rest
                for i, img in enumerate(all_img_tags[1:]):  # Start from the second image
                    img_src = img.get('src')
                    if img_src:
                        chair_image_url = f"https:{img_src}"
                        chair_images.append(chair_image_url)
                        # Download the chair images
                        chair_image_name = os.path.join(chairs_folder, f'chair_{i + 1}.jpg')
                        download_image(chair_image_url, chair_image_name)

                # Append the party name, logo URL, and chair images URLs to the list
                party_details.append({
                    'party_name': party_name,
                    'logo_url': logo_url,
                    'chair_images': chair_images
                })

# Print the list of party details (name, logo URL, chair images URLs)
for party in party_details:
    print(f"Party: {party['party_name']}")
    print(f"Logo URL: {party['logo_url']}")
    print("Chair Images URLs:")
    for chair_image in party['chair_images']:
        print(f"- {chair_image}")
    print()