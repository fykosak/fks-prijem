import os
import json
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader
from collections import OrderedDict

def init_upload_me(split_path, upload_me_path, problems, upload_foreign_only):
    back_up_path = upload_me_path + "/upload_me"
    if not os.path.exists(back_up_path):
        print("Vytvarim ./upload_me")
        
        # create the back_up_path directory
        os.makedirs(back_up_path)

        for problem in problems:
            problem_path = split_path + f'/uloha-{problem}'
            foreign_path = problem_path + '_foreign'
            czech_path = problem_path + '_czech'

            if upload_foreign_only:
                if os.path.exists(foreign_path):
                    shutil.copytree(foreign_path, back_up_path + f'/uloha-{problem}')
            else:
                # Copy both Czech and foreign files
                if os.path.exists(czech_path):
                    shutil.copytree(czech_path, back_up_path + f'/uloha-{problem}')
                if os.path.exists(foreign_path):
                    shutil.copytree(foreign_path, back_up_path + f'/uloha-{problem}')
        
        print("upload_me vytvoren.\n")
    else:
        print("upload_me uz existuje.\n")

def split_it(joined_and_split_dir, stranytxt_dir, problems):
    stranysouhlasi = True
    kdenesouhlasi = []
    
    for problem in problems:
        for file_type in ['czech', 'foreign']:
            split_path = joined_and_split_dir + f'/zaloha_split/uloha-{problem}_{file_type}'
            joined_path = joined_and_split_dir + f'/joined_uloha-{problem}_{file_type}.pdf' 
            stranytxtpath = stranytxt_dir + f"/stranyprorozdeleni_uloha-{problem}_{file_type}.txt"

            print(f'uloha: {problem} - {file_type}')

            if not os.path.exists(split_path):
                os.makedirs(split_path)

            if not os.path.exists(joined_path):
                print(f"Joined file for problem {problem} - {file_type} does not exist. Skipping.")
                continue

            #nacteme ulozeny pocet stran
            with open(stranytxtpath,"r") as f:
                dictnarozdeleni = OrderedDict(json.load(f))

            with open(joined_path, "rb") as joinedf:
                reader = PdfFileReader(joinedf)
                joinedpages = reader.getNumPages()
                print(f"Pocet stran joined u{problem} - {file_type}: {joinedpages}")
            
                pozice = 0

                for pdf in dictnarozdeleni.keys():
                    pages = dictnarozdeleni[pdf]
                    outpath = os.path.join(split_path, os.path.basename(pdf))

                    writer = PdfFileWriter()
                    for i in range(pages):
                        writer.addPage(reader.getPage(pozice))
                        pozice += 1 #posouvame pozici

                    with open(outpath,"wb") as outf:
                        writer.write(outf)
                print(f"Celkovy pocet stran vytvorenych pdf u{problem} - {file_type}: {pozice}")
                print()

            if pozice != joinedpages:
                stranysouhlasi = False
                kdenesouhlasi.append(f"{problem} - {file_type}")

    if stranysouhlasi:
        print("Strany sedi")
    else:
        print("Strany nesedi v techto ulohach")
        print(kdenesouhlasi)

if __name__ == "__main__":
    problems = ["1","2","3","4","5","P","E","S"]

    rocnik = input('napis cislo rocniku: ')
    serie = input('napis cislo serie: ')
    upload_foreign_only = input('Chces uploadovat jen zahranicni (z) nebo vse (v)?')
    upload_foreign_only = (upload_foreign_only.lower() == "z")

    joined_and_split_dir = f'./corrected/rocnik{rocnik}/serie{serie}'
    stranytxt_dir = f"./download/rocnik{rocnik}/serie{serie}"

    split_it(joined_and_split_dir, stranytxt_dir, problems)
    init_upload_me(joined_and_split_dir + f'/zaloha_split', joined_and_split_dir, problems, upload_foreign_only)