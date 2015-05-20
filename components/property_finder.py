from nltk import ParentedTree
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet

from components.data_base import DataBase


class PropertyFinder(object):
    def __init__(self):
        self._stemmer = PorterStemmer()

    def __get_property_string_forms(self, property_subtree):
        words = stopwords.words('english')

        property_string_forms = set()
        property_string_forms.add((' '.join(property_subtree.leaves())).lower())
        property_string_forms.add((' '.join([self._stemmer.stem(word) for word in property_subtree.leaves()])).lower())
        property_string_forms.add((' '.join([word for word in property_subtree.leaves() if word not in words])).lower())
        property_string_forms.add((' '.join([self._stemmer.stem(word) for word in property_subtree.leaves() if word not in words])).lower())

        return property_string_forms

    def __fetch_from_wikibase(self, property_string):
        labels = DataBase().search_properties_name(property_string)
        if labels is None:
            return []
        return [label.lower() for label in labels]

    def __fetch_synonyms_and_hypernyms(self, property_string):
        words = set()
        synsets = wordnet.synsets(property_string)
        for synset in synsets:
            words.update([lemma.replace('_', ' ').lower() for lemma in synset.lemma_names()])
            for hypernym in synset.hypernyms():
                words.update([lemma.replace('_', ' ').lower() for lemma in hypernym.lemma_names()])
        return words

    def find_candidates(self, property_subtree):
        if not isinstance(property_subtree, ParentedTree):
            raise AttributeError

        candidates = set(self.__get_property_string_forms(property_subtree))

        new_candidates = set()
        for candidate in candidates:
            for label in self.__fetch_from_wikibase(candidate):
                new_candidates.add(label)
        candidates.update(new_candidates)

        new_candidates = set()
        for candidate in candidates:
            new_candidates.update(self.__fetch_synonyms_and_hypernyms(candidate))
        candidates.update(new_candidates)

        new_candidates = set()
        for candidate in candidates:
            for POS in [wordnet.ADJ, wordnet.ADV, wordnet.NOUN, wordnet.VERB]:
                morphy = wordnet.morphy(candidate, POS)
                if morphy is not None:
                    new_candidates.add(morphy)
        candidates.update(new_candidates)

        return candidates