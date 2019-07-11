from flask import Flask, abort
import markov

app = Flask(__name__)


supported_ngram_sizes = [3,4,5]
source_file = "./data/portmanteau-and-markov.txt"
seen = set()
gens = {
    n: iter(markov.MarkovGenerator(n, source_file, already_seen=seen))
    for n in supported_ngram_sizes
}

@app.route('/word/<int:ngram_size>')
def get_portmanteau(ngram_size):
    if ngram_size in supported_ngram_sizes:
        word = next(gens[ngram_size])
        print(f"N = {ngram_size}: SENDING '{word}'.")
        return word
    else:
        abort(404)
