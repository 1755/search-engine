import json
import urllib
from flask import Flask, request, render_template
from application import Application

app = Flask(__name__)
app.debug = True
search_app = Application()


@app.route('/', methods=['GET', 'POST'])
def index():
    submit = False
    question = ""
    answers = []
    answers_count = 0
    images_links = []
    image_api_ids = []

    if request.method == 'GET':
        return render_template('index.html',
                               answers=answers,
                               answers_count=answers_count,
                               question=question,
                               images_links=images_links,
                               submit=submit)

    try:
        question = request.form['question']
        submit = True
    except KeyError as e:
        return str(e)

    answers = search_app.get_answer(question)
    if len(answers) > 0:
        for answer in answers:
            for key in answer.data['statements']:
                if 'image' in key:
                    for value in answer.data['statements'][key]['values']:
                        image_api_ids.append(unicode(value['data']))

        params = {
            'action': 'query',
            'titles': '|'.join(['File:'+unicode(id) for id in image_api_ids]),
            'prop': 'imageinfo',
            'iiprop': '|'.join(['url', 'thumbmime', 'size', 'mime'][0:50]),
            'iiurlwidth': 250,
            'format': 'json',
        }
        url = 'http://commons.wikimedia.org/w/api.php' + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())
        try:
            for key in response['query']['pages']:
                page = response['query']['pages'][key]
                for imageinfo in page['imageinfo']:
                    images_links.append({
                        'thumb': imageinfo['thumburl'],
                        'full': imageinfo['url']
                    })
        except KeyError as e:
            pass

    return render_template('index.html',
                           answers=answers,
                           answers_count=len(answers),
                           question=question,
                           images_links=images_links,
                           submit=submit)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)