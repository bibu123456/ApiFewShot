import matplotlib.pyplot as plt
import torch as t
from torch.utils.data.dataloader import DataLoader
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE,MDS,LocallyLinearEmbedding
import numpy as np

from models.ProtoNet import ProtoNet
from utils.color import getRandomColor
from models.IMP import IMP
from models.ImpIMP import ImpIMP
from models.HybridIMP import HybridIMP

from components.datasets import SeqFileDataset
from utils.manager import PathManager, TrainingConfigManager
from utils.training import batchSequenceWithoutPad
from components.task import ImpEpisodeTask
from utils.magic import magicSeed

# ***************************************************************************
dataset_name = 'virushare-20-3gram'
dataset_subtype = 'test'
model_name = 'IMP'
version = 141
N = 20
plot_option = 'entire'#'entire'
k, n, qk = 5, 5, 15
figsize = (12,10)
task_seed = magicSeed()
sampling_seed = magicSeed()
# ***************************************************************************


path_man = PathManager(dataset=dataset_name,
                       d_type=dataset_subtype,
                       model_name=model_name,
                       version=version)

################################################
#----------------------读取模型参数------------------
################################################

model_cfg = TrainingConfigManager(path_man.Doc()+'config.json')

modelParams = model_cfg.modelParams()

dataset = SeqFileDataset(path_man.FileData(), path_man.FileSeqLen(), N=N)

state_dict = t.load(path_man.Model() + '_v%s.0' % version)
# state_dict = t.load(path_man.DatasetBase()+'models/ProtoNet_v105.0')
word_matrix = state_dict['Embedding.weight']

if model_name == 'IMP':
    model = IMP(word_matrix,
                **modelParams)
elif model_name == 'ImpIMP':
    model = ImpIMP(word_matrix,
                   **modelParams)
elif model_name == 'HybridIMP':
    model = HybridIMP(word_matrix,
                      **modelParams)
elif model_name == 'ProtoNet':
    model = ProtoNet(word_matrix,
                     **modelParams)

model.load_state_dict(state_dict)
model = model.cuda()
model.eval()

if plot_option == 'entire':
    dataloader = DataLoader(dataset, batch_size=N, collate_fn=batchSequenceWithoutPad)

    datas = []
    # reduction = PCA(n_components=2)
    reduction = TSNE(n_components=2)

    class_count = 0

    for x,_,lens in dataloader:
        class_count += 1
        x = x.cuda()
        x = model._embed(x, lens).cpu().view(N,-1).detach().numpy()
        datas.append(x)

    datas = np.array(datas).reshape((class_count*N,-1))
    datas = reduction.fit_transform(datas)

    colors = ['darkgreen',
 'darkseagreen',
 'olive',
 'teal',
 'orangered',
 'yellowgreen',
 'steelblue',
 'gold',
 'magenta',
 'hotpink',
 'blueviolet',
 'red',
 'black',
 'bisque',
 'violet',
 'deepskyblue',
 'firebrick',
 'purple',
 'pink',
 'lime']#getRandomColor(class_count)
    datas = datas.reshape((class_count,N,2))

    plt.figure(figsize=figsize)
    for i in range(class_count):
        plt.scatter(datas[i,:,0],datas[i,:,1],color=colors[i],marker='o')

    plt.show()

# ***************************************************************************

elif plot_option == 'episode':
    task = ImpEpisodeTask(k,qk,n,N,
                          dataset,expand=False)

    support, query, *others = task.episode(task_seed=task_seed,
                                           sampling_seed=sampling_seed)
    support, query, acc = model(support, query, *others, if_cache_data=True)

    clusters, cluster_labels = model.Clusters.squeeze().cpu().detach(), \
                               model.ClusterLabels.squeeze().cpu().detach().numpy()

    # reduction = PCA(n_components=2)
    reduction = TSNE(n_components=2)
    # reduction = MDS(n_components=2)
    # reduction = LocallyLinearEmbedding(n_components=2, n_neighbors=2)

    support = support.cpu().detach().view(k*n, -1)
    query = query.cpu().detach().view(qk*n,-1)
    union = t.cat((support,query,clusters),dim=0).numpy()

    union = reduction.fit_transform(union)
    support = union[:n*k].reshape((n,k,2))
    query = union[n*k:-len(clusters)].reshape((n,qk,2))
    clusters = union[-len(clusters):]

    colors = getRandomColor(n)

    plt.figure(figsize=figsize)
    plt.title(f'cluster_num={len(clusters)}')
    for i in range(n):
        plt.scatter(support[i,:,0],support[i,:,1],color=colors[i],marker='o')
        # plt.scatter(query[i,:,0],query[i,:,1],color=colors[i],marker='*')

        class_clusters = clusters[cluster_labels==i]
        plt.scatter(class_clusters[:,0],class_clusters[:,1],color=colors[i],marker='x',edgecolors='k',s=80)
        plt.scatter(class_clusters[:,0],class_clusters[:,1],marker='o',c='',edgecolors='k',s=80)

    plt.show()

    plt.figure(figsize=figsize)
    plt.title(f'cluster_num={len(clusters)}')
    for i in range(n):
        plt.scatter(support[i,:,0],support[i,:,1],color=colors[i],marker='o')
        plt.scatter(query[i,:,0],query[i,:,1],color=colors[i],marker='*')

        class_clusters = clusters[cluster_labels==i]
        plt.scatter(class_clusters[:,0],class_clusters[:,1],color=colors[i],marker='x',edgecolors='k',s=80)
        plt.scatter(class_clusters[:,0],class_clusters[:,1],marker='o',c='',edgecolors='k',s=80)

    plt.show()

    print('acc: ', acc)







