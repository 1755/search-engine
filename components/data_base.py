from data_base_providers.wikidata_provider import WikidataProvider


class DataBase(object):
    """
    Database.
    @todo: docme
    """

    def search(self, query):
        """ Get structured entity by text query.

         :type query: str
         :param query: text query. If, for example, you want
            get some data for Moscow you can call:

                search("Moscow")

         :return: Entity which corresponded to query
         :rtype: dict
        """

        provider = WikidataProvider()
        return provider.search(query)

    def search_properties_name(self, query):
        provider = WikidataProvider()
        return provider.search_properties_name(query)

    def get(self, entity_id):
        """ Get structured entity by some identifier.
         :type entity_id: str
         :param entity_id: Identifier of entity

         :return: Entity which corresponded to id
         :rtype: dict
        """

        provider = WikidataProvider()
        return provider.get(entity_id)