# https://developer.spotify.com/documentation/web-api for spotify api documentation
# https://spotipy.readthedocs.io/en/2.22.1/#examples for spotipy documentation
# https://onlinedevtools.in/curl convert curls to http urls
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("id")
CLIENT_SECRET = os.getenv("secret")

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
)


def recommend(genre):
    if genre == "hiphop":
        seed_gen = "hip-hop"
    else:
        seed_gen = genre

    recommend_list = []
    recommendations = spotify.recommendations(
        seed_artists=None,
        seed_genres=[seed_gen],
        seed_tracks=None,
        limit=6,
        country=None,
    )
    for i in range(6):
        recommend_list.append(
            {
                "Song": recommendations["tracks"][i]["name"],
                "Artist": recommendations["tracks"][i]["artists"][0]["name"],
                "Link": recommendations["tracks"][i]["external_urls"]["spotify"],
                "Image": recommendations["tracks"][i]["album"]["images"][2]["url"],
            }
        )

    return recommend_list


def new_recommend(genres):
    try:
        index_hop = genres.index("hiphop")
        genres[index_hop] = "hip-hop"
    except ValueError:
        pass
    finally:
        seed_gen = genres
    seed_gen = seed_gen * 2
    recommend_list = []
    for i in range(len(seed_gen)):
        recommendations = spotify.recommendations(
            seed_artists=None,
            seed_genres=[seed_gen[i]],
            seed_tracks=None,
            limit=1,
            country=None,
        )
        recommend_list.append(
            {
                "Song": recommendations["tracks"][0]["name"],
                "Artist": recommendations["tracks"][0]["artists"][0]["name"],
                "Link": recommendations["tracks"][0]["external_urls"]["spotify"],
                "Image": recommendations["tracks"][0]["album"]["images"][2]["url"],
                "Genre": seed_gen[i],
            }
        )

    return recommend_list


""" Music recommend card html
<div class="card">
    <div class="card__img"></div>
    <div class="card__title">Runaway</div>
    <div class="card__subtitle">Smalltown Boy , Shane D</div>
</div>

"""

""" Music recommend card css
.card {
  --main-color: #fff;
  --bg-color: #090909;
  --sub-main-color: #B9B9B9;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  width: 360px;
  height: 370px;
  background: var(--bg-color);
  border-radius: 20px;
  padding: 30px;
}


.card__img {
  height: 224px;
  width: 224px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-inline: auto;
  background: #131313;
  border-radius: 100%;
}

.card__img svg {
  width: 154px;
  height: 154px;
  border-radius: 100%;
}

.card__title {
  font-weight: 500;
  font-size: 28px;
  color: var(--main-color);
  text-align: center;
  margin-bottom: 10px;
  margin-top: 15px;
}

.card__subtitle {
  font-weight: 400;
  font-size: 16px;
  color: var(--sub-main-color);
  text-align: center;
  cursor: pointer;
}
"""

""" Upload button html
<div class="input-div">
  <input class="input" name="file" type="file">
<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" stroke-linejoin="round" stroke-linecap="round" viewBox="0 0 24 24" stroke-width="2" fill="none" stroke="currentColor" class="icon"><polyline points="16 16 12 12 8 16"></polyline><line y2="21" x2="12" y1="12" x1="12"></line><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"></path><polyline points="16 16 12 12 8 16"></polyline></svg>
</div>

"""

""" Upload button css
.input-div {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid rgb(1, 235, 252);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  box-shadow: 0px 0px 100px rgb(1, 235, 252) , inset 0px 0px 10px rgb(1, 235, 252),0px 0px 5px rgb(255, 255, 255);
}

.icon {
  color: rgb(1, 235, 252);
  font-size: 2rem;
  cursor: pointer;
}

.input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer !important;
}

"""

""" music recommend option 2 html
<div class="audio-player">
  <div class="album-cover"></div>
  <div class="player-controls">
    <div class="song-info">
      <div class="song-title">Song Title</div>
      <p class="artist">Artist</p>
    </div>
</div>

"""

""" music recommend option 2 css
.audio-player {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 300px;
  height: 80px;
  background-color: #282828;
  border-radius: 8px;
  padding: 8px;
  box-sizing: border-box;
}

.album-cover {
  width: 64px;
  height: 64px;
  background-color: #fff;
  border-radius: 50%;
  margin-right: 12px;
}

.player-controls {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.song-info {
  margin-bottom: 4px;
}

.song-title {
  font-size: 16px;
  color: #fff;
  margin: 0;
}

.artist {
  font-size: 12px;
  color: #b3b3b3;
  margin: 0;
}


"""
