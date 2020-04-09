from bs4 import BeautifulSoup

from settings import SARO_SKILL, SARO_PREFIXES


def my_add(x, y):
    """
    This functions adds x and y args

    Args:
        x: x parameter
        y: y parameter

    Returns:
        x+y

    Examples:
        >>> my_add(1,2)
    """
    return x + y


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
