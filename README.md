# wingman-data-scraper
A python program to convert an HTML file of CS:GO Wingman match history to a CSV file.

First run fetch_data.py, then run parse_data.py to format the data.

Directions below:

## fetch_data.py
  args: match-type (0 or 1)
  
  fetch_data.py 0 will fetch data for competitive matches
  
  fetch_data.py 1 will fetch data for wingman matches
  
  output: out-match-type.html
  
 ## parse_data.py
 args: username(string), html-file-location(string)
 
 personalized stats will be created for username in matches
 
 output: out-match-type.csv
