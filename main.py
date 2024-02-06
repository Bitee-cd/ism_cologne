from ism_cologne import SinglePageDetails
import json

#NOTE: Run ism_cologne_urls before running this file

total_data =[]
def remove_duplicate_urls(file_path):
    # Read URLs from the file
    with open(file_path, "r") as file:
        urls = file.readlines()

    # Remove duplicates by converting to a set
    unique_urls = set(urls)

    # Write unique URLs back to the file
    with open(file_path, "w") as file:
        for url in unique_urls:
            file.write(url)
def get_data(file_path):
    with open(file_path, "r") as file:
        urls = file.readlines()[:10]

    for url in urls:
        singlePageDetail = SinglePageDetails(url)
        data = singlePageDetail.run_scraper()
        total_data.append(data)

    with open("ism_cologne.json", "w") as json_obj:
            json.dump(total_data, json_obj)
            print("done scrapping")


remove_duplicate_urls("urls.txt")
get_data("urls.txt")