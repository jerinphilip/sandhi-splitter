from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
from sandhisplitter.trie import Trie


class Model:
    def __init__(self, *args, **kwargs):
        # Load from existing model
        if "model" in kwargs.keys():
            self.clean_init(0, 0)
            self.load(kwargs["model"])
        # Create new model from depth and initial skip values
        elif "depth" in kwargs.keys() and "skip" in kwargs.keys():
            self.clean_init(kwargs["depth"], kwargs["skip"])

        # Error, obviously.
        else:
            raise ValueError

    def clean_init(self, k, i):
        """ Resets the object variables to start fresh."""
        self.left = Trie()
        self.right = Trie()
        self.initial_skip = i
        self.k = k

    def add_entry(self, word, split, locs):
        """ Training part, add entries to model. """
        flag = [False for i in range(len(word)+10)]
        for i in locs:
            flag[i] = True
        for i in range(1, len(word)-2):
            first, second = word[:i+1], word[i+1:]
            first = self.trim(first[::-1])
            second = self.trim(second)
            self.left.add_word(first, flag[i])
            self.right.add_word(second, flag[i])

        # Add the other pattern?
        start = self.trim(word)
        end = self.trim(word[::-1])
        self.left.add_word(end, True)
        self.right.add_word(start, True)

    def serialize(self):
        """serializes a model into a dictionary"""
        return {
                "k": self.k,
                "initial_skip": self.initial_skip,
                "left": self.left.serialize(),
                "right": self.right.serialize()
                }

    def load(self, serialized):
        """ loads a model serialized into a dictionary """
        self.k = serialized["k"]
        self.initial_skip = serialized["initial_skip"]
        self.left.load(serialized["left"])
        self.right.load(serialized["right"])

    def probable_splits(self, word):
        """ Find probable splits in a word """
        ps = []
        for i in range(2, len(word)-1):
            fi, si = max(0, i-self.k-1), min(len(word), i+self.k)
            first, second = word[fi:i], word[i:si]
            backwardk = first[::-1]
            forwardk = second
            P_lsp = self.left.smoothed_P_sp(backwardk, self.initial_skip)
            P_rsp = self.right.smoothed_P_sp(forwardk, self.initial_skip)

            # Averaging right now, this is hardcoded.
            threshold = 1.0
            # Can be adjusted if more tolerance is required.
            # Paper implements P_lsp * P_rsp > 0.5
            # The author of this code likes this better.
            if (P_lsp + P_rsp >= threshold):
                ps.append(i-1)
        return ps

    def trim(self, word):
        """ reduce word to k characters. """
        return word[:min(len(word), self.k)]
