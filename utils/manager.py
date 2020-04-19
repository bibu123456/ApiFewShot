import numpy as np
from time import time
import torch as t
from platform import uname

from utils.file import loadJson

##########################################################
# 项目数据集路径管理器。
# 可以使用方法获取数据集路径。
# d_type用于指定当前使用的是训练集，验证集还是测试集，指定为all时代表
# 三者均不是。
##########################################################
class PathManager:

    # 文件父目录
    ParentPath = 'D:/peimages/JSONs/'

    # 数据文件夹路径
    FolderPathTemp = '%s/%s/'

    # 模型保存路径
    ModelPathTemp = '%s/models/%s'

    # 词嵌入矩阵路径
    WordEmbedMatrixPathTemp = '%s/data/matrix.npy'

    # 词转下标表路径
    WordIndexMapPathTemp = '%s/data/wordMap.json'

    # 文件型数据路径
    FileDataPathTemp = '%s/data/%s/data.npy'
    # 文件数据对应的长度表路径
    FileSeqLenPathTemp = '%s/data/%s/seqLength.json'
    DocTemp = '%s/doc/%d/'

    def __init__(self, dataset, model_name=None, d_type='all',
                 cfg_path='../run/runConfig.json',
                 version=1):
        manager = TrainingConfigManager(cfg_path)
        parent_path = manager.systemParams()

        self.ParentPath = parent_path

        # 不允许在指定all时访问数据分割路径
        BanedListWhenAll = ['FileDataPath', 'FileSeqLenPath']

        self.DataType = d_type

        self.FolderPath = self.ParentPath + self.FolderPathTemp % (dataset, d_type)

        self.WordEmbedMatrixPath = self.ParentPath + self.WordEmbedMatrixPathTemp % dataset
        self.WordIndexMapPath = self.ParentPath + self.WordIndexMapPathTemp % dataset

        self.FileDataPath = self.ParentPath + self.FileDataPathTemp % (dataset, d_type)
        self.FileSeqLenPath = self.ParentPath + self.FileSeqLenPathTemp % (dataset, d_type)

        self.ModelPath = self.ParentPath + self.ModelPathTemp % (dataset, model_name)
        self.DocPath = self.ParentPath + self.DocTemp % (dataset, version)

    def Folder(self):
        return self.FolderPath

    def WordEmbedMatrix(self):
        return self.WordEmbedMatrixPath

    def WordIndexMap(self):
        return self.WordIndexMapPath

    def FileData(self):
        if self.DataType == 'all':
            raise ValueError('在数据分割为all时，不允许访问FileData')
        else:
            return self.FileDataPath

    def FileSeqLen(self):
        if self.DataType == 'all':
            raise ValueError('在数据分割为all时，不允许访问FileSeqLen')
        else:
            return self.FileSeqLenPath

    def Model(self):
        return self.ModelPath

    def Doc(self):
        return self.DocPath


#########################################
# 训练时的统计数据管理器。主要用于记录训练和验证的
# 正确率和损失值，并且根据选择的标准来选择最优模型
# 保存和打印训练数据。在记录验证数据时会打印训练和
# 验证信息
#########################################
class TrainStatManager:

    def __init__(self, model_save_path, train_report_iter=100, criteria='loss'):
        self.TrainHist = {'accuracy': [],
                          'loss': []}
        self.ValHist = {'accuracy': [],
                          'loss': []}

        assert criteria in self.TrainHist.keys(), '给定的标准 %s 不在支持范围内!'%criteria

        self.ModelSavePath = model_save_path
        self.Criteria = criteria
        self.BestVal = float('inf') if criteria=='loss' else -1.
        self.BestValEpoch = -1
        self.TrainReportIter = train_report_iter
        self.TrainIterCount = -1

        self.PreTimeStamp = None
        self.CurTimeStamp = None

    def startTimer(self):
        self.CurTimeStamp = time()

    def recordTraining(self, acc, loss):
        self.TrainHist['accuracy'].append(acc)
        self.TrainHist['loss'].append(loss)
        self.TrainIterCount += 1

    def recordValidating(self, acc, loss, model):
        self.ValHist['accuracy'].append(acc)
        self.ValHist['loss'].append(loss)

        if self.Criteria == 'loss':
            if loss < self.BestVal:
                self.BestValEpoch = self.TrainIterCount
                self.BestVal = loss
                t.save(model.state_dict(), self.ModelSavePath)

        else:
            if acc > self.BestVal:
                self.BestValEpoch = self.TrainIterCount
                self.BestVal = acc
                t.save(model.state_dict(), self.ModelSavePath)

        self.PreTimeStamp = self.CurTimeStamp
        self.CurTimeStamp = time()

        record = self.getRecentRecord()
        self.printOut(*record)

    def printOut(self, average_train_acc, average_train_loss, recent_val_acc, recent_val_loss):
        print('***********************************')
        print('train acc: ', average_train_acc)
        print('train loss: ', average_train_loss)
        print('----------------------------------')
        print('val acc:', recent_val_acc)
        print('val loss:', recent_val_loss)
        print('----------------------------------')
        print('best val %s:' % self.Criteria, self.BestVal)
        print('best epoch:', self.BestValEpoch)
        print('time consuming:', self.CurTimeStamp - self.PreTimeStamp)
        print('\n***********************************')
        print('\n\n%d -> %d epoches...' % (self.TrainIterCount, self.TrainIterCount + self.TrainReportIter))

    def getRecentRecord(self):
        average_train_acc = np.mean(self.TrainHist['accuracy'][-1*self.TrainReportIter:])
        average_train_loss = np.mean(self.TrainHist['loss'][-1*self.TrainReportIter:])
        recent_val_acc = self.ValHist['accuracy'][-1]
        recent_val_loss = self.ValHist['loss'][-1]

        return average_train_acc, average_train_loss, recent_val_acc, recent_val_loss

    def getHistAcc(self):
        t,v = self.TrainHist['accuracy'], self.ValHist['accuracy']
        t,v = np.array(t), np.array(v)
        t = np.mean(t.reshape(-1,self.TrainReportIter),axis=1)
        return t,v

    def getHistLoss(self):
        t, v = self.TrainHist['loss'], self.ValHist['loss']
        t, v = np.array(t), np.array(v)
        t = np.mean(t.reshape(-1, self.TrainReportIter), axis=1)
        return t, v

class TrainingConfigManager:

    def __init__(self, cfg_path):
        self.Cfg = loadJson(cfg_path)

    def taskParams(self):
        dataset = self.Cfg['dataset']
        N = self.Cfg['Ns'][dataset]

        return self.Cfg['k'],\
               self.Cfg['n'],\
               self.Cfg['qk'], \
               N

    def model(self):
        return self.Cfg['modelName'],\
        '{model}_v{version}.0'.format(
            model=self.Cfg['modelName'],
            version=self.Cfg['version']
        )

    def dataset(self):
        return self.Cfg['dataset']

    def modelParams(self):
        return self.Cfg['embedSize'], \
               self.Cfg['hiddenSize'], \
               self.Cfg['biLstmLayer'], \
               self.Cfg['selfAttDim'], \
               self.Cfg['usePretrained'], \
               self.Cfg['wordCount']

    def valParams(self):
        return self.Cfg['valCycle'], \
               self.Cfg['valEpisode']

    def trainingParams(self):
        return self.Cfg['lrDecayIters'], \
               self.Cfg['lrDecayGamma'], \
               self.Cfg['optimizer'], \
               self.Cfg['weightDecay'], \
               self.Cfg['lossFunction'], \
               self.Cfg['defaultLr'], \
               self.Cfg['lrs'], \
               self.Cfg['taskBatchSize']

    def gradRecParams(self):
        return self.Cfg['recordGradient'], \
               self.Cfg['gradientUpdateCycle']

    def verboseParams(self):
        return self.Cfg['trainingVerbose'], \
               self.Cfg['useVisdom']

    def plotParams(self):
        return self.Cfg['plot']['types'], \
               self.Cfg['plot']['titles'], \
               self.Cfg['plot']['xlabels'], \
               self.Cfg['plot']['ylabels'], \
               self.Cfg['plot']['legends']

    def epoch(self):
        return self.Cfg['trainingEpoch']

    def systemParams(self):
        system = uname().system
        return self.Cfg['platform'][system]["datasetBasePath"]

    def version(self):
        return self.Cfg['version']




