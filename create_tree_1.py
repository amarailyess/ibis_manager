import os
import pathlib

from data import cards_infos


def create(dirname):
    try:
        pathlib.Path(dirname).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(os.path.basename(dirname), "Folder Already exists!")
    else:
        print(os.path.basename(dirname), " Folder was created successfully")

def create_forlders():
    pathlib.Path().resolve()
    test_path = "C:/IBIS"

    ibis_deliver_path = os.path.join(test_path, "IBIS_Deliver")
    create(ibis_deliver_path)
    os.chdir(ibis_deliver_path)
    create("Input_Data")
    create("Output_Data")
    create("Working_Directory")
    os.chdir("Input_Data")

    for info in cards_infos:
        create(info['name'])
        os.chdir(info['name'])

        for internal in info['internals']:
            create(internal)
            create('Zip_from_web')
            os.chdir(internal)
            os.chdir("..")
        os.chdir("..")

    os.chdir(os.path.join(ibis_deliver_path, "Output_Data"))
    for info in cards_infos:
        create(info['name'])
    os.chdir("../..")