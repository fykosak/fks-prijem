import os
import os.path
import glob
import re


class ExistsError(Exception):
    pass


def check_and_save_submitids(local_path, submitids_path, problems):
    submit_ids = []
    errors = []

    for problem in problems:
        path_list = glob.glob(local_path[:-1] + f'uloha-{problem}/*')
        pdf_list = [path for path in path_list if 'pdf' in path[-4:].lower()]
        for pdf_name in pdf_list:
            submit_id_match = re.search(r"__([0-9]*)", pdf_name)
            if submit_id_match is None:
                errors.append(pdf_name)
                continue
            submit_id = submit_id_match.group(1)
            try:
                submit_ids.append(int(submit_id))
            except:
                errors.append(pdf_name)

    if len(errors) > 0:
        for error in errors:
            print(error)
        raise ValueError(f"Nonvalid submitid(s) found")

    # else
    print("All submitids ok")

    # pokud uz neexistuje
    if os.path.exists(submitids_path):
        raise ExistsError(f"{submitids_path} already exists. Move to prevent overwrite.")

    with open(submitids_path, "w") as f:
        for submit_id in submit_ids:
            print(f"{submit_id},", file=f, end=" ")
        print(f"{len(submit_ids)} submitids saved at {submitids_path}")


def upload(local_path, remote_path, username, temp_path="./temp", server_name="fykos.cz"):
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

    # do upload dat slozky uloha-U
    local_path = os.path.join(os.path.dirname(__file__), "corrected",
                              f"rocnik{rocnik}", f"serie{serie}", "upload_me", "*")
    remote_path = f"/data/docker/fksdb/upload/corrected/fykos/rocnik{rocnik}/serie{serie}"
    submitids_path = os.path.join(os.path.dirname(__file__), "corrected",
                                  f"rocnik{rocnik}", f"serie{serie}", "submitids.txt")

    check_and_save_submitids(local_path, submitids_path, problems)
    upload(local_path, remote_path, username)
