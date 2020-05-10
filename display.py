#!/usr/bin/python3

import flask
import os
import time


app = flask.Flask(__name__)
app.config["DEBUG"] = True

VIDEO_KEYWORD = '{{video}}'
IMAGE_KEYWORD = '{{image}}'
EXTENSION_KEYWORD = '{{extension}}'
NEXT_KEYWORD = '{{next}}'
MSG_KEYWORD = '{{message}}'

DELIMITER = '----'

current_path = os.path.dirname(os.path.realpath(__file__))
SLIDES_DIR = 'slides'
SLIDES_PATH = os.path.join(current_path, SLIDES_DIR)

VIDEO_TEMPLATE = os.path.join(current_path, 'video.html')
IMAGE_TEMPLATE = os.path.join(current_path, 'image.html')

video_filetypes = ['mp4']
image_filetypes = ['png', 'jpg', 'gif']
files = []
messages = []

if not os.path.isdir(SLIDES_PATH):
    os.mkdir(SLIDES_PATH)


def list_files():
    global files
    global messages

    files = []
    messages = []
    msg_file = None

    for item in os.listdir(SLIDES_PATH):
        item_path = os.path.join(SLIDES_PATH, item)
        extension = item.split('.')[-1]

        if os.path.isfile(item_path) and ((extension in video_filetypes) or (extension in image_filetypes)):
            files.append(item)

        if os.path.isfile(item_path) and ('txt' in extension):
            msg_file = item_path

    if msg_file is not None:
        f = open(msg_file, 'r')
        messages = f.readlines()
        f.close()

    files = sorted(files)


def get_response_for(filename):
    extension = filename.split('.')[-1]
    current_id = files.index(filename)
    file_count = len(files)
    msg_count = len(messages)

    if (file_count - 1) > current_id:
        next_id = current_id + 1
    else:
        next_id = 0

    filename = '{}{}{}'.format(int(time.time()), DELIMITER, filename)
    next_file = '{}{}{}'.format(int(time.time()), DELIMITER, files[next_id])

    try:
        msg_id = current_id % msg_count
        message = messages[msg_id].replace('\n', '')
    except:
        message = ''

    if extension in video_filetypes:
        f = open(VIDEO_TEMPLATE, 'r')
        content = f.read()
        f.close()

        content = content.replace(VIDEO_KEYWORD, '{}/{}'.format(SLIDES_DIR, filename))
        content = content.replace(EXTENSION_KEYWORD, '{}'.format(extension))

    elif extension in image_filetypes:
        f = open(IMAGE_TEMPLATE, 'r')
        content = f.read()
        f.close()

        content = content.replace(IMAGE_KEYWORD, '{}/{}'.format(SLIDES_DIR, filename))

    else:
        content = None
        flask.abort(404)

    content = content.replace(NEXT_KEYWORD, '{}'.format(next_file))
    content = content.replace(MSG_KEYWORD, '{}'.format(message))

    return content


@app.route('/', methods=['GET'])
def home():
    list_files()

    return get_response_for(files[0])


@app.route('/<page>')
def profile(page):
    list_files()

    page_piece = page.split(DELIMITER)
    if len(page_piece) > 1:
        page = page_piece[1]

    if page in files:
        return get_response_for(page)
    else:
        print('No file: {} in files: {}'.format(page, files))
        flask.abort(404)


@app.route('/slides/<file>')
def slides(file):
    file_piece = file.split('----')
    if len(file_piece) > 1:
        file = file_piece[1]

    try:
        file_path = os.path.join(SLIDES_PATH, file)
        return flask.send_file(file_path, attachment_filename=file)
    except Exception as e:
        return str(e)


@app.route('/pwroff')
def pwroff():
    os.system('shutdown -h now')
    return 'OK'


if __name__ == '__main__':
    app.run('0.0.0.0', 8888, threaded=True)
