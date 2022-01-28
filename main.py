url = "https://api.telegram.org/bot5138197793:AAEZHTrnB3zwevc1vE9EnXE905DubaNl2qw/"

import requests
import json
from flask import Flask
from flask import request
from flask import Response
import os

application = Flask(__name__)


def get_updates():
    x = requests.get(url + 'getUpdates')
    return x.json()


def get_lupdate(all):
    return all['result'][-1]


def get_chatid(up):
    return up['message']['chat']['id']


def send_mess(chat_id, text):
    send = {
        'chat_id': chat_id,
        'text': text
    }
    x = requests.post(url + 'sendMessage', send)
    return x


@application.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        messs = request.get_json()
        chat_id = get_chatid(messs)
        text = messs['message'].get('text', '')
        if text == '/start':
            send_mess(chat_id, 'Hello welcome')
            send_mess(chat_id, 'if you want add your list write ( 1 movie_name its_mark )')
            send_mess(chat_id, 'if you want add your favorite list write ( 2 movie_name its_mark )')
            send_mess(chat_id, 'if you want see your list write ( 3 )')
            send_mess(chat_id, 'if you want see your favorite list write ( 4 )')
            send_mess(chat_id, 'if you want get information about movies write ( 5 )')

        if 1 in text:
            movies = read_json_file()
            user = messs['message']['from']['username']
            if user not in movies.keys():
                movies[user] = []
            new_user = text.split(maxsplit=1)[1]
            movies[user].append(new_user)
            write_json_file(movies)
            send_mess(chat_id, 'your movie is added to your list')


        elif 2 in text:
            favorite_movies = read_json_file()
            user = messs['message']['from']['username']
            if user not in favorite_movies.keys():
                favorite_movies[user] = []
            new_user = text.split(maxsplit=1)[1]
            favorite_movies[user].append(new_user)
            write_json_file(favorite_movies)
            send_mess(chat_id, 'your movie is added to your favorite list')


        elif text == 3:
            movies = read_json_file()
            user = messs['message']['from']['username']
            if user not in movies.keys():
                send_mess(chat_id, 'you have no movie')
            else:
                for i in movies[user]:
                    send_mess(chat_id, i)


        elif text == 4:
            favorite_movies = read_json_file()
            user = messs['message']['from']['username']
            if user not in favorite_movies.keys():
                send_mess(chat_id, 'you have no movie')
            else:
                for i in favorite_movies[user]:
                    send_mess(chat_id, i)


        elif text == 5:
            movie_list = [
                'Hotwired in Suburbia, genre: Exciting, Production Year: 2020, Score: 4, Actors: Zoe_Belkin Samantha_Helt Tyler_Hynes',
                'The Fosters S01, genre: Romantic, Production Year: 2013, Score: 7.9, Actors: Teri_Polo, Sherri_Saum, Hayden_Byerly',
                'TRANSFORMERS, genre: action, Production Year: 2007, Score: 7, Actors: Shia_LaBeouf, Megan_Fox, Josh_Duhamel',
                'In July Im Juli, genre: Romantic_Comedy, Production Year: 2000, Score: 7.7, Actors: Moritz_Bleibtreu, Idil_Uner, Mehmet_Kurtulus',
                'BLITHE SPIRIT, genre: Romantic_Comedy, Production Year: 2020, Score: 5.4, Actors: Dan_Stevens, Isla_Fisher, Leslie_Mann',
                'SCREAM 4, genre: Scary, Production Year: 2011, Score: 6.2, Actors: Neve_Campbell, Courteney_Cox, David_Arquette']

            for i in movie_list:
                send_mess(chat_id, i)
        else:
            send_mess(chat_id, 'try again')
        return Response('ok', status=200)

    else:
        return '<h1>My_Bot</h1>'


def write_json_file(dade, name="movielist.json"):
    with open(name, 'w') as goal:
        json.dump(dade, goal, indent=4, ensure_ascii=False)


def read_json_file(name="movielist.json"):
    with open(name, 'r') as goal:
        dade = json.load(goal)
    return dade


# while True:
#   dade = get_updates()
#  lupdate = get_lupdate(dade)
# send_mess(get_chatid(lupdate),'hello')

write_json_file({})
application.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))