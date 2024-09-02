import xml.etree.ElementTree as ET
from time import sleep

def combine_xml_files():
    while True:
        try:
            # Read the contents of FBLive.xml
            with open('FBLive.xml', 'r') as file1:
                xml1 = file1.read()

            # Read the contents of dashboard_data.xml
            with open('dashboard_data.xml', 'r') as file2:
                xml2 = file2.read()

            # Parse both XML files
            root1 = ET.fromstring(xml1)
            root2 = ET.fromstring(xml2)

            # Create a new root element for scorebug.xml
            combined_root = ET.Element('info')

            # Add elements from FBLive.xml to the combined root
            elements_to_add = [
                'clock', 'clockmin', 'clocksec', 'playclock', 'Hscore', 'Vscore', 'down', 'downtext', 'togo', 'ballon', 'downdist', 'quarter', 'qtrtext'
            ]
            for element_name in elements_to_add:
                element = root1.find(f'.//{element_name}')
                if element is not None:
                    combined_root.append(element)

            # Overwrite with elements from dashboard_data.xml
            elements_to_overwrite = [
                'flag', 'redzone', 'first', 'possession', 'title', 'touchdown', 'Htimeouts', 'Vtimeouts'
            ]
            for element_name in elements_to_overwrite:
                element = root2.find(f'.//{element_name}')
                if element is not None:
                    combined_root.append(element)

            # Create an ElementTree with the combined root
            combined_tree = ET.ElementTree(combined_root)

            # Write the combined data to scorebug.xml
            combined_tree.write('scorebug.xml')

            # Wait for one second before updating again
            sleep(0.1)

        except Exception as e:
            print(f"Error: {e}")
            # Wait for one second before trying again
            sleep(0.1)

if __name__ == "__main__":
    combine_xml_files()
