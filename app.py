import re
import random
from flask import Flask, render_template

app = Flask(__name__)


def get_str_data_info(data_string):
    tiktoks_info = []
    for item in data_string:
        tiktok_id = int(re.search(r'\D+(\d+)', item).group(1))
        author_name = re.search(r'uniqueId\': \'([^\']+)', item).group(1)
        likes_count = int(re.search(r'diggCount\': (\d+)', item).group(1))
        tiktoks_info.append({'tiktok_id': tiktok_id,
                             'author_name': author_name,
                             'likes_count': likes_count})
    return tiktoks_info


def get_sad_tiktoks():
    sad_tiktoks = []
    with open('sad.txt') as f:
        for line in f.readlines():
            author, id = line.split()
            sad_tiktoks.append({'author_name': author, 'tiktok_id': id})
    return sad_tiktoks


def get_tiktoks():
    with open('tiktoks.txt', errors="ignore") as file:
        data_string = file.readlines()
    return get_str_data_info(data_string)


tiktoks = get_tiktoks()


@app.route('/', methods=['get'])
def trading_page():
    popit = random.choice(tiktoks)
    tier = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
    img = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
    tradability = ['tradable', 'non-tradable1', 'non-tradable2']
    random.shuffle(tradability)
    return render_template('index.html', tier=tier, img=img, info=popit, tradability=tradability)


@app.route('/decline')
def decline_page():
    info = random.choice(get_sad_tiktoks())
    return render_template('decline-outcome.html', info=info)


@app.route('/agree')
def agree_page():
    return render_template('agree-outcome.html')


if __name__ == '__main__':
    app.run()