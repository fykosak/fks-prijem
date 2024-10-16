import os, os.path
import getpass

def download(upload_path, download_path, username, password, problems, temp_path = "./temp", server_name = "fykos.cz"):
    """odkud kam kdo stahuje"""
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    if len(problems) < 8: #pokud chceme jen nektere ulohy
        for problem in problems:
            problem_upload_path = upload_path[:-1] + f"uloha-{problem}/*"
            problem_download_path = download_path + f"/uloha-{problem}"

            if not os.path.exists(problem_download_path):
                os.makedirs(problem_download_path)
            if (password):
                command = f"sshpass -p '{password}' scp -r {username}@{server_name}:{problem_upload_path} {problem_download_path}"
            else:
                command = f"scp -r {username}@{server_name}:{problem_upload_path} {problem_download_path}"
            os.system(command)

    else: #defaultne vsechno
        if not os.path.exists(download_path):
                os.makedirs(download_path)

        command = f"scp -r {username}@{server_name}:{upload_path} {download_path}"
        os.system(command)


if __name__ == "__main__":
    problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']

    rocnik = int(input('napis cislo rocniku: '))
    serie = int(input('napis cislo serie: '))
    username = input('napis login na server: ')
    password = getpass.getpass(prompt="heslo (nebo prázdné): ")

    download_path = f"./download/rocnik{rocnik}/serie{serie}"
    upload_path = f"/data/docker/fksdb/upload/fykos/rocnik{rocnik}/serie{serie}/*"

    download(upload_path, download_path, username, password, problems)
