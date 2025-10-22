import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# Dictionary to map emotions to IMDb URLs
URLS = {
    "Drama": 'https://www.imdb.com/search/title/?title_type=feature&genres=drama&countries=IN&languages=ta',
    "Action": 'https://www.imdb.com/search/title/?title_type=feature&genres=action&countries=IN&languages=ta',
    "Comedy": 'https://www.imdb.com/search/title/?title_type=feature&genres=comedy&countries=IN&languages=ta',
    "Horror": 'https://www.imdb.com/search/title/?title_type=feature&genres=horror&countries=IN&languages=ta',
    "Crime": 'https://www.imdb.com/search/title/?title_type=feature&genres=crime&countries=IN&languages=ta',
}

def fetch_movies(emotion):
    url = URLS.get(emotion)
    if not url:
        return []

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36'
        )
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, "lxml")

    # Extract movie titles
    titles = [a.get_text() for a in soup.find_all('a', href=re.compile(r'/title/tt\d+/'))]

    # IMDb repeats some text (like "See more") — filter out junk
    titles = [t for t in titles if len(t) > 2 and not t.startswith("See more")]

    return list(dict.fromkeys(titles))  # remove duplicates while preserving order


# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Tamil Movie Recommender", page_icon="🎬")

st.title("🎬 Tamil Movie Recommendation App")
st.write("Get Tamil movies by emotion/genre (IMDb data).")

# Dropdown for emotion
emotion = st.selectbox("Select a Genre/Emotion", list(URLS.keys()))

if st.button("Get Movies"):
    with st.spinner("Fetching movies... 🎥"):
        movie_titles = fetch_movies(emotion)

    if not movie_titles:
        st.error("No titles found. Try again later.")
    else:
        max_titles = 14 if emotion in ["Drama", "Action", "Comedy", "Horror", "Crime"] else 12
        st.success(f"Top {max_titles} {emotion} movies:")
        for idx, title in enumerate(movie_titles[:max_titles], start=1):
            # Remove any leading numbering (e.g., "1. " or "2. ") from the title
            cleaned_title = re.sub(r'^\d+\.\s*', '', title.strip())
            st.write(f"{idx}. {cleaned_title}")
