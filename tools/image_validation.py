import requests
from PIL import Image
from io import BytesIO

def is_image_suitable(image_url):
    try:
        # Fetch the image
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Check the content type
        if 'image' not in response.headers['Content-Type']:
            return False
        
        # Check the file size (e.g., less than 5MB)
        if int(response.headers.get('Content-Length', 0)) > 5 * 1024 * 1024:
            return False
        
        # Check the image dimensions (e.g., at least 800x600)
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        if width < 800 or height < 600:
            return False
        
        return True
    except Exception as e:
        print(f"Error validating image: {e}")
        return False
