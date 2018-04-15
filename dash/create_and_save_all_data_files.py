from dash.training_parameters import create_training_params_file
from dash.create_training_set import create_training_set_files
from dash.create_template_set import create_template_set_file
from dash.deep_learning_multilayer import train_model
import zipfile
import os
import shutil
import time

scriptDirectory = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    modelName = 'agnosticZ'
    dataDirName = os.path.join(scriptDirectory, 'data_files_{0}/'.format(modelName))
    dataFilenames = []
    if not os.path.exists(dataDirName):
        os.makedirs(dataDirName)

    # MAKE INFO TEXT FILE ABOUT MODEL
    modelInfoFilename = dataDirName + "model_info.txt"
    with open(modelInfoFilename, "w") as f:
        f.write("Date Time: %s\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        f.write("Directory: %s\n" % dataDirName)
        f.write("Add Host: True\n")
        f.write("SN-Host fractions: [0.99, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]\n")
        f.write("Classify Host: False\n")
        f.write("Redshift: Zero\n")
        f.write("Redshift Range: 0 to 0.8\n")
        f.write("Num of Redshifts: 20\n")
        f.write("Fraction of Training Set Used: 0.8\n")
        f.write("Training Amount: 50 x 500000\n")
        f.write("Changed wavelength range to 3000 to 10000A\n")
        f.write("Set outer region to 0.5\n")
        dataFilenames.append(modelInfoFilename)

    # CREATE PARAMETERS PICKLE FILE
    t1 = time.time()
    trainingParamsFilename = create_training_params_file(dataDirName)
    dataFilenames.append(trainingParamsFilename)
    t2 = time.time()
    print("time spent: {0:.2f}".format(t2 - t1))

    # CREATE TRAINING SET FILES
    trainingSetFilename = create_training_set_files(dataDirName, minZ=0., maxZ=0.8, numOfRedshifts=20, trainWithHost=True, classifyHost=False)
    dataFilenames.append(trainingSetFilename)
    t3 = time.time()
    print("time spent: {0:.2f}".format(t3 - t2))

    # TRAIN TENSORFLOW MODEL
    modelFilenames = train_model(dataDirName)
    dataFilenames.extend(modelFilenames)
    t4 = time.time()
    print("time spent: {0:.2f}".format(t4 - t3))

    # SAVE ALL FILES TO ZIP FILE
    dataFilesZip = 'data_files_{0}.zip'.format(modelName)
    with zipfile.ZipFile(dataFilesZip, 'w') as myzip:
        for f in dataFilenames:
            myzip.write(f)

    modelZip = 'model_{0}.zip'.format(modelName)
    with zipfile.ZipFile(modelZip, 'w') as myzip:
        for f in [dataFilenames[0:2]] + dataFilenames[3:]:
            myzip.write(f)

    # Delete data_files folder since they are now in the zip files
    # for filename in filenames:
    #     os.remove(filename)
