import flask
import os


app = flask.Flask(__name__)
app.config["DEBUG"] = True

VIDEO_KEYWORD = '{{video}}'
IMAGE_KEYWORD = '{{image}}'
EXTENSION_KEYWORD = '{{extension}}'
NEXT_KEYWORD = '{{next}}'

current_path = os.path.dirname(os.path.realpath(__file__))
SLIDES_DIR = 'slides'
SLIDES_PATH = os.path.join(current_path, SLIDES_DIR)

VIDEO_TEMPLATE = os.path.join(current_path, 'video.html')
IMAGE_TEMPLATE = os.path.join(current_path, 'image.html')

video_filetypes = ['mp4']
image_filetypes = ['png', 'jpg', 'gif']
files = []


def list_files():
    global files

    files = []

    for item in os.listdir(SLIDES_PATH):
        item_path = os.path.join(SLIDES_PATH, item)
        extension = item.split('.')[-1]

        if os.path.isfile(item_path) and ((extension in video_filetypes) or (extension in image_filetypes)):
            files.append(item)

    files = sorted(files)


def get_response_for(filename):
    extension = filename.split('.')[-1]
    current_id = files.index(filename)

    if (len(files) - 1) > current_id:
        next_id = current_id + 1
    else:
        next_id = 0

    next_file = files[next_id]

    if extension in video_filetypes:
        f = open(VIDEO_TEMPLATE, 'r')
        content = f.read()
        f.close()

        content = content.replace(VIDEO_KEYWORD, '{}/{}'.format(SLIDES_DIR, filename))
        content = content.replace(EXTENSION_KEYWORD, '{}'.format(extension))
        content = content.replace(NEXT_KEYWORD, '{}'.format(next_file))

        return content

    elif extension in image_filetypes:
        f = open(IMAGE_TEMPLATE, 'r')
        content = f.read()
        f.close()

        content = content.replace(IMAGE_KEYWORD, '{}/{}'.format(SLIDES_DIR, filename))
        content = content.replace(NEXT_KEYWORD, '{}'.format(next_file))

        print('RETURNING:', content)
        return content
    else:
        flask.abort(404)


@app.route('/', methods=['GET'])
def home():
    list_files()

    return get_response_for(files[0])


@app.route('/<page>')
def profile(page):
    list_files()

    print('PAGE', page)

    if page in files:
        return get_response_for(page)
    else:
        print('No file: {} in files: {}'.format(page, files))
        flask.abort(404)


@app.route('/slides/<file>')
def slides(file):
    list_files()

    if file in files:
        try:
            file_path = os.path.join(SLIDES_PATH, file)
            return flask.send_file(file_path, attachment_filename=file)
        except Exception as e:
            return str(e)

app.run()
