import xml.etree.ElementTree as ET
import pandas as pd


def parse_languagecode(path):
    # Parse the XML file
    tree = ET.parse('../data/BoreholeML/LanguageCode.xml')
    root = tree.getroot()

    # Define namespaces
    namespaces = {
        'gmx': 'http://www.isotc211.org/2005/gmx',
        'gml': 'http://www.opengis.net/gml/3.2'
    }

    # Initialize lists for description and identifier
    description = []
    identifier = []

    # Extract description and identifier using XPath
    for code_entry in root.findall('.//gmx:codeEntry', namespaces):
        code_definition = code_entry.find('./gmx:CodeDefinition', namespaces)
        if code_definition is not None:
            description_element = code_definition.find('./gml:description', namespaces)
            identifier_element = code_definition.find('./gml:identifier', namespaces)
            if description_element is not None:
                description.append(description_element.text)
            if identifier_element is not None:
                identifier.append(identifier_element.text)

    df = pd.DataFrame(list(zip(
        description,
        identifier,
    )),
        columns=[
            'Description',
            'Identifier'
        ])

    return df


def parse_databasesourcelist(path):

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
        name = code_entry.find('.//gml:name', namespaces=namespaces).text
        key_id = int(code_entry.find('.//bmlcl:keyID', namespaces=namespaces).text)

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
