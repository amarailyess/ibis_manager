import os
import pathlib
import shutil
import zipfile
from data import data
import create_tree_1
import datetime

def prepare_paths():
    work_path = pathlib.Path().resolve()
    input_dir = str(work_path) + '\IBIS_Deliver\Input_Data'
    delivery_path = str(work_path) + '\IBIS_Deliver\Output_Data'
    ibis_to_rename_dir = str(work_path) + "\IBIS_Deliver\Working_Directory"
    return work_path, input_dir, delivery_path, ibis_to_rename_dir

def edit_file(file, old_name, new_name):
    with open(file, "r") as f:
        file_data = f.readlines()
    new_date = datetime.datetime.now().strftime("%Y-%m-%d")
    new_year = datetime.datetime.now().strftime("%Y")
    file_data[1] = file_data[1].replace(old_name, new_name)
    file_data[7] = file_data[7].replace(old_name, new_name)
    file_data[18] = file_data[18].replace(old_name.split('.')[0], new_name.split('.')[0])
    file_data[21] = file_data[21].replace(old_name.split('.')[0], new_name.split('.')[0])
    file_data[9] = file_data[9].replace(file_data[9].split('  ')[1], new_date) + '\n'
    file_data[15] = file_data[15].replace(file_data[15].split(' ')[2], new_year)

    file_data[2] = file_data[2].replace(file_data[2], "")
    file_data[3] = file_data[3].replace(file_data[3], "")
    file_data[4] = file_data[4].replace(file_data[4], "")

    with open(file, "w") as f:
        f.writelines(file_data)
    f.close()

def rename_files(ibis_to_rename_dir, delivery_path):
    for dir in os.listdir(ibis_to_rename_dir):
        dir_path = str(ibis_to_rename_dir) + str('\\') + str(dir)
        for sub_dir in os.listdir(dir_path):
            old_file_path = str(dir_path) + str('\\') + str(sub_dir)
            new_file_path = str(delivery_path) + str('\\') + str(dir)
            if sub_dir != "Zip_from_web":
                for file in os.listdir(old_file_path):
                    for item in data:
                        for p in item["package"]:
                            if p in file and file.index(p) + len(p) == file.index('.') and sub_dir == item["internal_name"] and dir.upper() == item['family']:
                                new_file_name = file.replace(item["old_name"], item["new_name"])
                                rename = False
                                if new_file_name != file:
                                    try:
                                        os.rename(old_file_path + str('\\') + file,
                                                  old_file_path + str('\\') + new_file_name)
                                        rename = True
                                    except:
                                        rename = False
                                        print("Error RENAME or MOVE FILE ==> ", file, '!!!  :(')
                                    if rename == True:
                                        edit_file(old_file_path + str('\\') + new_file_name, file, new_file_name)
                                        try:
                                            shutil.move(old_file_path + str('\\') + new_file_name, new_file_path)
                                        except:
                                            print("Error MOVE FILE ==> ", new_file_name, ' TO new_files!!!  :(')
            else:
                extract_latest_zip_files_version(old_file_path)
                for file in os.listdir(old_file_path):
                    try:
                        shutil.move(old_file_path + str('\\') + file, new_file_path)
                    except:
                        print("Error MOVE FILE ==> ", new_file_name, ' TO new_files!!!  :(')




def extract_latest_zip_files_version(zip_path):
    for dir in os.listdir(zip_path):
        if (".zip" in dir):
            try:
                zip_file_path = zip_path + str("\\") + dir
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(zip_path)
                os.remove(zip_file_path)
                print(" EXTRACT ZIP FILE DONE    :)")
            except:
                print(" ERROR EXTRACT ZIP FILE !!!    :(")





if __name__ == '__main__':
    print("SCRIPT STARTED ...")
    print("CREATED FOLDERS TREE ...")
    dir_name = create_tree_1.create_forlders()
    print("RENAME PROCESS STARTED ...")
    work_path, input_dir, delivery_path, ibis_to_rename_dir = prepare_paths()
    print("RENAMR STARTED ...")
    rename_files(ibis_to_rename_dir, delivery_path)
    print("******** SCRIPT FINISHED **********")
