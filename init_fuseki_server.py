from clients.fuseki_server import FusekiServer

if __name__ == "__main__":
    init_data = open('./config/mergedTTLs.ttl').read()

    fuseki_server = FusekiServer()
    fuseki_server.update_dataset(init_data)
