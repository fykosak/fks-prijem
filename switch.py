import os, glob, shutil, json


def back_up(path):
    back_up_path = path + "/back_up_switched"
    if not os.path.exists(back_up_path):
        print("Zalohuju")
        shutil.copytree(path, back_up_path)
        print("Switched download zalohovan.\n")
    else:
        print("Nezalohuju, zaloha uz existuje.\n")

def switch_name(given_path, manynames, problems):
    for problem in problems:
        path = given_path + f"/uloha-{problem}/*"
        for p in (glob.glob(path)):
            n = os.path.basename(p)
            path = os.path.dirname(p)
            cele_jmeno = n[:n.find('-')]
            za_krestnim = cele_jmeno[cele_jmeno.find('_')+1:]
            koncovka = n[n.find('-'):]

            if '_' in za_krestnim:
                if not cele_jmeno in manynames.keys():
                    index_prijmeni = input(f'Kolikate slovo z {cele_jmeno} je prijmeni? Indexovano od 1. Kdyztak koukni do FKSDB.')
                    manynames[cele_jmeno] = index_prijmeni
                names = cele_jmeno.split('_')
                bn = names.pop(int(manynames[cele_jmeno])-1)
                for name in names:
                    bn += '_' + name  
                bn += koncovka

            else:
                bn =  za_krestnim + '_' + n[:n.find('_')] + koncovka

            #pocitac mi radi lidi jejichz jmeno zacina na "Ch" pod "C"
            if "ch" in bn[:2].lower():
                bn = "hzz" + bn[2:]

            os.rename(p,os.path.join(path, bn))

if __name__ == "__main__":

    problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']
    
    manynames_path = os.path.join(os.path.dirname(__file__), "download", "poradi_jmen_vicejmennych_resitelu.txt")

    rocnik = input('napis cislo rocniku: ')
    serie = input('napis cislo serie: ')
    path = os.path.join(os.path.dirname(__file__), "download", f"rocnik{rocnik}", f"serie{serie}")

    #nacist manynames
    if os.path.exists(manynames_path):
        with open(manynames_path,"r") as f:
            manynames = json.load(f)
    else:
        manynames = {}

    #switch
    print("Prehazuju")
    switch_name(path, manynames, problems)
    #save manynames
    with open(manynames_path,"w") as f:
        json.dump(manynames,f)

    #back up files
    back_up(path)