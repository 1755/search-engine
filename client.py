from corenlp import jsonrpc
import json


class StanfordNLP:
    def __init__(self):
        self.server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
                                  jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))

    def parse(self, text):
        return json.loads(self.server.parse(text))

