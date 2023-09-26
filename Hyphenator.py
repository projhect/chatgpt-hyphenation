# Source: https://github.com/jfinkels/hyphenate

# hyphenate.py - hyphenate English words
#
# This file is part of Hyphenate. The authors of Hyphenate abandon all
# claims to copyright, and dedicate it to the public domain.
"""Hyphenation of English words.

This module contains the main Hyphenation algorithm, originally due to
Frank Liang. The :func:`hyphenate_word` function takes a string as input
and returns a list of strings representing the parts of the word between
which hyphens can be placed.

"""
import re

__version__ = '1.1.1.dev0'


class Hyphenator:
    """An object that hyphenates based on pre-computed patterns.

    `patterns` is a string of whitespace-separated patterns, each of
    which is a string of characters the form ``a1bc3d4``.

    `exceptions` is a string of whitespace-separated hyphenated strings
    of the form ``as-so-ciate``. When this object is asked to hyphenate
    one of these words, it uses the given hyphenation instead of the
    hyphenation that would have been computed by the standard algorithm.

    """

    def __init__(self, patterns, exceptions=''):
        self.tree = {}
        for pattern in patterns.split("\n"):
            self._insert_pattern(pattern)

        self.exceptions = {}
        for ex in exceptions.split("\n"):
            # Convert the hyphenated pattern into a point array for use later.
            points = [0] + [int(h == '-') for h in re.split(r"[a-z]", ex)]
            self.exceptions[ex.replace('-', '')] = points

    def _insert_pattern(self, pattern):
        # Convert the a pattern like 'a1bc3d4' into a string of chars 'abcd'
        # and a list of points [ 0, 1, 0, 3, 4 ].
        chars = re.sub('[0-9]', '', pattern)
        points = [int(d or 0) for d in re.split("[^\d]", pattern)]

        # Insert the pattern into the tree.  Each character finds a dict
        # another level down in the tree, and leaf nodes have the list of
        # points.
        t = self.tree
        for c in chars:
            if c not in t:
                t[c] = {}
            t = t[c]
        t[None] = points

    def hyphenate_word(self, word):
        """ Given a word, returns a list of pieces, broken at the possible
            hyphenation points.
        """
        # Short words aren't hyphenated.
        if len(word) <= 4:
            return [word]
        # If the word is an exception, get the stored points.
        if word.lower() in self.exceptions:
            points = self.exceptions[word.lower()]
        else:
            work = '.' + word.lower() + '.'
            points = [0] * (len(work)+1)
            for i in range(len(work)):
                t = self.tree
                for c in work[i:]:
                    if c in t:
                        t = t[c]
                        if None in t:
                            p = t[None]
                            for j, p_j in enumerate(p):
                                points[i+j] = max(points[i+j], p_j)
                    else:
                        break
            # No hyphens in the first two chars or the last two.
            points[1] = points[2] = points[-2] = points[-3] = 0

        # Examine the points to build the pieces list.
        pieces = ['']
        for c, p in zip(word, points[2:]):
            pieces[-1] += c
            if p % 2:
                pieces.append('')
        return pieces
