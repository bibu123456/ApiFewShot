import os

def makeDatasetDirStruct(base_path):
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    os.mkdir(base_path + 'all/')
    os.mkdir(base_path + 'train/')
    os.mkdir(base_path + 'validate/')
    os.mkdir(base_path + 'test/')
    os.mkdir(base_path + 'models/')

    os.mkdir(base_path + 'data/')
    os.mkdir(base_path + 'data/train/')
    os.mkdir(base_path + 'data/validate/')
    os.mkdir(base_path + 'data/test/')
    os.mkdir(base_path + 'doc/')

    print('Done')
    
if __name__ == "__main__":
    base_path = 'D:/CreateDatasets/new_datasets/'
    makeDatasetDirStruct(base_path)
    