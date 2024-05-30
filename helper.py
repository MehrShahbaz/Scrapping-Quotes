import requests
import json
from bs4 import BeautifulSoup

# Constant to use for printing separation lines
breakPrint = "\n==========================================================================================\n"
# HTTP status code for a successful response
response_ok = 200

def custom_print(data, endPrint=False):
    """
    Print data with a custom separator before and after the content.
    If endPrint is True, print the separator after the content as well.
    """
    print(breakPrint)
    print(data)
    if endPrint:
        print(breakPrint)

def print_list(data):
    """
    Print each item in the list using custom_print function.
    """
    for x in data:
        custom_print(x)
    print(breakPrint)

def write_in_file(data, file_name):
    """
    Write data to a file in JSON format. If an error occurs, print an error message.
    """
    try:
        f = open(file_name, "w")
        json.dump(data, f)
        f.close()
    except:
        print(f"Error Writing to the file: {file_name}")

def find_next_page_url(soup, base_url):
    """
    Find the URL for the next page from the BeautifulSoup object.
    If a next page link exists, return the full URL; otherwise, return None.
    """
    next_li = soup.select_one(".next a")
    return base_url + next_li.get("href") if next_li else None

def remove_character(string, chars):
    """
    Remove specific characters from a string.
    """
    return "".join([c for c in string if c not in chars])

def format_quote(data):
    """
    Format the quote by removing specific characters (e.g., quotation marks).
    """
    return remove_character(data, ["”", "“"])

def fetch_page(url):
    """
    Fetch the HTML content of a given URL using requests and parse it with BeautifulSoup.
    If an error occurs, print an error message and return None.
    """
    try:
        response = requests.get(url)
        if response.status_code != response_ok:
            raise Exception("Bad Response")
        return BeautifulSoup(response.text, "html.parser")
    except:
        print(f"Error fetching the URL: {url}")
        return None

def extract_quotes(soup, url):
    """
    Extract quotes, authors, and tags from the BeautifulSoup object and return them as a list of dictionaries.
    """
    return [
        {
            "quote": format_quote(div.select_one("span.text").text),
            "author": div.select_one(".author").text,
            "tags": [x.text for x in div.select(".tag")],
            "url": url,
        }
        for div in soup.select(".quote")
    ]

def convert_to_mbs(data):
    """
    Convert bytes to megabytes.
    """
    return data / (1024 * 1024)

def print_memory_use(current, peak):
    """
    Print the current and peak memory usage in megabytes.
    """
    custom_print(f"Current memory usage: {convert_to_mbs(current):.2f} MB")
    custom_print(f"Peak memory usage: {convert_to_mbs(peak):.2f} MB", True)

def append_to_list_in_file(key, number):
    try:
        try:
            with open("time.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file does not exist or is empty or contains invalid JSON, initialize with an empty dictionary
            data = {}

        if key in data:
            data[key].append(number)
        else:
            data[key] = [number]

        with open("time.json", "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(f"An error occurred: {e}")

def print_execution_time(start, end):
    """
    Print the time taken for an operation.
    """
    custom_print(f"Time taken = {end-start:.3f} Seconds", True)
