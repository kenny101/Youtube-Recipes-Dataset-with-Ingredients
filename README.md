# Youtube-Recipes-Dataset-with-Ingredients
This dataset was scraped using YouTube API v3, an open-source third party api that extract transcipts from videos, and a kaggle dataset containing recipe keywords.
Unused or unecessary recipe keywords were filtered out by running a script multiple times on thousands of youtube videos. The video title, thumbnail url, video url, and list
of recipe keywords are outputted to YouTubeRecipesData.csv. frequency.csv calculates and updates how frequent a keyword ingredient was used.


## Sources used:

https://www.kaggle.com/kaggle/recipe-ingredients-dataset

https://pypi.org/project/youtube-transcript-api/

https://developers.google.com/youtube/v3/getting-started

Use the extractData.py to append more data to YouTubeRecipesData.csv. For this script to work properly, all files should be in the same directory.

## Usage:
python3 extractData (youtube playlist url 1) (youtube playlist url 2)...

YouTube Playlist URLS begin with "https://www.youtube.com/playlist?list=". It will not work on individual video links
