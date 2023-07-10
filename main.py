from flask import Flask, request, render_template, jsonify
from src.get_graph import get_graph, get_repository_names, get_years, get_months, get_min_graph

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        names = get_repository_names()
        return render_template('index.html', names=names)
    if request.method == 'POST':
        data = request.json
        return get_graph(data['repository'], data['year'], data['month'])
    else:
        raise RuntimeError('Unknown op.')


@app.route('/years', methods=['POST'])
def years():
    data = request.json
    repository = data['repository']
    years = get_years(repository)
    return jsonify({'years': years})


@app.route('/months', methods=['POST'])
def months():
    data = request.json
    repository = data['repository']
    year = data['year']
    months = get_months(repository, year)
    return jsonify({'months': months})


@app.route('/point', methods=['POST'])
def point():
    data = request.json
    return get_min_graph(data['repository'], data['year'], data['month'], data['id'], data['kind'])


if __name__ == '__main__':
    app.run()
