import json
import calendar
import locale

from os import listdir
from os.path import isfile, join

locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')


def pretty_print(tracks):
    for i, l in enumerate(tracks):
        print(str(i + 1) + '. ' + l[0])


def keep(track):
    return track["msPlayed"] > 5000 and track["endTime"].startswith('2021')


def prepare_2021_data():
    data_files = ['data/' + f for f in listdir('data/') if isfile(join('data/', f))]
    data = []
    for f in data_files:
        with open(f, "r") as read_file:
            data.extend(json.load(read_file))
    return list(filter(keep, data))


def top_10_artist(data):
    counter_artist = {}
    for track in data:
        key = track["artistName"]
        try:
            counter_artist[key] += 1
        except KeyError:
            counter_artist[key] = 1
    top_artist = sorted(counter_artist.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 artists:")
    pretty_print(top_artist[:10])
    print()


def top_10_track(data):
    counter_artist_track = {}
    for track in data:
        key = track["artistName"] + ': ' + track["trackName"]
        try:
            counter_artist_track[key] += 1
        except KeyError:
            counter_artist_track[key] = 1
    top_track = sorted(counter_artist_track.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 tracks:")
    pretty_print(top_track[:10])
    print()


def top_10_track_month(data):
    month = {}
    for track in data:
        month_no = track["endTime"].split("-")[1]
        try:
            month[month_no].extend([track])
        except KeyError:
            month[month_no] = [track]
    for m in month:
        tracks = month[m]
        month_tracks = {}
        for track in tracks:
            key = track["artistName"] + ': ' + track["trackName"]
            try:
                month_tracks[key] += 1
            except KeyError:
                month_tracks[key] = 1
        top_track = sorted(month_tracks.items(), key=lambda x: x[1], reverse=True)
        print(calendar.month_abbr[int(m)])
        pretty_print(top_track[:10])
        print()


data_2021 = prepare_2021_data()

top_10_artist(data_2021)
top_10_track(data_2021)
top_10_track_month(data_2021)
