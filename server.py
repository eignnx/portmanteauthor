from flask import Flask, abort, render_template
import flask_cors
import sqlite3

import markov
from db_set import DbSet
import create_words_db
import utils

app = Flask(__name__)
flask_cors.CORS(app)

gens = {} # Stores markov word generator instances for a given ngram size and source text.
DB_FILE = "words.db"
supported_ngram_sizes = [3,4,5]
source_files = [
    "./static/data/portmanteau_and_markov.txt",
]


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')
  

@app.route('/word/<corpus>/<int:ngram_size>')
def get_portmanteau(corpus, ngram_size):
    if not ngram_size in supported_ngram_sizes:
        abort(404)
      
    word = next(gens[corpus][ngram_size])
    print(f"N = {ngram_size}, CORPUS = {corpus}: SENDING '{word}'.")
    return {
      "word": word,
      "ngram_size": ngram_size,
      "corpus": corpus,
    }


def build_markov():
  for source_file in source_files:
      corpus_name = utils.filename_from_path(source_file)
      seen = DbSet(DB_FILE, table=corpus_name, col="word")
      gens[corpus_name] = {
          n: iter(markov.MarkovGenerator(n, source_file, already_seen=seen))
          for n in supported_ngram_sizes
      }
    

if __name__ == "__main__":
  create_words_db.maybe_init()
  build_markov()
  app.run(host='0.0.0.0', port=8080)
