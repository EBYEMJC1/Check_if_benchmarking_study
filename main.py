import argparse
import os
import shutil
from grabbing_links import get_pmc_ids
from retrieve_ftp_links import retrieve_ftplink
from getting_pdfs import get_pdf
from extracting_text import *
from palm_eval import process_extracted_text

def main(url, tool_name):
    # Call the get_filtered_links function
    pmc_ids = get_pmc_ids(url)

    ftp_links = list()
    # Iterate over the filtered links and do further processing
    for pmc_id in pmc_ids:
        ftp_links_and_pmc_id = retrieve_ftplink(pmc_id, '3009543ad6329aa8ae725b7a11354398b608')
        # Process each link as needed
        if ftp_links_and_pmc_id is not None:
            ftp_links.append(ftp_links_and_pmc_id)

    pdf_list = list()
    for ftp_link, pmc_id in ftp_links:
        pdf_list.append(get_pdf(ftp_link, pmc_id))

    extracted_text = []
    # Extract text from PDF files
    for pmc_id, paths in pdf_list:
        extracted_text.extend(extract_text_from_pdf_paths(pmc_id, paths))

    for pmc_id, text in extracted_text:
        process_extracted_text(pmc_id, text, tool_name)
'''
    # Remove the 'pdfs' directory
    shutil.rmtree('pdfs')'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the script to process PMC articles.')
    parser.add_argument('url', type=str, help='URL to extract links from')
    parser.add_argument('tool_name', type=str, help='Tool name')
    args = parser.parse_args()

    main(args.url, args.tool_name)
