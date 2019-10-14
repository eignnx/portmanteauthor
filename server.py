from flask import Flask, abort
<<<<<<< HEAD
=======
import flask_cors
>>>>>>> 4912090f4a78b2d333c933de9cb15a0b09e70232
import sqlite3

import markov
from db_set import DbSet
import utils

app = Flask(__name__)
flask_cors.CORS(app)

conn = sqlite3.connect("test.db")
c = conn.cursor()

DB_FILE = "words.db"


supported_ngram_sizes = [3,4,5]
source_files = [
    "./data/portmanteau_and_markov.txt",
]

gens = {}


for source_file in source_files:
    corpus_name = utils.filename_from_path(source_file)
    seen = DbSet(DB_FILE, table=corpus_name, col="word")
    gens[corpus_name] = {
        n: iter(markov.MarkovGenerator(n, source_file, already_seen=seen))
        for n in supported_ngram_sizes
    }


@app.route('/word/<corpus>/<int:ngram_size>')
def get_portmanteau(corpus, ngram_size):
    if ngram_size in supported_ngram_sizes:
        word = next(gens[corpus][ngram_size])
        print(f"N = {ngram_size}, CORPUS = {corpus}: SENDING '{word}'.")
        return word
    else:
        abort(404)

@app.route('/portmantauthor/register_user/<username>')
def register_user(username):
    return None

@app.route("/")
def hello():
    return "WORKING"


if __name__ == "__main__":
    app.run(
        #ssl_context="adhoc",
        port=7000,
    )

