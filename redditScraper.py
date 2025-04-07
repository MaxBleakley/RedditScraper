import requests
import os
import datetime
# This is for making sure the post file name is a okay (doesn't have restricted chars)
import re
from gtts import gTTS


def sanitizeFilename(filename):
    # Remove characters that are invalid in file names.
    return re.sub(r'[\\/*?:"<>|]', "", filename)
    # uses the url and mozilla engine


def getTopPosts():
    url = "https://www.reddit.com/r/creepypasta/top/.json?t=week&limit=5"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; RedditScraper/1.0)'}
    # Status code 200 is successful status code so if it doesn't get it then it throws an error
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return

    data = response.json()
    posts = data.get('data', {}).get('children', [])

    # Create a folder for the posts if there isn't already one
    folder = "creepypasta_posts"
    os.makedirs(folder, exist_ok=True)

    for post in posts:
        postData = post.get('data', {})
        title = postData.get('title', 'No Title')
        selfText = postData.get('selftext', '')
        createdUtc = postData.get('created_utc')
        if createdUtc:
            # Convert Unix timestamp to a date string
            dateStr = datetime.datetime.fromtimestamp(createdUtc).strftime("%Y-%m-%d")
        else:
            dateStr = "no_date"

        # Sanitize the title to help prevent errors
        sanitizedTitle = sanitizeFilename(title)
        fileName = f"{sanitizedTitle}_{dateStr}.txt"

        # Save the content to txt file
        filePath = os.path.join(folder, fileName)
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(selfText)

        print(f"Saved post to {filePath}")

        # text to an mp3 file using gTTS
        tts = gTTS(selfText, lang='en')
        mp3FileName = f"{sanitizedTitle}_{dateStr}.mp3"
        mp3FilePath = os.path.join(folder, mp3FileName)
        tts.save(mp3FilePath)
        print(f"Converted text to mp3 and saved to {mp3FilePath}")


if __name__ == "__main__":
    getTopPosts()
