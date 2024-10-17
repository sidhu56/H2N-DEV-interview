import os
import xmltodict
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='process.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def convert_xml_to_json(xml_content):
    try:
        data_dict = xmltodict.parse(xml_content)
        json_data = json.dumps(data_dict, indent=4)
        return json_data
    except Exception as e:
        logging.error(f"Parsing error: {e}")
        return None

def process_xml_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    xml_content = file.read()
                    
                # Convert XML to JSON
                json_result = convert_xml_to_json(xml_content)
                if json_result:
                    # Save JSON result
                    json_filename = filename.replace('.xml', '.json')
                    with open(json_filename, 'w', encoding='utf-8') as json_file:
                        json_file.write(json_result)
                    logging.info(f"Processed {filename} successfully.")
                else:
                    logging.warning(f"Skipped {filename} due to parsing errors.")
                    
            except FileNotFoundError:
                logging.error(f"File not found: {filename}")
            except xmltodict.expat.ExpatError:
                logging.error(f"Malformed XML in {filename}.")
            except KeyError as e:
                logging.warning(f"Skipped {filename} - Missing <{e}> element.")
            except Exception as e:
                logging.error(f"Unexpected error in {filename}: {e}")

if __name__ == "__main__":
    process_xml_files('./xml-files/')
