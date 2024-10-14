import os, os.path, glob

class ExistsError(Exception):
    pass

def check_and_save_submitids(local_path, submitids_path, problems):
    submitids = []
    errors = []

    for problem in problems:
        path_list = glob.glob( local_path[:-1] + f'uloha-{problem}/*')
        pdf_list = [path for path in path_list if 'pdf' in path[-4:].lower()]
        for pdf in pdf_list:
            idpozice = pdf.find("__")+2
            submitid = pdf[idpozice:idpozice+5]
            try:
                submitids.append(int(submitid))
            except:
                errors.append(pdf)

    if len(errors) > 0:
        for error in errors:
            print(error)
        raise ValueError(f"Nonvalid submitid(s) found")

    #else
    print("All submitids ok")

    #pokud uz neexistuje
    if os.path.exists(submitids_path):
        raise ExistsError(f"{submitids_path} already exists. Move to prevent overwrite.")

    with open(submitids_path, "w") as f:
        for submitid in submitids:
            print(f"{submitid},", file = f, end=" ")
        print(f"{len(submitids)} submitids saved at {submitids_path}")


def upload(local_path, remote_path, username, temp_path = "./temp", server_name = "fykos.cz"):
    """odkud kam kdo uploaduje"""
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    command = f"scp -r {local_path} {username}@{server_name}:{remote_path}"
    os.system(command)


if __name__ == "__main__":

    problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']

    rocnik = int(input('napis cislo rocniku: '))
    serie = int(input('napis cislo serie: '))
    username = input('napis login na server: ')
    print()

    #do upload dat slozky uloha-U
    local_path = f"./corrected/rocnik{rocnik}/serie{serie}/upload_me/*"
    remote_path = f"/data/docker/fksdb/upload/corrected/fykos/rocnik{rocnik}/serie{serie}"
    submitids_path = f"./corrected/rocnik{rocnik}/serie{serie}/submitids.txt"

    check_and_save_submitids(local_path, submitids_path, problems)
    upload(local_path, remote_path, username)




