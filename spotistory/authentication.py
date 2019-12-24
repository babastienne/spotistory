import json
import toml
from flask import Flask, request, redirect, render_template
import requests
from urllib.parse import quote

app = Flask('authentication')


def init(conf, conf_file):
    global config, config_file, auth_query_parameters, synchronized
    config = conf
    config_file = conf_file
    if config['spotify']['redirect_uri'] == "":
        config['spotify']['redirect_uri'] = 'http://{}:{}/callback/q'.format(config['server']['host'], config['server']['port'])
    scope = 'user-library-read user-read-recently-played playlist-modify-public playlist-modify-private'

    auth_query_parameters = {
        'response_type': 'code',
        'redirect_uri': config['spotify']['redirect_uri'],
        'scope': scope,
        'client_id': config['spotify']['client_id']
    }


@app.route('/')
def index():
    url_args = '&'.join(['{}={}'.format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = '{}/?{}'.format(config['spotify']['auth_url'], url_args)
    return redirect(auth_url)


@app.route('/callback/q')
def callback():
    auth_token = request.args['code']
    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': config['spotify']['redirect_uri'],
        'client_id': config['spotify']['client_id'],
        'client_secret': config['spotify']['client_secret'],
    }
    post_request = requests.post(config['spotify']['token_url'], data=code_payload)

    response_data = json.loads(post_request.text)
    config['spotify']['access_token'] = response_data['access_token']
    config['spotify']['refresh_token'] = response_data['refresh_token']

    return redirect('/synchro')


@app.route('/synchro')
def synchronize():
    with open(config_file, 'w') as myfile:
        toml.dump(config, myfile)
    stop_server()
    return render_template('index.html')


def launch():
    app.run(debug=False, port=config['server']['port'], host=config['server']['host'])


def stop_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
