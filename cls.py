###############################################################
#
# Libraries
#
###############################################################

import requests
from bs4 import BeautifulSoup
import sys
import json
import csv
import tabulate


###############################################################
#
# Scraper
#
###############################################################

def scrape(url):
    # Try to get the given URL
    try:
        html = requests.get(url).text
               
    # Quit program otherwise
    except:
        print('Failed to retrieve url "%s"' % url)
        sys.exit()
    
    # Parse content
    content = BeautifulSoup(html, 'lxml')
    
    # Parse selectors
    try:
        # Init content selectors
        selectors = json.loads(sys.argv[2])
        
        # Create variable to store results
        results = []
        
        # Create item to store extracted data
        item = {}
        
        # Loop over selectors
        for tag in selectors['tags']:
            # Append selector class to item
            item[tag['class']] = [one.text for one in content.findAll(tag['tag'], {'class': tag['class']})]
        
        # loop over row indexes
        for index in range(0, len(item[next(iter(item))])):
            # Create single 'row' to append to table
            row = {}
            
            # loop over stored data
            for key, value in item.items():
                # append value to the new row
                row[key] = '"' + value[index] + '"'
            
            # append new row to results list
            results.append(row)
        
        # Specify table field names
        field_names = []

        # Loop over selectors
        for selector in selectors['tags']:
            # Loop over selector's items
            for key, val in selector.items():
                # Use class names as field names
                if key == 'class':
                    field_names.append(val)
        
        # Print table to console
        print(tabulate.tabulate([row.values() for row in results], field_names, tablefmt="fancy_grid"))
            
        # Try to write results to CSV file
        try:
            # Store file name
            file_name = sys.argv[3]

            # Write results to CSV file
            with open(file_name, 'w', newline='') as file_csv:
                # Init dictionary writer
                writer = csv.DictWriter(file_csv, fieldnames=field_names)
                
                # Write table header
                writer.writeheader()
                
                # Populate table with rows
                for row in results:
                    writer.writerow(row)
        
        # Except the case if file name is not provided
        except:
            print('Provide "filename.csv" as the last argument to store file')
    
    # Except malformed json string
    except:
        print('Failed to parse selectors!')


###############################################################
#
# Main
#
###############################################################

# If no command line options specified
if len(sys.argv) == 1:
    print('Type "cls.py -help" to get some help...')
    sys.exit()

# Print HELP ,essage
elif sys.argv[1] == '-help':
    print('Usage: ...')

# Run scraper
elif 'http' in sys.argv[1]:
    # URL to scrape data from
    url = sys.argv[1]
    
    # Run scraper
    scrape(url)
    


    

