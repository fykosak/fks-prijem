try:
    import pypdf
except ImportError:
    print("Error: pypdf package not found!")
    print("Please install requirements by running:")
    print("pip install -r requirements.txt")
    exit(-1)

import download, switch, pdfjoin
import os
import json
import getpass

if __name__ == "__main__":
    problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S'] #feel free to change this if you want only some problems

    rocnik = int(input('Zadejte číslo ročníku: '))
    serie = int(input('Zadejte číslo série: '))
    username = input('Zadejte login na server: ')
    split_exceptions = input('Vyjimky oddelene nebo dohromady? o/d (oddelene pro elektronicke opravovani, dohromady po tisk, default = o) ')
    password = getpass.getpass(prompt="Heslo ssh klíče (pokud nemáš, nech prázdné): ")

    upload_path = f"/data/docker/fksdb/upload/fykos/rocnik{rocnik}/serie{serie}"
    download_path = os.path.join(os.path.dirname(__file__), "download", f"rocnik{rocnik}", f"serie{serie}")

    print("\nSTEP 1: DOWNLOAD")
    if not os.path.exists(download_path) \
        or input("Download directory already exists. Download again? (Y/n): ").lower() != 'n':
            print("Downloading... This might take a while :D")
            download.download(upload_path, download_path, username, password, problems)
    
    print("\nSTEP 2: HANDLE NAME SWITCHING")
    #nacist manynames
    manynames_path = os.path.join(os.path.dirname(__file__), "download", "poradi_jmen_vicejmennych_resitelu.txt")
    if os.path.exists(manynames_path):
        with open(manynames_path,"r") as f:
            manynames = json.load(f)
    else:
        print("\nWarning: poradi_jmen_vicejmennych_resitelu.txt not found!")
        print("The file should be located at:", manynames_path)
        manynames = {}
    
    #switch
    print("Switching names...")
    switch.switch_name(download_path, manynames, problems)
    print("Switching names finished!")

    #save manynames
    with open(manynames_path,"w") as f:
        json.dump(manynames,f)

    print("\nSTEP 3: BACKUP FILES")
    switch.back_up(download_path)

    print("\nSTEP 4: JOINING PDFs")
    pdfjoin.join_it(download_path, split_exceptions, problems)
    print("Joining PDFs finished!")

    print("\nSTEP 5: PREPARE CORRECTED FOLDER")
    correct_path = os.path.join(os.path.dirname(__file__), "corrected", f"rocnik{rocnik}", f"serie{serie}")
    if not os.path.exists(correct_path):
        os.makedirs(correct_path)
    print("\nCreated folder for corrected pdfs:", correct_path)
    print("\nMake prijem finished succesfully!")
