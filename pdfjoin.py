import os
import glob
import json
from collections import OrderedDict
from pypdf import PdfWriter, PdfReader
import csv

def get_page_count(file_name):
    with open(file_name, 'rb') as file:
        pdf = PdfReader(file) 
        pg = pdf.get_num_pages()
    return pg

def pdf_ok_writing(pdf, temp_path="./temp"):
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    try:
        merger = PdfWriter()
        merger.append(pdf)
        merger.write(temp_path + "/test_can_be_deleted.pdf")
        merger.close()
        return True
    except:
        return False

def is_foreign(file_name, foreign_submitids):
    file_submitid = file_name[file_name.find("__")+2:-4]
    try:
        return file_submitid in foreign_submitids
    except:
        return False

def join_it(download_path, split_exceptions, problems):
    exceptions = []
    if split_exceptions == "d" or split_exceptions == False:
        split_exceptions = False
    else:
        split_exceptions = True

    submitids_path = os.path.join(download_path, 'submitids.csv')
    if not os.path.exists(submitids_path):
        print("\nWarning: submitids.csv not found!")
        print("This file is needed to separate foreign and Czech solutions.")
        print("Please download the list of foreign submits from fksdb (export 'Submity zahraničních řešitelů')")
        print("The file should be in:", submitids_path)
        input("\nPress Enter once you've added the file...")
        
        if not os.path.exists(submitids_path):
            raise FileNotFoundError("submitids.csv still not found. Cannot continue without it.")

    # Read the foreign submitids
    with open(os.path.join(download_path, 'submitids.csv'), 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        headers = next(csv_reader)
        submit_index = headers.index('submit')
        foreign_submitids = [row[submit_index] for row in csv_reader]
    
    for problem in problems:
        print(f'uloha: {problem}')

        writer_czech = PdfWriter()
        writer_foreign = PdfWriter()
        path_list = glob.glob(download_path + f'/uloha-{problem}/*')
        pdf_list = [path for path in path_list if 'pdf' in path[-4:].lower()]
        pdf_list = sorted(pdf_list)
        dictnarozdeleni_czech = OrderedDict()
        dictnarozdeleni_foreign = OrderedDict()

        for pdf in pdf_list:
            if pdf_ok_writing(pdf):
                reader = PdfReader(pdf)
                page_count = reader.get_num_pages()
                last_page = reader.pages[page_count-1]
                
                if is_foreign(pdf, foreign_submitids):
                    writer_foreign.append(reader)
                    if page_count % 2 != 0:
                        # if you use defaults (no params) you get: AttributeError: 'NoneType' object has no attribute 'get_object'
                        writer_foreign.add_blank_page(last_page.mediabox.width,last_page.mediabox.height)
                        page_count += 1
                    dictnarozdeleni_foreign.update({pdf: page_count})
                else:
                    writer_czech.append(reader)
                    if page_count % 2 != 0:
                        writer_czech.add_blank_page(last_page.mediabox.width,last_page.mediabox.height)
                        page_count += 1
                    dictnarozdeleni_czech.update({pdf: page_count})
            else:
                try: 
                    _ = get_page_count(pdf)
                    print("chyba writing: ", pdf)
                except:
                    print("chyba get_page_count: ", pdf)
                exceptions.append(pdf)

        joined_path_czech = download_path + f'/joined_uloha-{problem}_czech.pdf'
        joined_path_foreign = download_path + f'/joined_uloha-{problem}_foreign.pdf'
        
        writer_czech.write(joined_path_czech)
        writer_foreign.write(joined_path_foreign)
        writer_czech.close()
        writer_foreign.close()

        with open(download_path + f"/stranyprorozdeleni_uloha-{problem}_czech.txt", "w") as f:
            json.dump(dictnarozdeleni_czech, f)
        with open(download_path + f"/stranyprorozdeleni_uloha-{problem}_foreign.txt", "w") as f:
            json.dump(dictnarozdeleni_foreign, f)

        jp_czech = get_page_count(joined_path_czech)
        jp_foreign = get_page_count(joined_path_foreign)
        print(f'Joined get_page_count (Czech): {jp_czech}')
        print(f'Joined get_page_count (Foreign): {jp_foreign}')
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

    rocnik = int(input('Zadejte číslo ročníku: '))
    serie = int(input('Zadejte číslo série: '))
    split_exceptions = input('Vyjimky oddelene nebo dohromady? o/d (oddelene pro elektronicke opravovani, dohromady po tisk, default = o) ')
    print()

    download_path = os.path.join(os.path.dirname(__file__), "download", f"rocnik{rocnik}", f"serie{serie}")

    join_it(download_path, split_exceptions, problems)