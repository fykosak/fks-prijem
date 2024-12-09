import os
import json
import shutil
from pypdf import PdfReader, PdfWriter
from collections import OrderedDict
import logging
import io

# handler to catch warnings
log_stream = io.StringIO()
handler = logging.StreamHandler(log_stream)
logging.getLogger().addHandler(handler)

def init_upload_me(split_path, upload_me_path, problems, upload_foreign_only):
    back_up_path = os.path.join(os.path.dirname(__file__), upload_me_path, "upload_me")
    if os.path.exists(back_up_path):
        print("upload_me uz existuje. Vpisuji do něj!\n")
    else:
        # create the back_up_path directory
        os.makedirs(back_up_path)
    print("Vytvarim ./upload_me")
    

    for problem in problems:
        problem_path = split_path + f'/uloha-{problem}'
        foreign_path = problem_path + '_foreign'
        czech_path = problem_path + '_czech'

        if upload_foreign_only:
            if os.path.exists(foreign_path):
                shutil.copytree(foreign_path, back_up_path + f'/uloha-{problem}', dirs_exist_ok=True)
        else:
            # Copy both Czech and foreign files
            if os.path.exists(czech_path):
                shutil.copytree(czech_path, back_up_path + f'/uloha-{problem}', dirs_exist_ok=True)
            if os.path.exists(foreign_path):
                shutil.copytree(foreign_path, back_up_path + f'/uloha-{problem}', dirs_exist_ok=True)
    
    print("upload_me vytvoren.\n")

def split_it(joined_and_split_dir, stranytxt_dir, problems):
    stranysouhlasi = True
    kdenesouhlasi = []
    split_warnings = {}
    
    for problem in problems:
        for file_type in ['czech', 'foreign']:
            split_path = os.path.join(os.path.dirname(__file__), joined_and_split_dir, 'zaloha_split', f'uloha-{problem}_{file_type}')
            joined_path = os.path.join(os.path.dirname(__file__), joined_and_split_dir, f'joined_uloha-{problem}_{file_type}.pdf')
            stranytxtpath = os.path.join(os.path.dirname(__file__), stranytxt_dir, f'stranyprorozdeleni_uloha-{problem}_{file_type}.txt')

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
                reader = PdfReader(joinedf)
                joinedpages = reader.get_num_pages()
                print(f"Pocet stran joined u {problem} - {file_type}: {joinedpages}")
            
                pozice = 0

                for pdf in dictnarozdeleni.keys():
                    pages = dictnarozdeleni[pdf]
                    outpath = os.path.join(split_path, os.path.basename(pdf))
                    
                    writer = PdfWriter()
                    for i in range(pages):
                        writer.add_page(reader.get_page(pozice))
                        pozice += 1 #posouvame pozici

                    with open(outpath,"wb") as outf:
                        writer.write(outf)

                    # read warnings
                    warnings = log_stream.getvalue()
                    log_stream.truncate(0)
                    log_stream.seek(0)
                    if warnings:
                        split_warnings[outpath] = warnings

                print(f"Celkovy pocet stran vytvorenych pdf u {problem} - {file_type}: {pozice}")
                print()

            if pozice != joinedpages:
                stranysouhlasi = False
                kdenesouhlasi.append(f"{problem} - {file_type}")

    if stranysouhlasi:
        print("Strany sedi")
    else:
        print("Strany nesedi v techto ulohach")
        print(kdenesouhlasi)
    
    warnings_count = len(split_warnings.keys())
    if warnings_count:
        input(f"\nPress Enter to show {warnings_count} PDF warnings: ")
        print(*[f"FILE {k}\n{v.strip()}" for k, v in split_warnings.items()], sep="\n----\n", end="\n\n")

if __name__ == "__main__":
    problems = ["1","2","3","4","5","P","E","S"]

    rocnik = int(input('Zadejte číslo ročníku: '))
    serie = int(input('Zadejte číslo série: '))
    upload_foreign_only = input('Chceš uploadovat vše nebo jen zahraniční (V/z)? ').lower() == "z"

    joined_and_split_dir = os.path.join(os.path.dirname(__file__), 'corrected', f'rocnik{rocnik}', f'serie{serie}')
    stranytxt_dir = os.path.join(os.path.dirname(__file__), 'download', f'rocnik{rocnik}', f'serie{serie}')

    print("\nSTEP 1: SPLIT")
    split_it(joined_and_split_dir, stranytxt_dir, problems)
    print("\nSTEP 2: CREATE upload_me")
    init_upload_me(joined_and_split_dir + f'/zaloha_split', joined_and_split_dir, problems, upload_foreign_only)