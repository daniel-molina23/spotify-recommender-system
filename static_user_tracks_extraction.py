# didnt work...ran the whole program from main
# from main import getFeatures, getUsers, getPlaylists, getTracks, current_user, sp
import pandas as pd
import numpy
import statistics
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred

start = 750
end = 850

def getPlaylists(user, playlist_offset):
    # get user's 50 playlists
    try:
        results = sp.user_playlists(user=user, offset=playlist_offset, limit=50)
    except:
        pass
    playlist_ids = []
    for idx, item in enumerate(results['items']):
        playlist = item['id']
        playlist_ids.append(playlist)
    return playlist_ids

def getTracks(user, playlist_ids, track_limit):
    # get all tracks from given playlists
    track_ids = []
    for x in playlist_ids:
        try:
            tracks = sp.user_playlist_tracks(user=user, playlist_id=x, limit=track_limit)
            # print(track)
            # print()
            # print()
            for item in tracks['items']:
                track_ids.append(item['track']['id'])
        except:
            pass

    print("len(track_ids)", len(track_ids))
    return track_ids

def getFeatures(track_ids, user_id):
    # get all features from each track
    tracks = []
    for i in range(len(track_ids)):
        # time.sleep(.5)
        track = getTrackFeatures(track_ids[i], user_id)
        if track == -1:
            pass
        else:
            tracks.append(track)
        # print(str(i) + ": " + user_id)
    return tracks

def getTrackFeatures(id, user_id):
    try:
        meta = sp.track(id)
        features = sp.audio_features(id)

        # meta
        # name = meta['name']
        # album = meta['album']['name']
        artist = meta['album']['artists'][0]['name']
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
        track = [user_id, artist, popularity, danceability, acousticness, energy, instrumentalness, loudness, speechiness, tempo]

        return track
    except:
        return -1


scope = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id,
                                               client_secret=cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))


current_user = 'yojam4kpfre3ozvia2n73cduw'






# # get current user's 50 playlists
# current_user_playlist_ids = getPlaylists(current_user, 0)
# # get the next 50 playlists
# current_user_playlist_ids2 = getPlaylists(current_user, 50)

# # get 100 tracks from those playlists
# current_user_track_ids = getTracks(current_user, current_user_playlist_ids, 100) #100 for everyone
# # get 25 tracks from those playlists
# current_user_track_ids2 = getTracks(current_user, current_user_playlist_ids2, 25) #25 for everyone

# # join both lists into the first list name
# current_user_playlist_ids.extend(current_user_playlist_ids2)
# current_user_track_ids.extend(current_user_track_ids2)


# print(len(current_user_track_ids))
# # get all features from each track
# current_user_tracks = getFeatures(current_user_track_ids, current_user)

# # print(len(current_user_tracks))
# current_user_tracks = pd.DataFrame(current_user_tracks, columns = ['user_id', 'artist', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo'])

# # current_user_averages = []
max_col_value = {'popularity': 100,'danceability':1,'acousticness':1,'energy':1,'instrumentalness':1,'loudness':-60,'speechiness':1}
# # current_user_variances = []

current_user_averages = [0.4382300339192106, 0.6568518347209374, 0.34813078211532533, 0.5577589577551649, 0.053833063731113164, 0.1443700740055504, 0.14644465001541782, 0.5645482048764167]
current_user_variances = [715.7459605018392, 0.02373772756834775, 0.09174929249884411, 0.040100934925131775, 0.03800893408124727, 15.365590780831603, 0.018815291676334906, 817.1962030521762]


# #start
# for column in current_user_tracks.columns:
#     if not(column == 'user_id') and not(column == 'artist'):
#         print('getting averages from ', column)
#         if column == 'tempo':
#             maxTempo = max(current_user_tracks['tempo'])
#             average = statistics.mean(current_user_tracks[column])
#             average_norms = average / maxTempo

#         else:
#             average = statistics.mean(current_user_tracks[column])
#             average_norms = average / max_col_value[column]

#         current_user_averages.append(average_norms)

#         variance = statistics.variance(current_user_tracks[column])
#         current_user_variances.append(variance)


# print(current_user_averages)
# print(current_user_variances)


# import sys
# sys.exit()
# #end



# normalize popularity...etc.
# Find average values for features the matter

# create dataset
# df = pd.DataFrame(current_user_tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
# df = pd.DataFrame(current_user_tracks, columns = ['popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo'])

# current_user_tracks.to_csv("current_user_songs.csv", sep = ',')

users = pd.read_csv("users.csv")
users = [x for x in users['users']]

print("LENGTH of USERS:", len(users))

#distances[]
# df = pd.DataFrame(users, columns=['users'])
# df.to_csv("users.csv", sep = ',')


distances = []
all_user_information = []

current_user_averages = numpy.array(current_user_averages)
current_user_variances = numpy.array(current_user_variances)

print("portion of the dataset length: ", len(users[start:end]))

i = start
for user in users[start:end]:
    # try:
    # Get track information for each added user through their 50 playlists
    print(str(i) + ": getting track information for " + user)
    playlist_ids = getPlaylists(user, 0)
    track_ids = getTracks(user, playlist_ids, 100) # 100 everyone
    tracks = getFeatures(track_ids, user)
    for track_info in tracks:
        all_user_information.append(track_info)
    tracks = pd.DataFrame(tracks, columns = ['user_id', 'artist', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo'])

    # Get average values for each feature
    user_averages = []
    user_variances = []

    for column in tracks.columns:
        if not(column == 'user_id') and not(column == 'artist'):
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
    print()
    # df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'],)
    # csv_name = user + ".csv"
    # df.to_csv(csv_name, sep = ',')

    # except:
    #     print(user + " has no songs")
    #     continue
    i += 1

all_user_information = pd.DataFrame(all_user_information, columns = ['user_id', 'artist', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo'])
all_user_information.to_csv("all_user_information.csv.zip", sep=',', compression="zip")

distances = pd.DataFrame(distances, columns=['user', 'averages_distance', 'variances_distance'])
distances.to_csv("distances.csv", index=False)