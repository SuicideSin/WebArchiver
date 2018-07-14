import functools
import threading

import flask

import webarchiver

app = flask.Flask(__name__)


@app.route('/')
def main():
    return flask.render_template('main.html', sort=sort)


@app.route('/config')
@app.route('/configuration')
def configuration():
    return flask.render_template('configuration.html')


@app.route('/job')
@app.route('/jobs')
def jobs():
    print(server.job_identifiers)
    return flask.render_template('jobs.html', jobs=server.job_identifiers)


@app.route('/job/<identifier>')
@app.route('/jobs/<identifier>')
def job(identifier):
    return flask.render_template('job.html', identifier=identifier)


def run(port, server=None):
    globals()['server'] = server
    globals()['sort'] = 'stager' \
        if isinstance(server, webarchiver.server.StagerServer) else 'crawler'
    app.run(port=port)


def create(*args, **kwargs):
    dashboard = threading.Thread(target=run, args=args, kwargs=kwargs)
    dashboard.daemon = True
    dashboard.start()

