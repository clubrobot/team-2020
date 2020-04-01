#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from zipfile import ZipFile
from xml.etree import ElementTree
from io import BytesIO

# Match ggb elements
def match_name(name): return 'roadmap_' in name

# Parse the initial ggb file
ggb = ZipFile('roadmap.ggb', mode='r')
xml = ggb.open('geogebra.xml')
tree = ElementTree.parse(xml)
xml.close()
ggb.close()

# Find the construction element in which to remove sub elements
construction = tree.getroot().find('./construction')

# Remove the roadmap elements
for element in construction.findall('./element[@label]'):
	if match_name(element.get('label')):
		construction.remove(element)
for command in construction.findall('./command/output[@a0]/..'):
	if match_name(command.find('output').get('a0')):
		construction.remove(command)

# Save the new ggb file
stream = BytesIO()
tree.write(stream, encoding='utf-8', xml_declaration=True)
ggb = ZipFile('roadmap.ggb', mode='a')
ggb.writestr('geogebra.xml', stream.getvalue().decode('utf8'))
ggb.close()
