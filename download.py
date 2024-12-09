import os
import getpass

def download(upload_path, download_path, username, password, problems, temp_path = "./temp", server_name = "fykos.cz"):
    """odkud kam kdo stahuje"""
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    if len(problems) < 8: #pokud chceme jen nektere ulohy
        for problem in problems:
            problem_upload_path = upload_path + f"/uloha-{problem}"
            problem_download_path = download_path + f"/uloha-{problem}"

            if not os.path.exists(problem_download_path):
                os.makedirs(problem_download_path)
            ssh_command = f"ssh {username}@{server_name} 'cd \"{problem_upload_path}\" && tar --exclude=\'*.bak\' -czf - .' | (cd \"{problem_download_path}\" && tar -xzf -)"
            if (password):
                command = f"sshpass -p '{password}' "+ ssh_command
            else:
                command = ssh_command
            res = os.system(command)
            if res != 0:
                raise Exception(f"Download of problem {problem} failed!")
                

    else: #defaultne vsechno
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        command = f"ssh {username}@{server_name} 'cd \"{upload_path}\" && tar --exclude=\'*.bak\' -czf - .' | (cd \"{download_path}\" && tar -xzf -)"
        res = os.system(command)
        if res != 0:
            raise Exception(f"Download failed!")


if __name__ == "__main__":
    problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']

    rocnik = int(input('Zadejte číslo ročníku: '))
    serie = int(input('Zadejte číslo série: '))
    username = input('Zadejte login na server: ')
    password = getpass.getpass(prompt="heslo (nebo prázdné): ")

    download_path = os.path.join(os.path.dirname(__file__), "download", f"rocnik{rocnik}", f"serie{serie}")
    upload_path = f"/data/docker/fksdb/upload/fykos/rocnik{rocnik}/serie{serie}/*"

    download(upload_path, download_path, username, password, problems)
