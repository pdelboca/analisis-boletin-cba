import re
import codecs

from nltk.text import TokenSearcher as NLTKTokenSearcher

import iepy
iepy.setup(__file__)

from analisis_boletines_cba.preprocess.base import BaseNERRunner


class RegExpNERRunner(BaseNERRunner):

    def __init__(self, label, regexp, override=False):
        self.label = label
        self.regexp = regexp

        super(RegExpNERRunner, self).__init__(override)

    def run_ner(self, doc):
        entities = []
        tokens = doc.tokens
        searcher = TokenSearcher(tokens)
        for match in searcher.finditer(self.regexp):
            entity_oc = self.process_match(match)
            if type(entity_oc) == list:
                entities.extend(entity_oc)
            else:
                entities.append(entity_oc)
        return entities

    def process_match(self, match):
        name = ' '.join(match.group())
        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(name, kind, name, offset, offset_end)

        return entity_oc


class TokenSearcher(NLTKTokenSearcher):

    def __init__(self, tokens):
        # replace < and > inside tokens with \< and \>
        _raw = '><'.join(w.replace('<', '\<').replace('>', '\>') for w in tokens)
        #  preprend >< instead of < for easier token counting
        self._raw = '><' + _raw + '>'
        # super(TokenSearcher, self).__init__(tokens)

    def finditer(self, regexp):
        regexp = preprocess_regexp(regexp)

        i = re.finditer(regexp, self._raw)
        # last_start, last_end = 0, 0
        # token_start, token_end = 0, 0
        while True:
            try:
                m = next(i)
                start, end = m.span()
                # FIXME: do not count from the beggining
                # token_start = token_start  + self._raw[last_start:start].count('><')
                # token_end = token_end + self._raw[last_end:end].count('><')
                # last_start, last_end = start, end
                token_start = self._raw[:start].count('><')
                token_end = self._raw[:end].count('><')
                yield MatchObject(m, token_start, token_end)
            except:
                return


class MatchObject:

    def __init__(self, m, token_start, token_end):
        self.m = m
        self.all = m.group()
        self.all_start, self.all_end = m.span()
        self.token_start = token_start
        self.token_end = token_end

    def group(self, *args):
        result = self.m.group(*args)
        if result:
            return result[1:-1].split('><')
        else:
            return None

    def span(self, *args):
        start, end = self.m.span(*args)
        span_start = self.all[:start - self.all_start].count('<')
        span_end = self.all[:end - self.all_start].count('<')

        return (self.token_start + span_start, self.token_start + span_end)


def preprocess_regexp(regexp):
    # preprocess the regular expression
    regexp = re.sub(r'\s', '', regexp)
    # replace < and > only if not double (<< or >>):
    # FIXME: avoid matching \< and \>.
    regexp = re.sub(r'(?<!<)<(?!<)', '(?:<(?:', regexp)
    regexp = re.sub(r'(?<!>)>(?!>)', ')>)', regexp)
    # now, replace << >> with < > resp.
    regexp = re.sub(r'<<', '<', regexp)
    regexp = re.sub(r'>>', '>', regexp)
    # Replace . (if not preceded by \) with [^>]
    regexp = re.sub(r'(?<!\\)\.', '[^>]', regexp)

    return regexp


def tokenized_re(s):
    return '<' + '> <'.join(s.split()) + '>'


def options_re(options):
    options2 = []
    for o in options:
        options2.append(tokenized_re(o))
    result = '(' + ' | '.join(options2) + ')'
    return result


def options_file_re(filename):
    f = codecs.open(filename, encoding="utf8")
    options = f.read().strip().split('\n')
    f.close()
    return options_re(options)
