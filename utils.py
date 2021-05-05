import re
from os import path
import pandas as pd
from bs4 import BeautifulSoup

import json

import requests
from rdflib import Graph

from clients.postgres_client import PostgresClient
from settings import QUERY_EXECUTOR_URL, INDEX, ASK_ANALEYEZER


def create_meta_value(value):
    """
    This function is used to to transform the value output of Dobie to meta data value

    :param value: provided Dobie value
    :return: metadata value
    """
    extracted_value = value.replace("+", "plus")
    split_value = extracted_value.split(" ")

    if len(split_value) > 1:
        processed_value = list(map(lambda word: word.title() if word != split_value[0] else word, split_value))
        value_data = "".join(processed_value)
    else:
        value_data = extracted_value

    meta_value = "".join(list(map(lambda char: "dot" if char == "." and char == value_data[0] else char, value_data)))
    return meta_value


def parse_features(annotation):
    """
    This function is used to to extract features from a provided annotation object

    :param annotation: provided annotation object
    :return: extracted features
    """
    saro_skill = {}

    features = annotation.select('Feature')
    for feature in features:

        name = feature.Name.text.capitalize()
        value = feature.Value.text.capitalize()

        if name == 'String':
            value = value.lower()

            meta_value = create_meta_value(value)
            saro_skill["meta_value"] = meta_value

        if name != "Frequencyofmention":
            saro_skill[name] = value

    features_dict = dict(filter(lambda element: element[1] != 'External', saro_skill.items()))
    return features_dict


def parse_dobie_response(xml_response):
    """
    The following function is used to get DOBIE responses and parses annotated tools

    Args:
        xml_response: DOBIE response

    Returns:
        extracted_skills: list of dict
        >>> [{'string': 'CustomerSupport', 'frequencyOfMention': '1', 'kind': 'topic'}, {'string': 'Security', 'frequencyOfMention': '1', 'kind': 'topic'}]

    Examples:
        >>> parse_dobie_response(
        '''<Annotation Id="0" Type="Split" StartNode="42" EndNode="42">
            <Feature>
              <Name className="java.lang.String">kind</Name>
              <Value className="java.lang.String">external</Value>
            </Feature>
        </Annotation>'''
        )
    """
    soup = BeautifulSoup(xml_response, "xml")
    annotations = soup.find_all('Annotation')

    extracted_skills = []

    for annotation in annotations:
        features_dict = parse_features(annotation)

        if features_dict:
            extracted_skills.append(SARO_SKILL.format(**features_dict))

    if extracted_skills:
        extracted_saro_data = SARO_PREFIXES + "".join(extracted_skills)
    else:
        extracted_saro_data = []
    return extracted_saro_data


def split_camel_case(input_string):
    """
    This function is used to transform camel case words to more words

    Args:
        input_string: camel case string

    Returns: Extracted words from camel case

    """
    if len(input_string) > 5:

        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', input_string)).split()
        joined_string = " ".join(splitted)
        return joined_string
    else:
        return input_string


def extract_raw_features(annotation):
    """
    This function is used to extract raw features from annotations

    :param annotation: annotation object
    :return: features in dictionary
    """
    features = annotation.select('Feature')
    annotation_features = {}
    for feature in features:
        feature_name = feature.Name.text
        feature_value = feature.Value.text

        annotation_features[feature_name] = feature_value
    features_dict = dict(filter(lambda element: element[1] != 'external', annotation_features.items()))
    return features_dict


def transform_to_graph(ttl):
    """This function is used to transform a ttl response to graph"""
    g = Graph()
    g.parse(data=ttl, format='turtle')

    SELECT_SPARQL_QUERY = """
        SELECT ?skill ?label ?frequency ?type 
        WHERE { 
            ?skill rdfs:label ?label .
            ?skill saro:frequencyOfMention ?frequency.
            ?skill rdf:type ?type.
        }"""
    results = g.query(SELECT_SPARQL_QUERY)
    return results


def handle_course_skill_annotation(dobie_output, course_id):
    """
       This function is used to extract dobie annotation and return list of extracted skills

       :param dobie_output: dobie response
       :param course_name: provided course_name
       :return: list of extracted skills
       """
    # postgres_client = PostgresClient()
    results = transform_to_graph(ttl=dobie_output.text)
    skill_list = []
    for row in results:
        skill_list.append(row['label'].toPython())
        print(row['label'].title())

    skill_list = remove_common_skills(skill_list)
    print(skill_list)
    return skill_list


def remove_common_skills(skill_list):
    common_list = ['tools', 'design', 'analysis', 'development', 'programming']
    filtered_skill_list = [skill for skill in skill_list if skill not in common_list]
    return filtered_skill_list


def handle_raw_annotation(dobie_output, job_name):
    """
    This function is used to extract dobie annotation and return list of extracted skills

    :param dobie_output: dobie response
    :param job_name: provided job_name
    :return: list of extracted skills
    """
    postgres_client = PostgresClient()

    soup = BeautifulSoup(dobie_output, "xml")
    annotations = soup.find_all('Annotation')

    extracted_skills = []

    for annotation in annotations:
        features_dict = extract_raw_features(annotation)

        if features_dict and 'type' not in features_dict.keys():
            features_dict['string'] = split_camel_case(features_dict['string'])

            postgres_client.upsert_new_skill(
                job_name=job_name,
                skill=features_dict['string'],
                frequencyOfMention=features_dict['frequencyOfMention'],
                kind=features_dict['kind']
            )

            extracted_skills.append(features_dict)
    postgres_client.session.close()
    return extracted_skills


def find_qualichain_skills(qualichain_skills, dobie_skill):
    """This function finds a match for skill extracted from qualichain"""
    match_skill_row = qualichain_skills[qualichain_skills['alt_label'] == dobie_skill]
    if_skill_exists = len(match_skill_row)
    if if_skill_exists:
        skill_name = match_skill_row['name'].values[0]
    else:
        skill_name = None
    return skill_name


def translate_v2dobie_output(dobie_response, job_name):
    """This function is used to translate dobie output"""
    postgres_client = PostgresClient()
    results = transform_to_graph(ttl=dobie_response)

    for row in results:
        # skill = row['skill'].replace('http://w3id.org/saro/', '')
        skill_label = row['label'].toPython()
        frequency_of_mention = int(row['frequency'].title())
        kind = row['type'].toPython().replace('http://w3id.org/saro/', '')

        postgres_client.upsert_new_skill(
            job_name=job_name,
            skill=skill_label,
            frequencyOfMention=frequency_of_mention,
            kind=kind
        )
    postgres_client.session.close()


def handle_raw_output(dobie_output):
    """
    This function is used to receive raw dobie output
    """

    soup = BeautifulSoup(dobie_output, "xml")
    annotations = soup.find_all('Annotation')

    extracted_skills = []

    for annotation in annotations:
        features_dict = extract_raw_features(annotation)

        if features_dict and 'type' not in features_dict.keys():
            extracted_skills.append(features_dict['string'])
    return extracted_skills


def save_extracted_skills(skills, filename):
    """
    This function is used to get extracted skills and save them to a csv

    :param skills: provided skills
    :param filename: given file name
    :return:
    """
    file_name = '{}.csv'.format(filename)
    skills_df = pd.DataFrame(skills)
    skills_df['frequencyOfMention'] = pd.to_numeric(skills_df['frequencyOfMention'])

    sorted_skills = skills_df.sort_values(by='frequencyOfMention', ascending=False)
    check_if_file_exists = path.isfile(file_name)

    if check_if_file_exists:
        sorted_skills.to_csv(file_name, mode='a', header=False)
    else:
        sorted_skills.to_csv(file_name)


def query_creator(job_attributes, key):
    """
    This function is used to query Analyzer for job posts

    :param job_attributes: provided job attributes
    :param key: provided key
    :return: returned job post ids
    """
    data = {
        "query": "bool_query",
        "index": INDEX,
        "min_score": job_attributes['min_score'],
        "_source": ["id"],
        "should": [
            {"multi_match": {
                "query": query,
                "fields": ["title", "requirements"],
                "type": "phrase",
                "slop": 2}
            } for query in job_attributes['queries']
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url=QUERY_EXECUTOR_URL, headers=headers, data=json.dumps(data))
    job_post_ids = [res['_source']['id'] for res in response.json()]

    return job_post_ids


def chunkify(a, n):
    """This method is used to split list to n parts"""
    k, m = divmod(len(a), n)
    return list((a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)))


def store_job_to_elk(**kwargs):
    """This function is used to store jobs to ElasticSearch"""
    payload = kwargs

    payload['index'] = INDEX
    payload['query'] = 'create_document'

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url=ASK_ANALEYEZER,
        data=json.dumps(payload),
        headers=headers
    )
    return response


def get_skills_from_payload(data):
    """This function grabs skills"""
    if 'skills' in data.keys():
        job_skills = data['skills']
    elif 'skillReq' in data.keys():
        job_skills = data['skillReq']
    else:
        job_skills = None
    return job_skills
