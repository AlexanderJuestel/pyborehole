import xml.etree.ElementTree as ET
import pandas as pd


class BoreholeML:

    def __init__(self,
                 path):
        tree = ET.parse(path)
        root = tree.getroot()

        # Defining dicts
        df_dict = {}
        df_dict_stratigraphy = {}

        # Defining Lists
        # Stratigraphy
        tops = []
        base = []
        rockcode = []
        rocknametext = []
        rockcode_sublayer = []
        rocknametext_sublayer = []
        rockname = []
        percentage = []
        rockColor = []
        rockname_sublayer = []
        rockColor_sublayer = []
        chronostratigraphy = []
        lithostratigraphy = []
        from_sublayer = []
        to_sublayer = []

        # Drilling
        dp_from = []
        dp_to = []
        drilling_method = []
        drilling_tool = []
        drillhole_diameter = []

        # Casing
        casingstringnumber = []
        casingstringtype = []
        casingfrom = []
        casingto = []
        casinginstallationelement = []
        casingdiameter = []
        casingmaterial = []
        casingwallthickness = []

        # Investigations
        investigationfrom = []
        investigationto = []
        investigationtype = []

        for level1 in root.findall("."):
            for level2 in level1:
                for level3 in level2:

                    # Getting Envelope Data
                    if 'srsName' in level3.attrib:
                        df_dict[('Bounded_by', 'Envelope', 'srsName', '')] = level3.attrib['srsName']

                    if 'srsDimension' in level3.attrib:
                        df_dict[('Bounded_by', 'Envelope', 'srsDimension', '')] = level3.attrib['srsDimension']

                    if level3.tag == '{http://www.opengis.net/gml/3.2}Envelope':
                        for child1 in level3:
                            if child1.tag == '{http://www.opengis.net/gml/3.2}lowerCorner':
                                lower_corner = child1.text.split()
                                lower_corner_mapped = list(map(float, lower_corner))
                                df_dict[('Bounded_by', 'Envelope', 'X_Lower_Corner', '')] = lower_corner_mapped[0]
                                df_dict[('Bounded_by', 'Envelope', 'Y_Lower_Corner', '')] = lower_corner_mapped[1]
                                df_dict[('Bounded_by', 'Envelope', 'Z_Lower_Corner', '')] = lower_corner_mapped[2]

                            if child1.tag == '{http://www.opengis.net/gml/3.2}upperCorner':
                                upper_corner = child1.text.split()
                                upper_corner_mapped = list(map(float, upper_corner))
                                df_dict[('Bounded_by', 'Envelope', 'X_Upper_Corner', '')] = upper_corner_mapped[0]
                                df_dict[('Bounded_by', 'Envelope', 'Y_Upper_Corner', '')] = upper_corner_mapped[1]
                                df_dict[('Bounded_by', 'Envelope', 'Z_Upper_Corner', '')] = upper_corner_mapped[2]

                    # # Getting Borehole Data
                    if '{http://www.opengis.net/gml/3.2}id' in level3.attrib:
                        df_dict[('Feature_Member', 'Borehole', 'ID', '')] = level3.attrib[
                            '{http://www.opengis.net/gml/3.2}id']

                    for level4 in level3:

                        if level4.tag == '{http://www.opengis.net/gml/3.2}identifier':
                            df_dict[('Feature_Member', 'Borehole', 'Identifier', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}location':
                            for child1 in level4:
                                if child1.tag == '{http://www.opengis.net/gml/3.2}Point':
                                    for child2 in child1:
                                        if child2.tag == '{http://www.opengis.net/gml/3.2}pos':
                                            print(child1.text)
                                            position = child2.text.split()
                                            position_mapped = list(map(float, position))
                                            df_dict[('Feature_Member', 'Borehole', 'Location', 'X_Position')] = \
                                                position_mapped[0]
                                            df_dict[('Feature_Member', 'Borehole', 'Location', 'Y_Position')] = \
                                                position_mapped[1]
                                            df_dict[('Feature_Member', 'Borehole', 'Location', 'Z_Position')] = \
                                                position_mapped[2]

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}boreholePath':

                            for child1 in level4:
                                if child1.tag == '{http://www.opengis.net/gml/3.2}Curve':

                                    for child2 in child1:
                                        if child2.tag == '{http://www.opengis.net/gml/3.2}segments':
                                            for child3 in child2:
                                                if child3.tag == '{http://www.opengis.net/gml/3.2}LineStringSegment':
                                                    for child4 in child3:
                                                        if child4.tag == '{http://www.opengis.net/gml/3.2}posList':
                                                            posList = child4.text.split()
                                                            posList_mapped = list(map(float, posList))
                                                            posList_x = posList_mapped[0::3]
                                                            posList_y = posList_mapped[1::3]
                                                            posList_z = posList_mapped[2::3]

                                                            df_dict[('Feature_Member', 'Borehole', 'Borehole_Path',
                                                                     'X_Easting')] = posList_x
                                                            df_dict[('Feature_Member', 'Borehole', 'Borehole_Path',
                                                                     'X_Northing')] = posList_y
                                                            df_dict[('Feature_Member', 'Borehole', 'Borehole_Path',
                                                                     'X_TVD')] = posList_z

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}id':
                            df_dict[('Feature_Member', 'Borehole', 'Identifier_2', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}language':
                            for child1 in level4:
                                if child1.tag == '{http://www.isotc211.org/2005/gmd}LanguageCode':
                                    df_dict[('Feature_Member', 'Borehole', 'LanguageCode', '')] = child1.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}shortName':

                            for child1 in level4:
                                df_dict[('Feature_Member', 'Borehole', 'Short_Name', '')] = child1.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}fullName':
                            for child1 in level4:
                                df_dict[('Feature_Member', 'Borehole', 'Full_Name', '')] = child1.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}databaseSource':
                            df_dict[('Feature_Member', 'Borehole', 'DataBaseSource', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}totalLength':
                            df_dict[('Feature_Member', 'Borehole', 'TotalLength', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}exportDate':
                            df_dict[('Feature_Member', 'Borehole', 'ExportDate', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}groundwaterEncountered':
                            df_dict[('Feature_Member', 'Borehole', 'GroundwaterEncountered', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}codingStandard':
                            df_dict[('Feature_Member', 'Borehole', 'CodingStandard', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}boreholeSegment':
                            for child1 in level4:
                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}BoreholeSegment':
                                    for child2 in child1:
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}from':
                                            df_dict[
                                                ('Feature_Member', 'Borehole', 'BoreholeSegment', 'From')] = child2.text

                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}to':
                                            df_dict[
                                                ('Feature_Member', 'Borehole', 'BoreholeSegment', 'To')] = child2.text

                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}azimuth':
                                            df_dict[(
                                                'Feature_Member', 'Borehole', 'BoreholeSegment',
                                                'Azimuth')] = child2.text

                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}inclination':
                                            df_dict[('Feature_Member', 'Borehole', 'BoreholeSegment',
                                                     'Inclination')] = child2.text

                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}segmentDataQuality':
                                            df_dict[('Feature_Member', 'Borehole', 'BoreholeSegment',
                                                     'DataQuality')] = child2.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}organisation':
                            for child in level4:
                                if child.tag == '{http://www.infogeo.de/boreholeml/3.0}BoreholeProvider':
                                    for child1 in child:

                                        if child1.tag == '{http://www.isotc211.org/2005/gmd}individualName':

                                            for child2 in child1:
                                                if child2.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                    df_dict[('Feature_Member', 'Borehole', 'Borehole_Provider',
                                                             'Individual_Name')] = child2.text

                                        if child1.tag == '{http://www.isotc211.org/2005/gmd}organisationName':

                                            for child2 in child1:
                                                if child2.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                    df_dict[('Feature_Member', 'Borehole', 'Borehole_Provider',
                                                             'Organisation_Name')] = child2.text

                                        if child1.tag == '{http://www.isotc211.org/2005/gmd}contactInfo':
                                            for child2 in child1:
                                                if child2.tag == '{http://www.isotc211.org/2005/gmd}CI_Contact':
                                                    for child3 in child2:
                                                        if child3.tag == '{http://www.isotc211.org/2005/gmd}phone':
                                                            for child4 in child3:
                                                                if child4.tag == '{http://www.isotc211.org/2005/gmd}CI_Telephone':
                                                                    for child5 in child4:
                                                                        if child5.tag == '{http://www.isotc211.org/2005/gmd}voice':
                                                                            for child6 in child5:
                                                                                if child6.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                                                    df_dict[(
                                                                                        'Feature_Member', 'Borehole',
                                                                                        'Borehole_Provider',
                                                                                        'Telephone')] = child6.text
                                                                        if child5.tag == '{http://www.isotc211.org/2005/gmd}facsimile':
                                                                            for child6 in child5:
                                                                                if child6.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                                                    df_dict[(
                                                                                        'Feature_Member', 'Borehole',
                                                                                        'Borehole_Provider',
                                                                                        'Fax')] = child6.text
                                                        if child3.tag == '{http://www.isotc211.org/2005/gmd}address':
                                                            for child4 in child3:
                                                                if child4.tag == '{http://www.isotc211.org/2005/gmd}CI_Address':
                                                                    for child5 in child4:
                                                                        if child5.tag == '{http://www.isotc211.org/2005/gmd}deliveryPoint':
                                                                            for child6 in child5:
                                                                                if child6.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                                                    df_dict[(
                                                                                        'Feature_Member', 'Borehole',
                                                                                        'Borehole_Provider',
                                                                                        'Delivery_Point')] = child6.text
                                                                        if child5.tag == '{http://www.isotc211.org/2005/gmd}administrativeArea':
                                                                            for child6 in child5:
                                                                                if child6.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                                                    df_dict[(
                                                                                        'Feature_Member', 'Borehole',
                                                                                        'Borehole_Provider',
                                                                                        'Administrative_Area')] = child6.text
                                                                        if child5.tag == '{http://www.isotc211.org/2005/gmd}postalCode':
                                                                            for child6 in child5:
                                                                                if child6.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                                                    df_dict[(
                                                                                        'Feature_Member', 'Borehole',
                                                                                        'Borehole_Provider',
                                                                                        'Postal_Code')] = child6.text
                                                                        if child5.tag == '{http://www.isotc211.org/2005/gmd}country':
                                                                            for child6 in child5:
                                                                                if child6.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                                                    df_dict[(
                                                                                        'Feature_Member', 'Borehole',
                                                                                        'Borehole_Provider',
                                                                                        'Country')] = child6.text
                                                                        if child5.tag == '{http://www.isotc211.org/2005/gmd}electronicMailAddress':
                                                                            for child6 in child5:
                                                                                if child6.tag == '{http://www.isotc211.org/2005/gco}CharacterString':
                                                                                    df_dict[(
                                                                                        'Feature_Member', 'Borehole',
                                                                                        'Borehole_Provider',
                                                                                        'Email Address')] = child6.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}groundwater':
                            for child1 in level4:
                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}Groundwater':
                                    for child2 in child1:
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}entryDepth':
                                            df_dict[(
                                                'Feature_Member', 'Borehole', 'Groundwater',
                                                'Entry_Depth')] = child2.text
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}entryDateTime':
                                            df_dict[('Feature_Member', 'Borehole', 'Groundwater',
                                                     'Entry_Date_time')] = child2.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}boreholeWebLink':
                            df_dict[('Feature_Member', 'Borehole', 'Borehole_WebLink', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}locationName':
                            for child1 in level4:
                                if child1.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}GeographicalName':
                                    for child2 in child1:
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}language':
                                            df_dict[
                                                ('Feature_Member', 'Borehole', 'Location', 'Language')] = child2.text
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}nativeness':
                                            df_dict[
                                                ('Feature_Member', 'Borehole', 'Location', 'Nativeness')] = child2.text
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}nameStatus':
                                            df_dict[
                                                ('Feature_Member', 'Borehole', 'Location', 'Name_Status')] = child2.text
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}sourceOfName':
                                            df_dict[(
                                                'Feature_Member', 'Borehole', 'Location',
                                                'Source_of_Name')] = child2.text
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}pronunciation':
                                            df_dict[(
                                                'Feature_Member', 'Borehole', 'Location',
                                                'Pronounciation')] = child2.text
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}spelling':
                                            for child3 in child2:
                                                if child3.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}SpellingOfName':
                                                    for child4 in child3:
                                                        if child4.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}text':
                                                            df_dict[('Feature_Member', 'Borehole', 'Location',
                                                                     'Spelling_Text')] = child4.text
                                                        if child4.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}script':
                                                            df_dict[('Feature_Member', 'Borehole', 'Location',
                                                                     'Spelling_Script')] = child4.text
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}grammaticalGender':
                                            df_dict[('Feature_Member', 'Borehole', 'Location',
                                                     'Grammatical_Gender')] = child2.text
                                        if child2.tag == '{urn:x-inspire:specification:gmlas:GeographicalNames:3.0}grammaticalNumber':
                                            df_dict[('Feature_Member', 'Borehole', 'Location',
                                                     'Grammatical_Number')] = child2.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}drillingMethod':
                            df_dict[('Feature_Member', 'Borehole', 'DrillingMethod', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}drillingDate':
                            df_dict[('Feature_Member', 'Borehole', 'DrillingDate', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}lastHorizon':
                            df_dict[('Feature_Member', 'Borehole', 'Last_Horizon', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}drillingPurpose':
                            df_dict[('Feature_Member', 'Borehole', 'DrillingPurpose', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}owner':
                            df_dict[('Feature_Member', 'Borehole', 'Owner', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}project':
                            df_dict[('Feature_Member', 'Borehole', 'Project', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}layerDataLegalAvail':
                            df_dict[('Feature_Member', 'Borehole', 'layerDataLegalAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}layerDataTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'layerDataTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}installationLegalAvail':
                            df_dict[('Feature_Member', 'Borehole', 'installationLegalAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}installationTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'installationTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}groundwaterLevelDataLegalAvail':
                            df_dict[('Feature_Member', 'Borehole', 'groundwaterLevelDataLegalAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}groundwaterLevelDataTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'groundwaterLevelDataTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}boreholeMeasurementLegalAvail':
                            df_dict[('Feature_Member', 'Borehole', 'boreholeMeasurementLegalAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}boreholeMeasurementTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'boreholeMeasurementTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}archiveDataLegalAvail':
                            df_dict[('Feature_Member', 'Borehole', 'archiveDataLegalAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}archiveDataTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'archiveDataTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}scansLegalAvail':
                            df_dict[('Feature_Member', 'Borehole', 'scansLegalAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}scansTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'scansTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}samplesTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'samplesTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}labDataLegalAvail':
                            df_dict[('Feature_Member', 'Borehole', 'labDataLegalAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}labDataTechAvail':
                            df_dict[('Feature_Member', 'Borehole', 'labDataTechAvail', '')] = level4.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}origin':
                            for child1 in level4:
                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}Origin':
                                    for child2 in child1:
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}originalLocation':
                                            if 'srsName' in child2.attrib:
                                                df_dict[('Feature_Member', 'Borehole', 'Origin', 'srsName')] = \
                                                    child2.attrib['srsName']
                                            if 'srsDimension' in child2.attrib:
                                                df_dict[('Feature_Member', 'Borehole', 'Origin', 'srsDimension')] = \
                                                    child2.attrib['srsDimension']

                                            df_dict[(
                                                'Feature_Member', 'Borehole', 'Origin',
                                                'Original_Location')] = child2.text
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}locationMethod':
                                            df_dict[(
                                                'Feature_Member', 'Borehole', 'Origin',
                                                'Location_Method')] = child2.text
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}elevation':
                                            df_dict[('Feature_Member', 'Borehole', 'Origin', 'Elevation')] = child2.text
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}levelMethod':
                                            df_dict[
                                                ('Feature_Member', 'Borehole', 'Origin', 'Level_Method')] = child2.text

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}intervalSeries':
                            for child1 in level4:
                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}IntervalSeries':
                                    for layer in child1:
                                        if layer.tag == '{http://www.infogeo.de/boreholeml/3.0}layer':
                                            for interval in layer:
                                                if interval.tag == '{http://www.infogeo.de/boreholeml/3.0}Interval':
                                                    for item in interval:
                                                        if item.tag == '{http://www.infogeo.de/boreholeml/3.0}from':
                                                            tops.append(float(item.text))
                                                        if item.tag == '{http://www.infogeo.de/boreholeml/3.0}to':
                                                            base.append(float(item.text))
                                                        if item.tag == '{http://www.infogeo.de/boreholeml/3.0}rockCode':
                                                            rockcode.append(item.text)
                                                        if item.tag == '{http://www.infogeo.de/boreholeml/3.0}rockNameText':
                                                            for subitem in item:
                                                                if subitem.tag == '{http://www.isotc211.org/2005/gmd}LocalisedCharacterString':
                                                                    rocknametext.append(subitem.text)

                                                        if item.tag == '{http://www.infogeo.de/boreholeml/3.0}lithology':
                                                            for subitem in item:
                                                                if subitem.tag == '{http://www.infogeo.de/boreholeml/3.0}Lithology':
                                                                    for subsubitem in subitem:
                                                                        if subsubitem.tag == '{http://www.infogeo.de/boreholeml/3.0}rockName':
                                                                            rockname.append(subsubitem.text)
                                                                        if subsubitem.tag == '{http://www.infogeo.de/boreholeml/3.0}percentage':
                                                                            percentage.append(subsubitem.text)
                                                                        if subsubitem.tag == '{http://www.infogeo.de/boreholeml/3.0}rockColor':
                                                                            rockColor.append(subsubitem.text)

                                                        if item.tag == '{http://www.infogeo.de/boreholeml/3.0}stratigraphy':
                                                            for subitem in item:
                                                                if subitem.tag == '{http://www.infogeo.de/boreholeml/3.0}Stratigraphy':
                                                                    for subsubitem in subitem:
                                                                        if subsubitem.tag == '{http://www.infogeo.de/boreholeml/3.0}chronoStratigraphy':
                                                                            chronostratigraphy.append(subsubitem.text)
                                                                        if subsubitem.tag == '{http://www.infogeo.de/boreholeml/3.0}lithoStratigraphy':
                                                                            for child in subsubitem:
                                                                                if child.tag == '{http://www.isotc211.org/2005/gmd}LocalisedCharacterString':
                                                                                    lithostratigraphy.append(child.text)
                                                        if item.tag == '{http://www.infogeo.de/boreholeml/3.0}sublayer':
                                                            for child1 in item:
                                                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}Component':
                                                                    for child2 in child1:
                                                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}rockCode':
                                                                            rockcode_sublayer.append(child2.text)
                                                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}rockNameText':
                                                                            for child3 in child2:
                                                                                if child3.tag == '{http://www.isotc211.org/2005/gmd}LocalisedCharacterString':
                                                                                    rocknametext_sublayer.append(
                                                                                        child3.text)

                                                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}lithology':
                                                                            for child3 in child2:
                                                                                if child3.tag == '{http://www.infogeo.de/boreholeml/3.0}Lithology':
                                                                                    for subitem in child3:
                                                                                        if subitem.tag == '{http://www.infogeo.de/boreholeml/3.0}rockName':
                                                                                            rockname_sublayer.append(
                                                                                                subitem.text)
                                                                                        if subitem.tag == '{http://www.infogeo.de/boreholeml/3.0}rockColor':
                                                                                            rockColor_sublayer.append(
                                                                                                subitem.text)
                                                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}from':
                                                                            from_sublayer.append(child2.text)
                                                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}to':
                                                                            to_sublayer.append(child2.text)

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}drillingProcess':
                            for child1 in level4:
                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}DrillingProcess':
                                    for child2 in child1:
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}from':
                                            dp_from.append(child2.text)
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}to':
                                            dp_to.append(child2.text)
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}drillingMethod':
                                            drilling_method.append(child2.text)
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}drillingTool':
                                            drilling_tool.append(child2.text)
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}drillholeDiameter':
                                            drillhole_diameter.append(child2.text)

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}installationDetail':
                            for child1 in level4:
                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}InstallationDetails':
                                    for child2 in child1:
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}casingString':
                                            for child3 in child2:
                                                if child3.tag == '{http://www.infogeo.de/boreholeml/3.0}CasingString':
                                                    for child4 in child3:
                                                        if child4.tag == '{http://www.infogeo.de/boreholeml/3.0}casingStringNumber':
                                                            casingstringnumber.append(child4.text)
                                                        if child4.tag == '{http://www.infogeo.de/boreholeml/3.0}casingStringType':
                                                            casingstringtype.append(child4.text)
                                                        if child4.tag == '{http://www.infogeo.de/boreholeml/3.0}casingStringSegment':
                                                            for child5 in child4:
                                                                if child5.tag == '{http://www.infogeo.de/boreholeml/3.0}CasingStringSegment':
                                                                    for child6 in child5:
                                                                        if child6.tag == '{http://www.infogeo.de/boreholeml/3.0}from':
                                                                            casingfrom.append(child6.text)
                                                                        if child6.tag == '{http://www.infogeo.de/boreholeml/3.0}to':
                                                                            casingto.append(child6.text)
                                                                        if child6.tag == '{http://www.infogeo.de/boreholeml/3.0}installationElement':
                                                                            casinginstallationelement.append(
                                                                                child6.text)
                                                                        if child6.tag == '{http://www.infogeo.de/boreholeml/3.0}diameter':
                                                                            casingdiameter.append(child6.text)
                                                                        if child6.tag == '{http://www.infogeo.de/boreholeml/3.0}casingMaterial':
                                                                            casingmaterial.append(child6.text)
                                                                        if child6.tag == '{http://www.infogeo.de/boreholeml/3.0}wallThickness':
                                                                            casingwallthickness.append(child6.text)

                        if level4.tag == '{http://www.infogeo.de/boreholeml/3.0}investigation':
                            for child1 in level4:
                                if child1.tag == '{http://www.infogeo.de/boreholeml/3.0}Investigation':
                                    for child2 in child1:
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}from':
                                            investigationfrom.append(child2.text)
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}to':
                                            investigationto.append(child2.text)
                                        if child2.tag == '{http://www.infogeo.de/boreholeml/3.0}investigationType':
                                            investigationtype.append(child2.text)

        self.meta_data = pd.DataFrame(list(df_dict.values()),
                                      index=pd.MultiIndex.from_tuples(df_dict.keys()))

        self.stratigraphic_table = pd.DataFrame(list(zip(tops,
                                                         base,
                                                         rockcode,
                                                         rocknametext,
                                                         rockname,
                                                         percentage,
                                                         rockColor,
                                                         chronostratigraphy,
                                                         lithostratigraphy,
                                                         rockcode_sublayer,
                                                         rocknametext_sublayer,
                                                         rockname_sublayer,
                                                         rockColor_sublayer,
                                                         from_sublayer,
                                                         to_sublayer
                                                         )),
                                                columns=['Top',
                                                         'Base',
                                                         'Rock_Code',
                                                         'Rock_Name_Text',
                                                         'Rock_Name',
                                                         'Percentage',
                                                         'Rock_Color',
                                                         'Chronostratigraphy',
                                                         'Lithostratigraphy',
                                                         'Rock_Code_Sublayer',
                                                         'Rock_Name_Text_Sublayer',
                                                         'Rock_Name_Sublayer',
                                                         'Rock_Color_Sublayer',
                                                         'Top_Sublayer',
                                                         'Base_Sublayer'
                                                         ])

        self.drilling_process = pd.DataFrame(list(zip(dp_from,
                                                      dp_to,
                                                      drilling_method,
                                                      drilling_tool,
                                                      drillhole_diameter
                                                      )),
                                             columns=['From',
                                                      'To',
                                                      'Drilling_Method',
                                                      'Drilling_Tool',
                                                      'Drillhole_Diameter'
                                                      ]).sort_values('From', ascending=True)

        self.installation_details = pd.DataFrame(list(zip(casingstringnumber,
                                                          casingstringtype,
                                                          casingfrom,
                                                          casingto,
                                                          casinginstallationelement,
                                                          casingdiameter,
                                                          casingmaterial,
                                                          casingwallthickness,
                                                          )),
                                                 columns=['Casing_String_Number',
                                                          'Casing_String_Type',
                                                          'From',
                                                          'To',
                                                          'Casing_Installation_Element',
                                                          'Casing_Diameter',
                                                          'Casing_Material',
                                                          'Casing_Wall_Thickness'

                                                          ]).sort_values('From', ascending=True)

        self.investigations = pd.DataFrame(list(zip(investigationfrom,
                                                    investigationto,
                                                    investigationtype
                                                    )),
                                           columns=['From',
                                                    'To',
                                                    'Investigation_Type'
                                                    ]).sort_values('From', ascending=True)
