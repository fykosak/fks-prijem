import os
import glob
import json
import pandas as pd
from collections import OrderedDict
from PyPDF2 import PdfFileMerger, PdfFileReader

def get_pages(file_name):
    with open(file_name, 'rb') as file:
        pdf = PdfFileReader(file) 
        pg = pdf.getNumPages()
    return pg

def pdf_ok_writing(pdf, temp_path="./temp"):
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    try:
        merger = PdfFileMerger()
        merger.append(pdf)
        merger.write(temp_path + "/test_can_be_deleted.pdf")
        merger.close()
        return True
    except:
        return False

def is_foreign(file_name, foreign_submitids):
    file_submitid = file_name[file_name.find("__")+2:-4]
    try:
        return int(file_submitid) in foreign_submitids
    except:
        return False

def join_it(download_path, split_exceptions, problems):
    exceptions = []
    white = 'white.pdf'

    if split_exceptions == "d" or split_exceptions == False:
        split_exceptions = False
    else:
        split_exceptions = True

    # Read the foreign submitids
    submitids_df = pd.read_csv(os.path.join(download_path, 'submitids.csv'), sep=';')
    foreign_submitids = submitids_df["submit"].values

    for problem in problems:
        print(f'uloha: {problem}')

        merger_czech = PdfFileMerger()
        merger_foreign = PdfFileMerger()
        path_list = glob.glob(download_path + f'/uloha-{problem}/*')
        pdf_list = [path for path in path_list if 'pdf' in path[-4:].lower()]
        pdf_list = sorted(pdf_list)
        dictnarozdeleni_czech = OrderedDict()
        dictnarozdeleni_foreign = OrderedDict()

        for pdf in pdf_list:
            if pdf_ok_writing(pdf):
                pages = get_pages(pdf)
                if is_foreign(pdf, foreign_submitids):
                    merger_foreign.append(pdf)
                    if pages % 2 != 0:
                        merger_foreign.append(white)
                        pages += 1
                    dictnarozdeleni_foreign.update({pdf: pages})
                else:
                    merger_czech.append(pdf)
                    if pages % 2 != 0:
                        merger_czech.append(white)
                        pages += 1
                    dictnarozdeleni_czech.update({pdf: pages})
            else:
                try: 
                    p = get_pages(pdf)
                    print("chyba writing: ", pdf)
                except:
                    print("chyba get_pages: ", pdf)
                exceptions.append(pdf)

        joined_path_czech = download_path + f'/joined_uloha-{problem}_czech.pdf'
        joined_path_foreign = download_path + f'/joined_uloha-{problem}_foreign.pdf'
        
        merger_czech.write(joined_path_czech)
        merger_foreign.write(joined_path_foreign)
        merger_czech.close()
        merger_foreign.close()

        with open(download_path + f"/stranyprorozdeleni_uloha-{problem}_czech.txt", "w") as f:
            json.dump(dictnarozdeleni_czech, f)
        with open(download_path + f"/stranyprorozdeleni_uloha-{problem}_foreign.txt", "w") as f:
            json.dump(dictnarozdeleni_foreign, f)

        jp_czech = get_pages(joined_path_czech)
        jp_foreign = get_pages(joined_path_foreign)
        print(f'Joined pages (Czech): {jp_czech}')
        print(f'Joined pages (Foreign): {jp_foreign}')
        print()

        if split_exceptions:
            exc_path = download_path + f'/exceptions/uloha-{problem}'
            if not os.path.exists(exc_path):
                os.makedirs(exc_path)

            for exception in exceptions:
                a = exception.find(f'uloha')
                os.rename(exception, exc_path + exception[a+7:])

            exceptions = []

    if not split_exceptions:
        print('Exceptions:')
        exc_path = download_path + f'/exceptions'
        if not os.path.exists(exc_path):
            os.mkdir(exc_path)

        for exception in exceptions:
            print(exception)
            a = exception.find(f'uloha')
            os.rename(exception, exc_path + exception[a+7:])     

if __name__ == "__main__":
    problems = ["1", "2", "3", "4", "5", "P", "E", "S"]  

    rocnik = input('napis cislo rocniku: ')
    serie = input('napis cislo serie: ')
    split_exceptions = input('Vyjimky oddelene nebo dohromady? o/d (oddelene pro elektronicke opravovani, dohromady po tisk, default = o) ')
    print()

    download_path = f"./download/rocnik{rocnik}/serie{serie}"

    join_it(download_path, split_exceptions, problems)