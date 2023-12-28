from glove import Glove, Corpus
import numpy as np
import json
import os
from tqdm import tqdm

def dumpJson(obj, path, indent=4):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=indent)

def loadJson(path):
    with open(path, 'r') as f:
        j = json.load(f)
    return j

def aggregateApiSequences(path, is_class_dir=True):
    seqs = []

    for folder in tqdm(os.listdir(path)):
        class_folder_path = os.path.join(path, folder)

        if is_class_dir:
            items = os.listdir(class_folder_path)
        else:
            items = [folder + '.json']

        for item in items:
            if is_class_dir:
                item_path = os.path.join(class_folder_path, item, item + '.json')
            else:
                item_path = os.path.join(class_folder_path, item)

            try:
                print("Checking:", item_path)
                if os.path.isfile(item_path):  # Check if it's a file
                    print("Processing:", item_path)
                    report = loadJson(item_path)
                    apis = report['apis']

                    if len(apis) > 0:
                        seqs.append(apis)
                else:
                    print("Not a file:", item_path)
            except Exception as e:
                print("Error processing file:", item_path, e)
                exit(-1)

    return seqs



def getGloveEmbedding(seqs, size=300, window=10, epochs=20):
    corpus = Corpus()
    corpus.fit(seqs, window=window)

    glove = Glove(no_components=size, learning_rate=0.05)
    glove.fit(corpus.matrix, epochs=epochs, verbose=True)

    return corpus.dictionary, glove.word_vectors

def trainGloVe(seqs, size=300, save_matrix_path=None, save_word2index_path=None, padding=True, **kwargs):
    print('Training GloVe...')
    word2index, matrix = getGloveEmbedding(seqs, size, **kwargs)

    if padding:
        pad_matrix = np.zeros((1, matrix.shape[1]))
        matrix = np.concatenate((pad_matrix, matrix), axis=0)

        for k in word2index.keys():
            word2index[k] = word2index[k] + 1 if padding else word2index[k]
        word2index['<PAD>'] = 0

    print('Saving...')
    if save_matrix_path:
        np.save(save_matrix_path, matrix)

    if save_word2index_path:
        dumpJson(word2index, save_word2index_path)

    if save_matrix_path is None and save_word2index_path is None:
        return matrix, word2index

    print('Done')

if __name__ == '__main__':
    dataset = 'HKS'
    seqs = aggregateApiSequences("/home/kyo/datasets/%s/all/" % dataset)
    trainGloVe(seqs,
               size=300,
               save_matrix_path="/home/kyo/datasets/%s/data/matrix.npy" % dataset,
               save_word2index_path="/home/kyo/datasets/%s/data/wordMap.json" % dataset)
