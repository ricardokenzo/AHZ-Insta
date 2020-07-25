import subprocess
import json
import requests
import datetime
import instagram_scraper
import werkzeug
import werkzeug.utils
from app import app
from flask import Flask, flash, request, redirect, render_template
import shutil

@app.route('/')
def upload_form():
    return render_template('upload.html')
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/scraper', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        
        username = request.form['username']
        number = request.form['number']

        subprocess.run(["instagram-scraper", username,"-t", "none","-m", number, "--media-metadata"])

        def format(element):
            feed = {}
            feed["description"] = element["edge_media_to_caption"]["edges"][0]["node"]["text"]
            feed["source"] = element["username"]
            feed["source_url"] = element["display_url"]
            feed["file"] = element["display_url"]
            return feed
        with open(username + '/' + username + '.json', encoding = 'utf-8') as json_data:

            data = json.load(json_data)

            result = map(format, data["GraphImages"])
            result = list(result)
            payload = {"feeds": result}
            r = requests.post('', json=payload)
            print(r.text)

        shutil.rmtree(username, ignore_errors=False, onerror=None)

        flash('File successfully uploaded')
        return redirect('/success')


if __name__ == "__main__":
    app.run(debug = True)