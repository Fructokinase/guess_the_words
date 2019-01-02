import sys
import string
import random
import itertools

class WordGenerator(object):

    def __init__(self, requirement=10):
        self._min_words = requirement

    def generate(self):
        """
        All word generators should provide a generate method that
        generates
        Returns: set(of str)
        """
        pass

class DumbWordGenerator(WordGenerator):
    """
    Dumb word generator that uses words from /usr/share/dict/words that are
    3 ~ 6 words to generate a set of words

    The algorithm is simple
    First, find 50 seed words. Seed words are words that are six letters, and
    those six letters will be used to generate the rest of the words for that seed
    """

    NUM_SEEDS = 50

    def _seed_words(self, seed):
        """
        Given a seed, generate words that can be made from the letter set
        of the seed
        """
        valid_words = set()
        for i in range(3, 7):
            for _tuple in itertools.permutations(list(seed), i):
                if ''.join(_tuple) in self._word_set:
                    valid_words.add(''.join(_tuple))
        return valid_words

    def _score_word_set(self, word_set):
        """
        4 letterd words are common and therefore the best words for the game
        3 lettered words come next
        5 lettered words are a bit harder
        6 lettered words should be mixed in occasionally
        Returns: int - score of the word set
        """
        if len(word_set) < self._min_words:
            return -1
        len_to_score = dict({
            3: 3,
            4: 4,
            5: 2,
            6: 1
        })
        return sum([ len_to_score[len(word)] for word in word_set ])

    def _read_source(self):
        """
        Reads the source texts
        Sets:
            self._word_set: set(str) - set of all words to be used
            self._seeds listof str - list of seeds
        """
        with open('word_source.txt', 'r') as handle:
            self._word_set = set([
                line.strip() for line in handle.readlines()
            ])

        with open('six_lettered_word_source.txt', 'r') as handle:
            self._seeds = random.choices(
                [ line.strip() for line in handle.readlines() ],
                k=self.NUM_SEEDS
            )

    def generate(self):

        self._read_source()

        max_score = 0
        res = None
        letters = None
        for seed in self._seeds:
            if len(set(list(seed))) < 6: continue # bad seed
            seeded_word_set = self._seed_words(seed)
            score = self._score_word_set(seeded_word_set)
            max_score = max(score, max_score)
            if max_score == score:
                res = seeded_word_set
                res.add(seed)
                letters = list(seed)
        print(res)
        return letters, res


class Game(object):

    def __init__(self, generator_cls=DumbWordGenerator):
        self._generator = generator_cls()
        self._words = self._generate_words()
        self._words_guessed = set()

    def _generate_words(self):
        """
        Returns:
            listof str - list of words that will be used in the game
        Sets:
            self_letters - letters that the generated words uses
            self._num_words - number of words
        """
        self._letters, words = self._generator.generate()
        self._num_words = len(words)
        return list(words)

    def _update_guessed_word(self, word):
        self._words_guessed.add(word)

    def _process_word(self, word):
        if word in self._words:
            self._update_guessed_word(word)

    def reveal(self):
        """
        Reveals the solution by setting the words guessed to the solution
        Returns: None
        """
        self._words_guessed = self._words

    def _validate_word(self, word):
        """
        A word is valid if it is a string and it can be composed from self._letters
        Args:
            word(str) - word to be validated against
        Returns: bool
        """
        return type(word) == type('a') and set(self._letters) == set(list(word))

    def tick(self, word):
        """
        """
        if not self._validate_word(word): return False
        self._process_word(word.lower())
        return True

    def player_has_won(self):
        """
        The player has won if the number of words guessed is
        the total number of words to be guessed
        Returns: bool
        """
        return len(self._words_guessed) == self._num_words


    def print(self):
        """
        Prints the game board
        If the word has been guessed, print the word,
        Otherwise, print a series of underscores
        """

        def format_guessed_word(word):
            return ' '.join(list(word))

        def format_blank_word(word):
            return ' '.join(list('_' * len(word)))

        print('\n' + "Board" + '=' * 75)
        for word in self._words:
            word_str = format_guessed_word(word) \
                if word in self._words_guessed \
                else format_blank_word(word)
            print(word_str)
        print("{}/{} words remaining".format(self._num_words - len(self._words_guessed),self._num_words))
        print('=' * 80 + '\n')
