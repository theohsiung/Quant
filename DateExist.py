import os.path

def CheckFileExist(path, date):
    file = path + str(date) + '.csv'
    check_file = os.path.isfile(file)

    return check_file



