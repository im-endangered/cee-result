from flask import Flask, redirect, url_for, render_template, request
import csv
import os
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/result/<string:name>/<float:score>/<int:rank>')
def result(name, score, rank):
    return render_template('result.html', name=name.upper(), score=score, rank=rank)


app_root = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(app_root, 'data.csv')


def findScore(name):
    with open(csv_file_path, newline='', encoding='unicode_escape') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'].lower().replace(' ', '') == name.lower().replace(' ', ''):
                score = float(row['Score'])
                rank = int(row['Rank'])
                return (score, rank)
    return (0, 0)


@app.route('/check/')
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        res = findScore(name)
        return redirect(url_for('result', name=name, score=res[0], rank=res[1]))


if __name__ == '__main__':
    app.run(debug=True)
