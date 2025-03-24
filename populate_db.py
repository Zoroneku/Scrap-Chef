import os
import django
import random
from googleapiclient.discovery import build

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Scrap_Chef.settings')
django.setup()

from scrapchef.models import User, UserProfile, Post, Review, List
from django.core.management import call_command

YOUTUBE_API_KEY = 'AIzaSyDSCvEbUjI9mFP7v3MMnnpbUYEsBcv7ocs'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

WORDS = ["Fat", "Thin", "Big", "Small", "Fast", "Slow", "Red", "Blue", "Green", "Shark", "Bear", "Eagle", "Tiger", "Fox"]

call_command('flush', interactive=False)

def generate_username():
    """Generate a random username with two words and a two-digit number."""
    word1 = random.choice(WORDS)
    word2 = random.choice(WORDS)
    number = str(random.randint(10, 99))
    return f"{word1}{word2}{number}"

def fetch_youtube_recipes(query="recipe", max_results=10):
    """Fetch recipe videos from YouTube API."""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video"
    ).execute()
    
    videos = []
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
        
        videos.append({
            "video_id": video_id,
            "title": title,
            "description": description,
            "thumbnail": thumbnail
        })
    
    return videos

def create_users(count=15):
    """Create default users."""
    occupations = ["Chef", "Food Blogger", "Home Cook", "Baker"]
    names= []

    for _ in range(count):
        username = generate_username()
        
        while username in names:
            username = generate_username()

        new_user = User.objects.create_user(username=username, password="hashedpassword")

        user_profile = UserProfile.objects.get(User=new_user)
        user_profile.Occupation = random.choice(occupations)
        user_profile.Profile_photo = ""

        user_profile.save()
        new_user.save()
        names.append(username)

def populate():
    print("Populating database with 15 default users and YouTube recipe videos...")

    if User.objects.count() < 15:
        create_users(15 - User.objects.count())

    videos = fetch_youtube_recipes()

    for video in videos:
        Post.objects.create(
            Media=f"https://www.youtube.com/embed/{video['video_id']}",
            Caption=video["title"],
            User = random.choice(User.objects.all())
        )

    print("Database population complete! (Users & Posts added, Lists & Reviews remain empty)")

if __name__ == "__main__":
    populate()