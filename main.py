import requests
from datetime import datetime

# WordPress API URL for media
wordpress_site = input("Enter the wordpress site url, ex: galitie.com ")
api_url = f'https:/{wordpress_site}/wp-json/wp/v2/media'


# Set the date range
print("Set the date range to retrieve images YEAR-MO-DY, ex: '2023-12-30':")
start_date = input("Enter the start date in the exact format above: ")
end_date = input("Enter the end date in the exact format above: ")

# Convert date strings to datetime objects
start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

# Get user input for the destination directory
destination_directory = input("Enter the folder path where you would like to save the files: ")

# Initialize variables
page = 1
per_page = 100
all_media = []
counter = 0

while True:
    # Prepare parameters for the API request
    params = {
        'after': start_datetime.isoformat(),
        'before': end_datetime.isoformat(),
        'per_page': per_page,
        'page': page,
        'post': 0,  # Filter by unattached media items
    }

    # Make the API request
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f'Request made, on page {page}, loading next page...')
        # Parse the JSON response
        media_data = response.json()
        
        # If there are no more media items, break the loop
        if not media_data:
            print(f"API requests finished! Total requested pages = {page}, All possible media to download (includes all extentions) = {len(all_media)}")
            break
        
         # Append current page media to the list
        all_media.extend(media_data)

        # Increment page for the next request
        page += 1
    
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        break

# List of allowed file extensions
allowed_extensions = ['.jpeg', '.jpg', '.png']
      
# Iterate through each media item
for media in all_media:
    # Check if the media item is a JPEG or PNG
    if media['mime_type'] in ['image/jpeg', 'image/png', 'img/jpg']:
        # Get the URL of the media item
        media_url = media['source_url']

        # Download the media file
        media_response = requests.get(media_url)

        # Save the media file to the specified directory
        file_path = f"{destination_directory}/{media['slug']}.{media_url.split('.')[-1]}"
        
        with open(file_path, 'wb') as file:
            file.write(media_response.content)

        print(f"Downloaded image {media['slug']}.{media_url.split('.')[-1]}")
        counter += 1

    
input(f'All done! Downloaded {counter} {allowed_extensions} files. Press Enter to close!')
