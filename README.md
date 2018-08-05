# wingman-data-scraper
A python program to convert an HTML file of CS:GO Wingman match history to a CSV file.

To use this program:

1. Download your wingman html file from [here](https://steamcommunity.com/my/gcpd/730?tab=matchhistorywingman).
  (I recommend [this](https://chrome.google.com/webstore/detail/save-page-we/dhhpefjklgkmgeafimnjhojgjamoafof) to save all the loaded data)
2. Place the html file in the same directory as this program.

3. Run the command $python wingman.py "{steam_username}" "{html_file_name}". Note: quotes are necessary.

4. A file 'wingman.csv' will be created in your current directory.
