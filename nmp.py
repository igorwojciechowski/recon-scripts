import sys
import xml.etree.ElementTree as et

if len(sys.argv) < 2:
    print('Nmap report path required!')
    sys.exit(1)

root = et.parse(sys.argv[1]).getroot()
hosts = root.findall('host')
for host in hosts:
    for port in host.find('ports').findall('port'):
        print("{url}\t{port}\t{protocol}\t{state}".format(
            url=host.find('hostnames').find('hostname').attrib['name'],
            port=port.attrib['portid'],
            protocol=port.attrib['protocol'],
            state=port.find('state').attrib['state']
        ))
