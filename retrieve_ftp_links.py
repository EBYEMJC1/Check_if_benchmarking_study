import requests
import xml.etree.ElementTree as ET

def retrieve_ftplink(pmc_id, api_key):
    api_url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmc_id}&api_key={api_key}"
    response = requests.get(api_url)
    xml_data = response.text

    root = ET.fromstring(xml_data)
    
    if root.tag == 'OA' and 'error' in root.attrib:
        error_message = root.find('error').text
        print(f"Error: {error_message}, {pmc_id}")
        return None

    records = root.findall('.//record')
    ftp_link_list=list()

    if len(records) > 0:
        for record in records:
            link_element = record.find('.//link[@format="tgz"]')
            if link_element is not None:
                href = link_element.get('href')
                return href, pmc_id

    return None

