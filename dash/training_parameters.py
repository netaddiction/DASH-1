import pickle


def create_training_params_file():
    parameters = {
        'typeList': ['Ia-norm', 'Ia-91T', 'Ia-91bg', 'Ia-csm', 'Ia-02cx', 'Ia-pec',
                    'Ib-norm', 'Ibn', 'IIb', 'Ib-pec', 'Ic-norm', 'Ic-broad',
                    'Ic-pec', 'IIP', 'IIL', 'IIn', 'II-pec'],
        'nTypes': 17,
        'w0': 2500.,             #wavelength range in Angstroms
        'w1': 10000.,
        'nw': 1024,             #number of wavelength bins
        'minAge': -20.,
        'maxAge': 50.,
        'ageBinSize': 4.
    }

    trainingParamsFilename = 'data_files/training_params.pickle'

    # Saving the objects:
    with open(trainingParamsFilename, 'wb') as f:
        pickle.dump(parameters, f, protocol=2)
    print("Saved files to %s" %trainingParamsFilename)

    # Getting back the objects:
    with open(trainingParamsFilename, 'rb') as f:
        pars = pickle.load(f)
    nTypes, w0, w1, nw, minAge, maxAge, ageBinSize, typeList = pars['nTypes'], pars['w0'], pars['w1'], pars['nw'], \
                                                               pars['minAge'], pars['maxAge'], pars['ageBinSize'], \
                                                               pars['typeList']

    return trainingParamsFilename

if __name__ == '__main__':
    trainingParamsFilename = create_training_params_file()

