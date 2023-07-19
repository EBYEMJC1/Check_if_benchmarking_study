from ftplib import FTP
import tarfile
import os
import zlib
import shutil

MAX_RETRIES = 3

def get_pdf(url, pmc_id):
    ftp_url = 'ftp.ncbi.nlm.nih.gov'
    ftp_directory = '/pub/pmc'
    subdirectories = url.split("/")[5:-1]  # Extract the relevant subdirectories from the URL
    ftp_directory += "/" + "/".join(subdirectories)  # Append the subdirectories to the FTP directory
    filename = url.split("/")[-1]

    # Connect to the FTP server
    ftp = FTP(ftp_url)
    ftp.login()

    # Change to the desired directory
    ftp.cwd(ftp_directory)

    # Check if the file exists in the FTP directory
    file_exists = filename in ftp.nlst()

    success = False  # Flag variable to track extraction success
    result = None  # Variable to store the result

    if file_exists:
        # Download the file
        with open(filename, 'wb') as file:
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    ftp.retrbinary('RETR ' + filename, file.write)
                    break
                except EOFError:
                    retries += 1
                    if retries == MAX_RETRIES:
                        print(f"Error: Maximum retries exceeded. Skipping download.")
                        return pmc_id, None
                    else:
                        print(f"Retrying download... Attempt {retries}/{MAX_RETRIES}")

        try:
            pdf_name_list = list()
            # Extract the content from the tar.gz file
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    with tarfile.open(filename, 'r:gz') as tar:
                        pdf_members = [member for member in tar.getmembers() if member.name.endswith('.pdf')]
                        for member in pdf_members:
                            member.name = os.path.basename(member.name)  # Remove any directory structure
                            tar.extract(member, path='pdfs')  # Extract to the 'pdfs' directory
                            pdf_name = os.path.basename(member.name)
                            pdf_name_list.append(f"./pdfs/{pdf_name}")
                            success = True  # Extraction successful
                        result = (pmc_id, pdf_name_list)  # Store the result
                    break
                except (tarfile.ReadError, zlib.error) as e:
                    retries += 1
                    if retries == MAX_RETRIES:
                        success = False
                        print(f"Error extracting content from '{filename}': {str(e)}. Skipping extraction.")
                        break
                    else:
                        print(f"Retrying extraction... Attempt {retries}/{MAX_RETRIES}")

        finally:
            try:
                # Delete the tar.gz file
                os.remove(filename)
            except OSError:
                print(f"Error deleting file '{filename}'. Skipping deletion.")

    else:
        print(f"File '{filename}' does not exist in the FTP directory.")

    # Close the FTP connection
    ftp.quit()

    if success:
        return result  # Return the result if extraction was successful
    else:
        return pmc_id, None  # Return None if there was an error

# Create the 'pdfs' directory if it doesn't exist
if not os.path.exists('pdfs'):
    os.makedirs('pdfs')
