import xml.etree.ElementTree as ET
import pandas as pd


def parse_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    namespaces = {
        'gmx': 'http://www.isotc211.org/2005/gmx',
        'bmlcl': 'http://www.infogeo.de/boreholeml/3.0/codelists',
        'gml': 'http://www.opengis.net/gml/3.2'
    }

    code_entries = root.findall('.//gmx:codeEntry', namespaces=namespaces)

    data = []

    for code_entry in code_entries:
        description = code_entry.find('.//gml:description', namespaces=namespaces).text
        identifier = code_entry.find('.//gml:identifier', namespaces=namespaces).text
        try:
            name = code_entry.find('.//gml:name', namespaces=namespaces).text
        except AttributeError:
            name = None
        try:
            key_id = int(code_entry.find('.//bmlcl:keyID', namespaces=namespaces).text)
        except AttributeError:
            key_id = None

        alternative_expression = code_entry.find('.//gmx:alternativeExpression', namespaces=namespaces)
        if alternative_expression is not None:
            alternative_identifier = alternative_expression.find('.//gml:identifier', namespaces=namespaces).text
            alternative_name = alternative_expression.find('.//gml:name', namespaces=namespaces).text
        else:
            alternative_identifier = None
            alternative_name = None

        data.append((description, identifier, name, key_id, alternative_identifier, alternative_name))

    columns = [
        'Description',
        'Identifier',
        'Name',
        'KeyID',
        'Alternative Identifier',
        'Alternative Name'
    ]

    df = pd.DataFrame(data, columns=columns).sort_values('KeyID', ascending=True).reset_index(drop=True)

    return df
