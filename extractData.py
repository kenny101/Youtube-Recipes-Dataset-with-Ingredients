#!/usr/bin/python3
import csv
import pandas as pd
from csv import writer
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import operator
import sys

# Youtube API Key
api_key = 'your youtube API key'

# format the file
def format_file(file_dir):
    s = open(file_dir,'r').read()
    chars = ('[',']','{','}',"'","\\",'""')
    for c in chars:
        s = ''.join( s.split(c))

    out_file = open(file_dir,'w')
    out_file.write(s)
    out_file.close()

# Takes a YouTube video id and outputs the thumbnail url
def extractThumbnail(video_id):
    video_url = "http://img.youtube.com/vi/"+str(video_id)+"/hqdefault.jpg"
    return(video_url)

# Takes in a playlist and outputs the individual video links
def get_source(playlist_url):
    #extract playlist id from url
    url = playlist_url
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]

    #print(f'get all playlist items links from {playlist_id}')
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = api_key)

    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 50
    )
    response = request.execute()

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    return [ 
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
        for t in playlist_items
    ]

# extracts only the video id from a playlist
def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail?
    return None

# prints the data of a csv file
def printData(file_name):
    f = open(file_name)
    csv_f = csv.reader(f)
    for row in csv_f:
        print(row)

# Append to the spreadsheet by rows
def appendTo(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

# extracts list of video ids from a playlist/video
def extract_id(playlist_url):
    # if the link was not a playlist
    if 'list' not in playlist_url:
        single_id = playlist_url.split('=')
        return(single_id[1])

    playlist = get_source(playlist_url)

    vid_id = []
    for video in playlist:
        vid_id.append(extract_video_id(video))

    return vid_id

# extract a set of ingredients from a vid id
def extractIngredients(ingredients_file, vid_id):
    # add the ingredients to an array
    tupleList = []
    with open(ingredients_file,"r") as infile:
            for line in infile:
                line = line.split(", ")
                tupleList.append(line)

    ind = 0
    ingredients = []
    for items in tupleList:
        ingredients.append(tupleList[ind][0])
        ind = ind+1
    print(ingredients)
    containedIngredients = []
    transcript = str(YouTubeTranscriptApi.get_transcript(vid_id))
    for word in ingredients:
        if word in transcript:
            containedIngredients.append(word)
    
    for ingredient in containedIngredients:
        incrementFrequency(ingredient, 'frequency.csv')
    return set(containedIngredients)

# increment number of times an ingredient was used
def incrementFrequency(ingredient, file_dir):
    tupleList = []
    with open(file_dir,"r") as infile:
        for line in infile:
            line = line.split(", ")
            tupleList.append(line)

    ind = 0
    for num in tupleList:
        # print("error: " + str(tupleList[ind][1]))
        tupleList[ind][1] = int(tupleList[ind][1])
        # tupleList[ind][1] = tupleList[ind][1]
        # check if an occurence of the ingredient was found
        if (ingredient in tupleList[ind]):
            tupleList[ind][1] = tupleList[ind][1]+1
        ind = ind+1
    # parse correct format back into the file
    with open(file_dir, 'w') as writer:
        for item in tupleList:
            writer.write(str(item).replace("[","").replace("]","").replace("'","")+"\n")
    writer.close()

# gets the title of a single youtube video given url
def get_title(vid_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    ids = vid_id
    titles = []
    results = youtube.videos().list(id=ids, part='snippet').execute()
    for result in results.get('items', []):
        titles.append(result['snippet']['title'])
    return(titles)

def removeDuplicates(file_name):
    df = pd.read_csv(file_name)
    df.drop_duplicates(inplace=True)
    df.to_csv(file_name, index=False)

# sort the csv file from highest to lowest
def sort_csv(file_dir):
    mytuple = []
    i = 0
    with open(file_dir,"r") as infile:
        for line in infile:
            value = line.split(', ')
            print(value)
            value[1] = int(value[1])
            mytuple.append(value)

    csvOpen = open(file_dir, 'w')
    c = csv.writer(csvOpen)

    sort = sorted(mytuple, key=operator.itemgetter(1), reverse=True)
    for x in sort:
        ingredient = str(x[0])
        val = " " + str(x[1])
        c.writerow([ingredient, val])

# outputs the necessary data to the csv file
def extract_all_data(vid_url):
    #TODO: Handle cases for single video

    # for playlists
    source = get_source(vid_url)
    names = []
    img = []
    ingredients = []

    id_list = extract_id(vid_url)
    
    # extracting names, thumbnails, and ingredients
    for id in id_list:
        try:
            ingredients.append(extractIngredients('frequency.csv', id))
        except:
            continue 
        names.append(get_title(id))
        img.append(extractThumbnail(id))


    # adding the data to the csv file
    for i in range(len(names)-1):
        output = [names[i],img[i],source[i],sorted(ingredients[i])]
        print(output)
        appendTo('YouTubeRecipesData.csv', output)

    format_file('YouTubeRecipesData.csv')


def print_invalid_ingredients(file):
    with open(file, 'r', newline='') as f:
        data = csv.DictReader(f)
        for row in data:
            print(row[0])



# Parsing command line arguments
for i in range(2,len(sys.argv)):
    if sys.argv[i].startswith('https://www.youtube.com/playlist?list='):
        extract_all_data(sys.argv[i])
    else:
        print('Invalid argument. Youtube URL must be a playlist or API key was invalid/has invalid permissions')
        break










