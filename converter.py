import xml.etree.ElementTree as ET
from xml.dom import minidom

# Helper function to get a part of the line and check if it exists
def get_part(parts, index):
    return parts[index] if len(parts) > index else None

def convert_to_xml(data):
    root = ET.Element("people")
    person = None
    family = None
    
    for line in data:
        parts = line.strip().split('|')
        record_type = parts[0]

        if record_type == "P":
            person = ET.SubElement(root, "person")
            ET.SubElement(person, "firstname").text = get_part(parts, 1)
            ET.SubElement(person, "lastname").text =  get_part(parts, 2)
            family = None
        
        elif record_type == "T" and person is not None:
            phone = ET.SubElement(person if family is None else family, "phone")
            ET.SubElement(phone, "mobile").text = get_part(parts, 1)
            ET.SubElement(phone, "landline").text = get_part(parts, 2)
        
        elif record_type == "A" and person is not None:
            address = ET.SubElement(person if family is None else family, "address")
            ET.SubElement(address, "street").text = get_part(parts, 1)
            ET.SubElement(address, "city").text = get_part(parts, 2)
            ET.SubElement(address, "zipcode").text = get_part(parts, 3)
        
        elif record_type == "F" and person is not None:
            family = ET.SubElement(person, "family")
            ET.SubElement(family, "name").text = get_part(parts, 1)
            ET.SubElement(family, "born").text = get_part(parts, 2)
        
        else:
            continue
    
    # minidom is only used to prettify the XML
    return minidom.parseString(ET.tostring(root, encoding="unicode", method="xml")).toprettyxml()

def main():
    with open("info.txt", "r") as file:
        data = file.readlines()
        
    result = convert_to_xml(data)
    
    with open("output.xml", "w", encoding='utf-8') as xml_file:
        xml_file.write(result)

if __name__ == "__main__":
    main()
