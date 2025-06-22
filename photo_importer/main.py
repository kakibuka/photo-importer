from photo_importer.db import initializeDatabase, retrieveLastImported, insertLastImported
import argparse
import os
import shutil
from datetime import datetime

def retrieveInput(path):
    for subpath in os.scandir(path):
        if subpath.is_dir():
            yield from retrieveInput(subpath)
        else:
            yield subpath

def main():
    parser = argparse.ArgumentParser(description='Photo importer')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    lastImported = retrieveLastImported()
    print("Import images created after {}".format(lastImported.isoformat()))

    initializeDatabase()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    for imgPath in (retrieveInput(os.path.join(args.input, "DCIM"))):
        fileStat =  imgPath.stat()
        creationTime = datetime.fromtimestamp(fileStat.st_birthtime if fileStat.st_birthtime is not None else fileStat.st_ctime)
        if creationTime > lastImported:
            outputDir = os.path.join(args.output ,creationTime.strftime("%Y-%m-%d"))
            if not os.path.exists(outputDir):
                os.makedirs(outputDir)
                print("Created output directory {}".format(outputDir))
            print("Importing {}. creation date: {}".format(imgPath.name, creationTime.isoformat()))
            shutil.copy2(imgPath.path, outputDir)
    insertLastImported()

if __name__ == '__main__':
    main()