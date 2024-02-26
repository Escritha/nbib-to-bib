import os
from time import time
import urllib.request as req
from urllib.error import HTTPError
from datetime import datetime

class NbibToBibConverter:
    def __init__(self, directory):
        self.directory = directory
        self.bibs_folder = os.path.join(self.directory, 'bibs')
    
    def get_latest_file(self):
        files = [f for f in os.listdir(self.bibs_folder) if f.endswith(".bib")]
        if not files:
            return None
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(self.bibs_folder, x)))
        return os.path.join(self.bibs_folder, latest_file)

    def create_bibs_folder(self):
        '''Creates a new directory within the current directory called bibs'''
        if not os.path.exists(self.bibs_folder):
            os.makedirs(self.bibs_folder)

    def read_doi(self, content):
        for line in content.decode().splitlines():
            string = "doi"
            if string in line:
                doi = line[6:line.rfind(" ")]
                print(f"DOI: {doi}")
                return doi
        return ""

    def bib_from_doi(self, doi):
        BASE_URL = 'http://dx.doi.org/'

        url = BASE_URL + doi
        r = req.Request(url, headers={"Accept": "application/x-bibtex"})
        with req.urlopen(r) as reqopen:
            return reqopen.read().decode()

    def convert_file(self, content):
        process_start = time()

        self.create_bibs_folder()

        try:
            print("Starting conversion...")

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_file_path = os.path.join(self.bibs_folder, f'ref_{timestamp}.bib')

            with open(new_file_path, 'w') as output:
                doi = self.read_doi(content)

                if doi == "":
                    print("Can't find DOI in the provided content.")
                    return ""

                try:
                    bib = self.bib_from_doi(doi)
                except HTTPError as e:
                    if e.code == 404:
                        print('DOI not found')
                    else:
                        print(f'Service unavailable: {e}')

                output.write(f'{bib}\n\n')

            process_end = time()
            elapsed = process_end - process_start
            print(f"Processing time: {elapsed}")
            print("Conversion finished.")

            return new_file_path  # Retorna o caminho do novo arquivo
        except Exception as e:
            print(e)
            return ""
