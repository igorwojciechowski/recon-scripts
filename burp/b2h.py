#!/usr/bin/env python3
#
# B2H - Burp To Http
# Python script used to convert BurpSuite *.xml traffic to *.http files
#
import sys
import os
import base64
import uuid
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print("b2h.py <input xml> [<output directory>]")
    sys.exit(1)
output_directory = None
input_file = sys.argv[1]
if len(sys.argv) > 2:
    output_directory = sys.argv[2]
    os.makedirs(os.path.abspath(output_directory))

tree = ET.parse(os.path.abspath(input_file))
root = tree.getroot()
for item in root:
    filename = os.path.abspath(f"{output_directory}/{item.find('host').text}-{uuid.uuid4().hex}")
    request_filename = f"{filename}-request.http"
    response_filename = f"{filename}-response.http"
    request = base64.decodebytes(str.encode(item.find('request').text)).decode()
    response = base64.decodebytes(str.encode(item.find('response').text)).decode()
    with open(request_filename, 'w') as f:
        f.write(request)

    with open(response_filename, 'w') as f:
        f.write(response)
