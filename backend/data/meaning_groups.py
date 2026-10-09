"""Meaning identity, not a list of home-page cards.

Identical definitions share a key automatically. These reviewed equivalences
also join field-specific wording of the SAME concept. New distinct definitions
need no home-page registration. When rewording an existing concept, extend its
equivalence group (or retain an explicit meaningKey) during editorial review.
"""
import hashlib
import json
import re
import unicodedata
from pathlib import Path


def definition_key(definition):
    text = unicodedata.normalize('NFKC', definition).lower()
    text = re.sub(r'[^a-z0-9가-힣]', '', text)
    return 'meaning-' + hashlib.sha256(text.encode()).hexdigest()[:20]


def apply(entries):
    def key(entry):
        if entry.get('meaningKey'):
            return entry['meaningKey']
        return definition_key(entry['definition'])

    keys = {e['id']: key(e) for e in entries}
    parents = {k: k for k in keys.values()}

    def root(k):
        while parents[k] != k:
            parents[k] = parents[parents[k]]
            k = parents[k]
        return k

    groups = json.loads(Path(__file__).with_name('meaning-equivalences.json').read_text())['groups']
    for group in groups:
        # Match reviewed definitions, NEVER a whole headword: a future new sense
        # of PT, for example, must not be absorbed into presentation automatically.
        members = [definition_key(text) for text in group['definitions']]
        for k in members:
            parents.setdefault(k, k)
        roots = sorted({root(k) for k in members})
        for k in roots[1:]:
            parents[k] = roots[0]

    for e in entries:
        e['meaningKey'] = root(keys[e['id']])
    return entries
