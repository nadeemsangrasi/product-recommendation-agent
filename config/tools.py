import requests
from concurrent.futures import ThreadPoolExecutor
import os
from agents import function_tool

def get_amazon_product_details_by_id(product_id: str):

        url = "https://real-time-amazon-data.p.rapidapi.com/product-details"
        querystring = {"asin": product_id, "country": "US"}
        headers = {
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        }

        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            return response.json().get("data", {})
        except (requests.Timeout, requests.ConnectionError):
            return {}
        except Exception as e:
            print(f"Error fetching details for {product_id}: {str(e)}")
            return {}

def get_walmart_product_details_by_id(product_id: str):
    
        url = "https://realtime-walmart-data.p.rapidapi.com/product"
        querystring = {"itemId":product_id}
        headers = {
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "x-rapidapi-host": "realtime-walmart-data.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            return response.json()
        except (requests.Timeout, requests.ConnectionError):
            return {}
        except Exception as e:
            print(f"Error fetching details for {product_id}: {str(e)}")
            return {}

def initialize_tools():
    # Define tools for Amazon and walmart
    @function_tool
    def get_real_time_product_data_from_amazon(product_name: str) -> str:
        """Fetch live Amazon product data including price, stock status, and ratings.
        Use only when the user explicitly asks for an Amazon comparison."""
        # Initial search
        url = "https://real-time-amazon-data.p.rapidapi.com/search"
        headers = {
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"), 
            "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        }

        try:
            search_response = requests.get(url, headers=headers, params={
                "query": product_name,
                "page": "1",
                "country": "US",
                "sort_by": "RELEVANCE"
            })
            search_data = search_response.json()
        except Exception as e:
            print(f"Search failed: {str(e)}")
            return []

        # Early exit if no products
        if not search_data.get("data", {}).get("products"):
            print("No products found")
            return []

        # Get first 2 products to limit API calls
        products = search_data["data"]["products"][:2]
        asin_list = [p["asin"] for p in products]

        # Parallel fetch for product details
        with ThreadPoolExecutor(max_workers=3) as executor:
            details_results = list(executor.map(get_amazon_product_details_by_id, asin_list))

        # Merge results
        for product, details in zip(products, details_results):
            product["product_details"] = details

        return f"Amazon data for {products}"

    @function_tool
    def get_real_time_product_data_from_walmart(product_name: str) -> str:
        """Fetch live walmart product data including price, stock status, and ratings.
        Use only when the user explicitly asks for a walmart comparison."""
            # Initial search
        url = "https://realtime-walmart-data.p.rapidapi.com/search"
        headers = {
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),  # Use userdata here too!
            "x-rapidapi-host": "realtime-walmart-data.p.rapidapi.com"
        }
        querystring = {"keyword":product_name,"page":"1","sort":"price_high"}

        try:
            search_response = requests.get(url, headers=headers, params=querystring, )
            search_data = search_response.json()
        except Exception as e:
            print(f"Search failed: {str(e)}")
            return []

        # Early exit if no products
        if not search_data.get("results"):
            print("No products found")
            return []

        # Get first 2 products to limit API calls
        products = search_data["results"][:2]
        usItemId_list = [p["usItemId"] for p in products]

        # Parallel fetch for product details
        with ThreadPoolExecutor(max_workers=3) as executor:
            details_results = list(executor.map(get_walmart_product_details_by_id, usItemId_list))

        # Merge results
        for product, details in zip(products, details_results):
            product["product_details"] = details


        return f"walmart data for {products}"

    return {'get_real_time_product_data_from_walmart':get_real_time_product_data_from_walmart,'get_real_time_product_data_from_amazon':get_real_time_product_data_from_amazon}
