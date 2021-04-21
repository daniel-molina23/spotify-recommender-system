import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import pandas as pd
import time
import statistics
import numpy

# Values that can be changed

    # current_user = 'yojam4kpfre3ozvia2n73cduw'
        # any public username can be set
        
    # current_user_playlist_ids = getPlaylists(current_user, 0) 
        # 2nd parameter (offset)

    #current_user_track_ids = getTracks(current_user, current_user_playlist_ids, 1)
        # 2nd parameter (number of tracks)

    # while len(users) < 50:
    # for user in users:
    #     if not(user in root_users):
    #         if len(users) > 50:
    #### number represents how many minimum users should be considered/added

def getUsers(user):
    playlist_ids = getPlaylists(user, 0)

    for x in playlist_ids:
        try: 
            playlist = sp.user_playlist(user, x)
            owner = playlist['owner']['id']
            if (not(owner == current_user) and not(owner in users)):
                print("added:", owner)
                users.append(owner)
        except:
            print("playlist not found")

def getPlaylists(user, playlist_offset):
    # get user's 50 playlists
    results = sp.user_playlists(user=user, offset=playlist_offset, limit=50)
    playlist_ids = []
    for idx, item in enumerate(results['items']):
        playlist = item['id']
        playlist_ids.append(playlist)
    return playlist_ids

def getTracks(user, playlist_ids, track_limit):
    # get all tracks from given playlists
    track_ids = []
    for x in playlist_ids:
        tracks = sp.user_playlist_tracks(user=user, playlist_id=x, limit=track_limit)
        # print(track)
        # print()
        # print()
        for item in tracks['items']:
            try:
                track_ids.append(item['track']['id'])
            except:
                print("no ID present")

    print("len(track_ids)", len(track_ids))
    return track_ids

def getFeatures(track_ids):
    # get all features from each track
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = getTrackFeatures(track_ids[i])
        tracks.append(track)
        print(i)
    return tracks

def getTrackFeatures(id):
    try:
        meta = sp.track(id)
        features = sp.audio_features(id)

        # meta
        # name = meta['name']
        # album = meta['album']['name']
        # artist = meta['album']['artists'][0]['name']
        # release_date = meta['album']['release_date']
        # length = meta['duration_ms']
        popularity = meta['popularity']

        # features
        acousticness = features[0]['acousticness']
        danceability = features[0]['danceability']
        energy = features[0]['energy']
        instrumentalness = features[0]['instrumentalness']
        # liveness = features[0]['liveness']
        loudness = features[0]['loudness']
        speechiness = features[0]['speechiness']
        tempo = features[0]['tempo']
        # time_signature = features[0]['time_signature']

        # track = [name, album, artist, release_date, length, popularity, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
        track = [popularity, danceability, acousticness, energy, instrumentalness, loudness, speechiness, tempo]

        return track
    except:
        print("no track id")


scope = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id,
                                               client_secret=cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))


# current_user = 'yojam4kpfre3ozvia2n73cduw'
current_user = input("Input your username here! : ")

recommendation_count = input("How many users would you like me to recommended? : ")
recommendation_count = int(recommendation_count)

# get current user's 50 playlists
current_user_playlist_ids = getPlaylists(current_user, 0)
# get the next 50 playlists
current_user_playlist_ids2 = getPlaylists(current_user, 50)

# get 100 tracks from those playlists
current_user_track_ids = getTracks(current_user, current_user_playlist_ids, 100)
# get 25 tracks from those playlists
current_user_track_ids2 = getTracks(current_user, current_user_playlist_ids2, 25)

# for idx in current_user_track_ids2:
#     current_user_track_ids.append(idx)

print(len(current_user_track_ids))
# get all features from each track
current_user_tracks = getFeatures(current_user_track_ids)

print(current_user_tracks)
current_user_tracks = pd.DataFrame(current_user_tracks, columns = ['popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo'])

current_user_averages = []
max_col_value = {'popularity': 100,'danceability':1,'acousticness':1,'energy':1,'instrumentalness':1,'loudness':-60,'speechiness':1}
current_user_variances = []

for column in current_user_tracks.columns:
    if column == 'tempo':
        maxTempo = max(current_user_tracks['tempo'])
        average = statistics.mean(current_user_tracks[column])
        average_norms = average / maxTempo

    else:
        average = statistics.mean(current_user_tracks[column])
        average_norms = average / max_col_value[column]

    current_user_averages.append(average_norms)

    variance = statistics.variance(current_user_tracks[column])
    current_user_variances.append(variance)


# print(current_user_averages)

            
#normalize popularity...etc.
#Find average values for features the matter

# create dataset
# df = pd.DataFrame(current_user_tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
df = pd.DataFrame(current_user_tracks, columns = ['popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo'])

df.to_csv("current_user_songs.csv", sep = ',') 


users = []
root_users = []

# add owners of each playlist the current user follows
root_users.append(current_user)
print("getting owners of " + current_user + "'s playlists...")
for x in current_user_playlist_ids:
    try: 
        playlist = sp.user_playlist(current_user, x)
        owner = playlist['owner']['id']
        if (not(owner == current_user) and not(owner in users)):
            print("added:", owner)
            users.append(owner)
    except:
        print("playlist not found")

print()

# keep adding owners until around [x] owners are reached
while len(users) < 1000:
    for user in users:
        if not(user in root_users):
            if len(users) > 1000:
                break
            else:
                print("LENGTH:", len(users))
                print("getting owners of " + user + "'s playlists...")
                getUsers(user)
                print()
                root_users.append(user)

print(users)
print("LENGTH:", len(users))

#distances[]


distances = []

current_user_averages = numpy.array(current_user_averages)
current_user_variances = numpy.array(current_user_variances)

for user in users:

    # Get track information for each added user through their 50 playlists
    print("getting track information for " + user)
    playlist_ids = getPlaylists(user, 0)
    track_ids = getTracks(user, playlist_ids, 1)
    tracks = getFeatures(track_ids)
    tracks = pd.DataFrame(tracks, columns = ['popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo'])


    # Get average values for each feature
    user_averages = []
    user_variances = []

    for column in tracks.columns:
        if column == 'tempo':
            maxTempo = max(tracks['tempo'])
            average = statistics.mean(tracks[column])
            average_norms = average / maxTempo
        else:
            average = statistics.mean(tracks[column])
            average_norms = average / max_col_value[column]

        user_averages.append(average_norms)

        variance = statistics.variance(tracks[column])
        user_variances.append(variance)

    # Get difference for each user
    user_averages = numpy.array(user_averages)
    averages_distance = round(numpy.linalg.norm(current_user_averages - user_averages), 2)

    user_variances = numpy.array(user_variances)
    variances_distance = numpy.linalg.norm(current_user_variances - user_variances)

    # Add as user_id, distance, variance
    distances.append(tuple([user, averages_distance, variances_distance]))

    # df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'],)
    # csv_name = user + ".csv"
    # df.to_csv(csv_name, sep = ',')



# Sort first by average_distance, then by variance if tied
distances.sort(key=lambda x: (x[1], x[2]))


# Print out top 3 Recommendations
while len(distances) < recommendation_count:
    print("There is a maximum of ", len(distances), "users available to recommend. Please try again.")
    recommendation_count = input("How many users would you like me to recommended? : ")
    recommendation_count = int(recommendation_count)



#recommned the user and include their link
# count = 3

for x in distances[:recommendation_count]:
    print(x[0])

