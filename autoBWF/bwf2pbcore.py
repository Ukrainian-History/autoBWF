import argparse
import re
import xml.etree.ElementTree as ET
from autoBWF.BWFfileIO import *


def main():
    # def qualified_element(ns, element):
    #     return "{{{0}}}{1}".format(namespaces[ns], element)
    #
    # namespaces = {"xml": "http://www.w3.org/XML/1998/namespace",
    #               "pbcore": "http://www.pbcore.org/PBCore/PBCoreNamespace.html"}
    #
    # for ns in namespaces.keys():
    #     ET.register_namespace(ns, namespaces[ns])

    def add_child(parent, element_name, element_value, attributes=None):
        if element_value != "":
            element = ET.SubElement(parent, element_name)
            element.text = element_value
            if attributes is not None:
                for attribute in attributes.keys():
                    element.set(attribute, attributes[attribute])
            return element

    def add_multivalue_child(parent, element_name, element_value, attributes=None):
        wikidata_regex = re.compile(r'(.+)\s+\{(Q\d+)\}')

        if element_value != "":
            items = element_value.split(';')
            for item in items:
                m = wikidata_regex.match(item)
                if m:
                    matches = m.groups()
                    name = matches[0]
                    q_code = matches[1]
                    child = add_child(parent, element_name, name,
                                      {"source": "wikidata",
                                       "ref": "https://www.wikidata.org/wiki/{}".format(q_code)})
                else:
                    child = add_child(parent, element_name, item.strip())

                if attributes is not None:
                    for attribute in attributes.keys():
                        child.set(attribute, attributes[attribute])

    def add_complex_child(parent, element_name, subelement_name, role_name, subelement_value, role_value):
        wikidata_regex = re.compile(r'(.+)\s+\{(Q\d+)\}')

        if subelement_value != "":
            items = subelement_value.split(';')
            for item in items:
                element = ET.SubElement(parent, element_name)
                m = wikidata_regex.match(item)
                if m:
                    matches = m.groups()
                    name = matches[0]
                    q_code = matches[1]
                    add_child(element, subelement_name, name,
                              {"source": "wikidata",
                               "ref": "https://www.wikidata.org/wiki/{}".format(q_code)})
                else:
                    add_child(element, subelement_name, item.strip())

                add_child(element, role_name, role_value)

    parser = argparse.ArgumentParser(
        description='Extract metadata from BWF and create PBCore XML, possibly incorporating into existing OHMS XML')
    parser.add_argument('infile', help="WAV file")
    args = parser.parse_args()

    infile = args.infile
    ohmsfile = args.infile.rsplit('.', 1)[0] + '_ohms.xml'

    metadata = get_bwf_core(True, infile)
    metadata.update(get_bwf_tech(True, infile))
    metadata.update(get_xmp(infile, ["bwfmetaedit", "--specialchars", "--accept-nopadding"]))

    # root = ET.Element(qualified_element("pbcore", "pbcoreDescriptionDocument"))
    root = ET.Element("pbcoreDescriptionDocument")
    root.append(ET.Comment('Automatically generated by bwf2pbcore from {}. Do not edit by hand.'.format(infile)))

    add_child(root, "pbcoreAssetType", metadata["form"])
    add_child(root, "pbcoreAssetDate", metadata["ICRD"])
    add_child(root, "pbcoreTitle", metadata["INAM"])

    add_multivalue_child(root, "pbcoreSubject", metadata["topics"], {"subjectType": "topic"})
    add_multivalue_child(root, "pbcoreSubject", metadata["names"], {"subjectType": "name"})
    add_multivalue_child(root, "pbcoreSubject", metadata["events"], {"subjectType": "period"})
    add_multivalue_child(root, "pbcoreSubject", metadata["places"], {"subjectType": "geographic"})

    add_child(root, "pbcoreDescription", metadata["xmp_description"])

    add_complex_child(root, "pbcoreContributor", "contributor",
                      "contributorRole", metadata["interviewer"], "interviewer")
    add_complex_child(root, "pbcoreContributor", "contributor",
                      "contributorRole", metadata["interviewee"], "interviewee")
    add_complex_child(root, "pbcoreContributor", "contributor",
                      "contributorRole", metadata["host"], "host")
    add_complex_child(root, "pbcoreContributor", "contributor",
                      "contributorRole", metadata["speaker"], "speaker")
    add_complex_child(root, "pbcoreContributor", "contributor",
                      "contributorRole", metadata["performer"], "performer")

    publisher = ET.SubElement(root, "pbcorePublisher")
    add_child(publisher, "publisher", metadata["owner"])
    add_child(publisher, "publisherRole", "copyright holder")


    ET.ElementTree(root).write("boof.xml", xml_declaration=True)


if __name__ == '__main__':
    main()
