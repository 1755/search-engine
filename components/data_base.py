from search_engine.components.data_base_providers.wikidata_provider import WikidataProvider


class Base(object):
    def search(self, query):
        provider = WikidataProvider()
        return provider.search(query)

    def get(self, id):
        provider = WikidataProvider()
        return provider.get(id)