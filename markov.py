import random
from collections import defaultdict
from typing import Optional, Set

from utils import sliding_windows


class MarkovGenerator:
    DEBUG = False
    MAX_LENGTH = 20
    ENSURE_NOT_SUBSET = False
    ENSURE_NOT_IN_CORPUS = True
    MAX_ATTEMPTS = 10_000

    def __init__(self, ngram_size: int, corpus_file: str, already_seen: Optional[Set[str]] = None):
        self.n = ngram_size
        self.probabilities = defaultdict(list)
        self.src_words = set()
        self.starters = []
        self.already_seen = set() if already_seen is None else already_seen
        with open(corpus_file, "r") as f:
            for line in f:
                self.add_phrase(line)
                self.src_words.add(line.strip())

    def add_phrase(self, line: str):
        try:
            first = True
            for window in sliding_windows(line, self.n + 1):
                (*ngram, nxt) = window
                text = "".join(ngram)
                if first:
                    self.starters.append(text)
                    first = False
                self.probabilities[text].append(nxt)
        except AssertionError:
            pass  # Forget about the word if it's too short

    def _raw_generated_word(self):
        """
        Generates text with the markov chain algorithm, but doesn't check for
        uniqueness in the corpus.
        """
        text: str = random.choice(self.starters)
        while not text.endswith("\n"):
            last_ngram = text[-self.n:]
            next_letter = random.choice(self.probabilities[last_ngram])
            text += next_letter
            if len(text) > self.MAX_LENGTH:
                return None  # Too long, possibly stuck.
        return text.rstrip()  # Strip the \n from the end.

    def subset_of_src_word(self, word):
        for src_word in self.src_words:
            word_low = word.lower()
            src_word_low = src_word.lower()
            if word_low in src_word_low or src_word_low in word_low:
                return True
        return False

    def no_good(self, word):
        return (
            word is None
            or word in self.already_seen
            or (self.ENSURE_NOT_SUBSET and self.subset_of_src_word(word))
            or (self.ENSURE_NOT_IN_CORPUS and word in self.src_words)
        )

    def __iter__(self):
        streak = 0
        while True:
            word = self._raw_generated_word()
            if self.no_good(word):
                streak += 1
                if streak > self.MAX_ATTEMPTS:
                    raise Exception("Too many failed attempts to generate a word!")
            else:
                if self.DEBUG:
                    print("\tUNORIGINALITY STREAK:", streak)
                streak = 0
                self.already_seen.add(word)
                yield word


if __name__ == '__main__':
    import sys
    from collections import deque

    if len(sys.argv) == 2:
        [_exe, data_file] = sys.argv
        print(f"Data source: '{data_file}'")
        MarkovGenerator.ENSURE_NOT_SUBSET = False
        MarkovGenerator.ENSURE_NOT_IN_CORPUS = True
    else:
        print("Please specify a source file!")
        sys.exit(1)

    gen_count = 0
    favorites = set()
    history = deque(maxlen=10)
    already_seen = set()

    MarkovGenerator.DEBUG = True
    while True:
        resp = input("Enter a number for N or [Q] to quit: ").lower()
        if not resp.isnumeric(): break
        n = int(resp)
        markov = MarkovGenerator(n, data_file, already_seen)
        gen = iter(markov)
        while True:

            word = next(gen)
            history.append(word)
            print(word)
            gen_count += 1

            resp = input(f"N = {n}: Press [ENTER] for another word, or [B] for back: ")
            if resp.lower() == "eval":
                print(eval(input("EVAL> ")))
                resp = input(f"N = {n}: Press [ENTER] for another word, or [B] for back: ")
            elif resp.startswith("^") or resp.startswith("+"):
                i = len(resp)
                try:
                    prev = history[-i]
                    favorites.add(prev)
                    print()
                    print(f"\tAdded '{prev}' to favorites.")
                    print()
                except IndexError:
                    print()
                    print(f"\tIndex out of bounds: {resp}")
                    print(f"\tOnly {len(history)} words in history!")
                    print()
                continue

            if resp == "": continue
            else: break

    if favorites:
        print()
        print(f"Words generated:   {gen_count}")
        print(f"Percent favorited: {100 * len(favorites)/gen_count:.3}%")
        print()
        print("Your favorite words were:")
        for word in favorites:
            print("-", word)
        print()

        msg = "Enter a file to append favorites to [ENTER to skip]: "
        savefile = input("OPTIONAL: " + msg)
        if savefile.strip():
            with open(savefile, "a+") as f:
                for word in favorites:
                    print("-", word, file=f)
            print(f"Saved to '{savefile}'.")
