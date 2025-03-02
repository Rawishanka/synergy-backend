from datetime import datetime
import json


def parse_meta_data(meta_data):
    """ Extracts date and location from meta_data JSON string """
    meta_dict = json.loads(meta_data)
    date_str = meta_dict.get("date")
    location = meta_dict.get("location")
    
    # Convert date string to Date object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() if date_str else None
    return date_obj, location

def parse_price(price_str):
    """ Extracts and converts price from string to integer """
    price_str = price_str.replace("Rs", "").replace(",", "").strip()
    return int(price_str) if price_str.isdigit() else 0

def parse_image_urls(image_urls):
    """ Converts list of image URLs to comma-separated string """
    return ",".join(image_urls).replace("{", "").replace("}", "")
