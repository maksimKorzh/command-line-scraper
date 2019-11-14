#######################################################################
#
# Libraries
#
#######################################################################

import requests
import tabulate
import json
import csv
import sys
from bs4 import BeautifulSoup


#######################################################################
#
# Scraper
#
#######################################################################

def scrape(file_name):
    # Raw string format configuration data
    config_file = ''
    
    # Open configuration file
    with open(file_name, 'r') as json_file:
        for row in json_file.read():
            config_file += row
    
    # Dictionary structured configuration data
    config_file = json.loads(config_file)
    
    # Make HTTP GET request to fetch text data from URL
    html = requests.get(config_file['url'])
    
    # Parse content
    content = BeautifulSoup(html.text, 'lxml')
    
    # Create variable to store results
    results = []
    
    # Init content selectors
    tags = config_file['tags']
    
    # Create item to store extracted data
    scraped_items = {}
    
    # Loop over selectors
    for tag in tags:
        scraped_items[tag['class']] = [tag.text for tag in content.findAll(tag['tag'], {"class": tag['class']})]
    
    # Loop over the list of scraped items by tag
    for index in range(0, len(scraped_items[next(iter(scraped_items))])):
        # Create variable to store result row
        row = {}
        
        # Group scraped items' keys and values
        for key, val in scraped_items.items():
            row[key] = '"' + val[index] + '"'
        
        # Append the row to results list
        results.append(row)

    # Print table to console
    print(tabulate.tabulate([row.values() for row in results], config_file['columns'], tablefmt="fancy_grid"))

    # Write results to CSV file
    with open(config_file['output'], 'w', newline='') as file_csv:
        # Init dictionary writer
        writer = csv.DictWriter(file_csv, fieldnames=config_file['columns'])

        # Write table header
        writer.writeheader()

        # Populate table with rows
        for row in results:
            writer.writerow(row)

#######################################################################
#
# Main
#
#######################################################################

# Check the config file availability
if sys.argv[1]:
    scrape(sys.argv[1])

# Exit the program if no config file provided
else:
    print('Example usage: cls.py your_config_file.json')
    
    
    
    
    
    
    
    
