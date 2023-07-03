import download, switch, pdfjoin
import os
import json
import getpass

if __name__ == "__main__":
    
    problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S'] #feel free to change this if you want only some problems

    rocnik = int(input('napis cislo rocniku: '))
    serie = int(input('napis cislo serie: '))
    username = input('napis login na server: ')
    split_exceptions = input('Vyjimky oddelene nebo dohromady? o/d (oddelene pro elektronicke opravovani, dohromady po tisk, default = o) ')
    password = getpass.getpass(prompt="Heslo ssh klíče (pokud nemáš, nech prázdné): ")

    upload_path = f"/network/data/www/fykos/db.fykos.cz/upload/fykos/rocnik{rocnik}/serie{serie}/*"
    download_path = f"./download/rocnik{rocnik}/serie{serie}"

    download.download(upload_path, download_path, username, password, problems)

    #nacist manynames
    manynames_path = "download/poradi_jmen_vicejmennych_resitelu.txt"
    if os.path.exists(manynames_path):
        with open(manynames_path,"r") as f:
            manynames = json.load(f)
    else:
        manynames = {}

    #switch
    print("Prehazuju")
    switch.switch_name(download_path, manynames, problems)

    #save manynames
    with open(manynames_path,"w") as f:
        json.dump(manynames,f)

    #back up files
    switch.back_up(download_path)

    #join it  
    pdfjoin.join_it(download_path, split_exceptions, problems)