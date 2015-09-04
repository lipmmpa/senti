
import unicodedata

import numpy as np
from sklearn.base import BaseEstimator

__all__ = ['Elongations']


class Elongations(BaseEstimator):
    '''
    Proportion of tokens with elongated letters.
    '''

    @staticmethod
    def is_vowel(c):
        return c in 'aeiou'

    @staticmethod
    def is_letter(c):
        return unicodedata.category(c)[0] == 'L'

    @staticmethod
    def is_elongated(token, condition=None):
        if len(token) >= 3:
            condition = condition or (lambda x: True)
            prevprev, prev = token[:2]
            for i in range(2, len(token)):
                char = token[i]
                if condition(char) and char == prev and char == prevprev:
                    return True
                prevprev, prev = prev, char
        return False

    def fit(self, docs, y=None):
        return self

    def transform(self, docs):
        vecs = []
        for doc in docs:
            vec = np.array([
                sum(self.is_elongated(t, self.is_vowel) for t in doc),
                sum(self.is_elongated(t, self.is_letter) for t in doc),
                sum(map(self.is_elongated, doc)),
            ])/len(doc)
            vecs.append(vec)
        return np.vstack(vecs)