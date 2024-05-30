import concurrent.futures
from timeit import default_timer as timer
from helper import (
    fetch_page,
    find_next_page_url,
    custom_print,
    write_in_file,
    extract_quotes,
    print_execution_time,
    append_to_list_in_file,
)


def process_page(args):
    base_url, url = args
    soup = fetch_page(url)
    if soup:
        quotes = extract_quotes(soup, url)
        custom_print("Current Url: " + url, True)
        next_url = find_next_page_url(soup, base_url)
        return quotes, next_url
    return [], None


# Method to get all the quotes from the URL
# Returns a list of quotes
def scrape_quotes(base_url):
    current_url = base_url
    data = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        while current_url:
            results = executor.map(process_page, [(base_url, current_url)])
            for quotes, next_url in results:
                data.extend(quotes)
                current_url = next_url

    return data


if __name__ == "__main__":
    # Start the timer and memory tracer
    time_start = timer()

    # Base URL for the quotes
    base_url = "https://quotes.toscrape.com"

    # Get all the quotes from the website
    quotes = scrape_quotes(base_url)

    # Write the quotes to a file named "data.json"
    write_in_file(quotes, "data.json")

    # Stop the memory tracer and end the timer
    time_end = timer()

    # Print the execution time and memory usage in MB
    print_execution_time(time_start, time_end)
    append_to_list_in_file("concurrentFutures", time_end - time_start)
