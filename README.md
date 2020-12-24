# Youtube-Recipes-Dataset-with-Ingredients
This dataset was scraped using YouTube API v3, an open-source third party api that extract transcipts from videos, and a kaggle dataset containing recipe keywords.
Unused or unecessary recipe keywords were filtered out by running a script multiple times on thousands of youtube videos. The video title, thumbnail url, video url, and list
of recipe keywords are outputted to YouTubeRecipesData.csv. frequency.csv calculates and updates how frequent a keyword ingredient was used.


Sources used for scraping data:

https://www.kaggle.com/kaggle/recipe-ingredients-dataset

https://pypi.org/project/youtube-transcript-api/

https://developers.google.com/youtube/v3/getting-started
