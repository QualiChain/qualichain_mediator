import rdflib
from bs4 import BeautifulSoup
from rdflib import Graph

from clients.dobie_client import dobie_second_version

job_description = {
    "tasks": [
        {
            "label": "95671c903a5b97a9",
            "jobDescription": "Classical cryptography: Substitution cryptosystems, Caesar, Vigenere, cryptanalysis methods. Perfect secrecy (Shannon), one-time pad. Semantic security, CPA, CCA, PCPA. Symmetric cryptography. Pseudorandomness, stream cryptosystems. Block cryptosystems: Feistel circuits, DES, AES, operation modes. Message authentication codes (MACs). Hash functions, salt, Merkle trees.Elements of number theory: divisibility, residue arithmetic, quadratic residues, Chinese remainder theorem. Elements of group theory: groups, rings, Legendre theorem. Euler's φ function. Prime number tests. Public key cryptography. RSA and Rabin cryptosystems, relation to factoring problem. The discrete logarithm problem, ElGamal cryptosystem. Diffie-Hellman key exchange. Digital signatures: RSA, DSS, blind signatures. Cryptographic protocols: secret sharing, zero knowledge proofs, identification. Elements of complexity theory: one-way functions. Applications: encrypted communications, electronic voting, attacks, crypto-currencies (bitcoin).The course contains (in addition to exercises) a project with a written report and presentation, linear programming, computer science, Computer Science, flask, mongodb, angularjs, angular.js, ravendb, rdbms, .net, c++, html5, autosar, jenkins, junit, websocket"
        }
    ]
}

testing_response = dobie_second_version(job_description)
# soup = BeautifulSoup(testing_response.text, "turtle")
# print(soup.find_all())

g = Graph()
g.parse(data=testing_response.text, format='turtle')
# ttl_grapg.serialize(output_path, format='xml')
SELECT_SPARQL_QUERY = """SELECT ?x ?y WHERE { ?x saro:frequencyOfMention ?y }"""
results = g.query(SELECT_SPARQL_QUERY)
list_of_saro_skills = [{row['x'].replace('http://w3id.org/saro/', ''): int(row['y'].title())} for row in results]
print(list_of_saro_skills)
# for row in g.query("SELECT ?x ?y WHERE { ?x saro:frequencyOfMention ?y }"):
#     print(row['y'].title())
#     break