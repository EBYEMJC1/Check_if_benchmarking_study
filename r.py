'''from ftplib import FTP
import tarfile
import os
import zlib

def get_tar_gz_content(url):
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

    if file_exists:
        # Download the file
        with open(filename, 'wb') as file:
            ftp.retrbinary('RETR ' + filename, file.write)
        print(f"File '{filename}' downloaded successfully.")

        try:
            # Extract the content from the tar.gz file
            with tarfile.open(filename, 'r:gz') as tar:
                for member in tar.getmembers():
                    tar.extract(member)
            print(f"Content extracted from '{filename}'.")
        except (tarfile.ReadError, zlib.error) as e:
            print(f"Error extracting content from '{filename}': {str(e)}. Skipping extraction.")

        try:
            # Delete the tar.gz file
            os.remove(filename)
            print(f"File '{filename}' deleted.")
        except OSError:
            print(f"Error deleting file '{filename}'. Skipping deletion.")
    else:
        print(f"File '{filename}' does not exist in the FTP directory.")

    # Close the FTP connection
    ftp.quit()

urls = [
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/9e/6f/PMC8390189.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/14/7a/PMC4674845.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/54/ec/PMC9882225.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/3f/ac/PMC3664805.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/f7/8e/PMC10162771.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/93/0d/PMC3936741.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/0d/72/PMC5003782.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/a0/e9/PMC4499118.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/fa/a6/PMC4005686.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/06/cc/PMC4678815.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/41/42/PMC6118309.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/27/c6/PMC3278765.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/99/01/PMC3575843.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/7f/6f/PMC3664468.tar.gz'
]

for url in urls:
    get_tar_gz_content(url)
'''