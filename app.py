
from flask import Flask,request, jsonify
import json

app=Flask(__name__)


# load the manga data from json file

with open('Data/data.json','r') as file:
    manga_data=json.load(file)

@app.route('/',methods=['GET'])
def get_all_manhua():
    return jsonify(manga_data)

@app.route('/<title>', methods=['GET'])
def get_manhua_by_title(title):
    for manga in manga_data:
        if manga['title'].lower() == title.lower():
            return jsonify(manga)
    return jsonify({"error": "Manga not found"}), 404


@app.route('/manga/<title>/chapters', methods=['GET'])
def get_chapters(title):
    for manga in manga_data:
        if manga['title'].lower() == title.lower():
            return jsonify(manga['chapters'])
    return jsonify({"error": "Manga not found"}), 404

@app.route('/manga/<title>/chapters/<chapter>', methods=['GET'])
def get_chapter(title, chapter):
    for manga in manga_data:
        if manga['title'].lower() == title.lower():
            if chapter in manga['chapters']:
                return jsonify(manga['chapters'][chapter])
            else:
                return jsonify({"error": "Chapter not found"}), 404
    return jsonify({"error": "Manga not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
