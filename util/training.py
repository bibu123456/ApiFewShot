import torch as t
from torch.nn.utils.rnn import pad_sequence
import random as rd
import numpy as np

from util.magic import magicSeed


#########################################
# 使用pad_sequence来将序列补齐从而批次化。会同
# 时返回长度信息以便于将pad_sequence还原。
#########################################
def getBatchSequenceFunc(d_type='long'):

    def batchSequences(data):
        seqs = [x[0] for x in data]
        labels = t.LongTensor([x[1] for x in data])

        seqs.sort(key=lambda x: len(x), reverse=True)  # 按长度降序排列
        seq_len = [len(q) for q in seqs]
        seqs = pad_sequence(seqs, batch_first=True)

        if d_type=='long':
            return seqs.long(), labels, seq_len
        elif d_type=='float':
            return seqs.float(), labels, seq_len
        else:
            raise ValueError('无效的数据类型: %s'%d_type)

    return batchSequences


def batchSequenceWithoutPad(data):
    seqs = []
    lens = []
    labels = []

    for (seq,leng),label in data:
        seqs.append(seq.tolist())
        lens.append(leng)
        labels.append(label)

    # 注意：此时的序列没有按照长度进行排序，因此需要在pack时enforce_sort=False
    return t.LongTensor(seqs), t.LongTensor(labels), lens

################################################
# 从输入数据中获取任务元参数，如k，n，qk等
# arg:
# unsqueezed: 是否因为通道维度而增加了一个维度
# is_matrix: 是否是矩阵序列型输入
################################################
def extractTaskStructFromInput(support, query,
                               unsqueezed=False,
                               is_matrix=False):
        # support_dim_size = 6 if is_embedded else 3
        # query_dim_size = 5 if is_embedded else 2
        # len_dim_base = 1 if not is_embedded else 2      # 对于矩阵序列的输入，序列长度的维度是2([qk, in_channel=1, seq_len, height, width])

        support_dim_size = 3 + 2*is_matrix + unsqueezed
        query_dim_size = 2 + 2*is_matrix + unsqueezed
        len_dim_base = 1 if not unsqueezed else 2

        assert len(support.size()) == support_dim_size, '支持集结构 %s 不符合要求！'%(str(support.size()))

        n = support.size(0)
        k = support.size(1)
        sup_seq_len = support.size(len_dim_base+1)

        if query is not None:       # support for None query
            assert len(query.size()) == query_dim_size, '查询集结构 %s 不符合要求！' % (str(query.size()))
            qk = query.size(0)
            que_seq_len = query.size(len_dim_base)

        else:
            qk = None
            que_seq_len = None

        # assert sup_seq_len==que_seq_len, \
        #     '支持集序列长度%d和查询集序列%d长度不同！'%(sup_seq_len,que_seq_len,)

        return n, k, qk, sup_seq_len, que_seq_len

def repeatProtoToCompShape(proto, qk, n):
    proto = proto.repeat((qk, 1, 1)).view(qk, n, -1)

    return proto


def repeatQueryToCompShape(query, qk, n):
    query = query.repeat(n,1,1).transpose(0,1).contiguous().view(qk,n,-1)

    return query

def squEucDistance(v1, v2, neg=False, temperature=None):
    assert v1.size()==v2.size() and len(v1.size())==2, \
        '两组向量形状必须相同，且均为(batch, dim)结构！'

    if temperature is None:
        temperature = -1 if neg else 1
    else:
        temperature = temperature * ((-1) ** (2+neg))

    return ((v1-v2)**2).sum(dim=1) * temperature

def cosDistance(v1, v2, neg=False, factor=10):
    assert v1.size()==v2.size() and len(v1.size())==2, \
        '两组向量形状必须相同，且均为(batch, dim)结构！'

    factor = -1*factor if neg else factor

    return t.cosine_similarity(v1, v2, dim=1) * factor
    # return ((v1-v2)**2).sum(dim=1) * factor

def protoDisAdapter(support, query, qk, n, dim, dis_type='euc', **kwargs):
    support = support.view(qk*n, dim)
    query = query.view(qk*n, dim)

    if dis_type == 'euc':
        sim = squEucDistance(support, query, neg=True, **kwargs)
    elif dis_type == 'cos':
        sim = cosDistance(support, query, neg=False, **kwargs)

    return sim.view(qk, n)


################################################
# 根据提供的长度信息，返回一个长度以后的PAD位置的mask
# 掩码。PAD位置会被置位True，其余位置被置于False
################################################
def getMaskFromLens(lens, max_seq_len=200, expand_feature_dim=None):
    if type(lens) == list:
        lens = t.LongTensor(lens)

    # max_idx = max(lens)
    batch_size = len(lens)
    idx_matrix = t.arange(0, max_seq_len, 1).repeat((batch_size, 1))
    len_mask = lens.unsqueeze(1)
    mask = idx_matrix.ge(len_mask).cuda()

    if expand_feature_dim is not None:
        mask = mask.unsqueeze(-1).repeat_interleave(expand_feature_dim,dim=-1)

    return mask


################################################
# 输入一个PackedSequence，将其unpack，并根据lens信息
# 将PAD位置遮盖，并将有效位置取平均
################################################
def unpackAndMean(x):
    x, lens = t.nn.utils.rnn.pad_packed_sequence(x, batch_first=True)
    dim = x.size(2)
    bool_mask = getMaskFromLens(lens).unsqueeze(2).repeat(1,1,dim)
    # 使用0将padding部分的向量利用相乘掩码掉
    val_mask = t.ones_like(x).cuda().masked_fill_(bool_mask, value=0)
    lens_div_term = lens.unsqueeze(1).repeat(1,dim).cuda()
    # 最后让原向量与掩码值向量相乘抹去padding部分，相加后除以有效长度
    # 获得有效长度部分的平均值
    x = (x*val_mask).sum(dim=1) / lens_div_term
    return x


def avgOverHiddenStates(hs, lens):
    # hs shape: [batch, seq, dim]
    # lens shape: [batch]
    dim = hs.size(2)
    lens = lens.unsqueeze(1).repeat(1,dim).cuda()
    hs = hs.sum(dim=1) / lens

    return hs

##################################################
# 动态路由算法，使用该算法来获取类原型。
# arg:
#       transformer: 转换矩阵
#       e: 嵌入向量
#       b: 路由得分
#       k: k-shot的k
##################################################
def dynamicRouting(transformer, e, b, k):
    dim = e.size(2)
    # 先利用转换矩阵转换特征
    # e shape: [n,k,d]
    e = transformer(e)
    # d shape: [n,k]->[n,k,d]
    # b shape: [n,k]
    d = t.softmax(b, dim=1).unsqueeze(dim=2).repeat((1, 1, dim))

    # c shape: [n,k,d]->[n,d]
    c = (d * e).sum(dim=1)
    c_norm = c.norm(dim=1)

    # squashing
    coef = ((c_norm ** 2) / (c_norm ** 2 + 1) / c_norm).unsqueeze(dim=1).repeat((1, dim))
    c = c * coef

    # 更新b
    # [n,d]->[n,k,d]
    c_expand = c.unsqueeze(dim=1).repeat((1, k, 1))
    delta_b = (c_expand * e).sum(dim=2)

    return b + delta_b, c

def splitMetaBatch(meta_data, meta_label,
                   batch_num, max_sample_num, sample_num,
                   meta_len=None):

    assert len(meta_data)==len(meta_label)==len(meta_len)

    index_pool = [i for i in range(len(meta_data))]
    meta_len = t.LongTensor(meta_len)

    for i in range(batch_num):

        # for each meta-mini-batch, sample certain items per class
        index = []

        for start_i in range(0,len(meta_data),max_sample_num):
            rd.seed(magicSeed())
            class_batch_index = rd.sample(index_pool[start_i:start_i+max_sample_num],
                                          sample_num)
            index += class_batch_index

        # print(index)

        if meta_len is not None:
            yield meta_data[index], meta_label[index], meta_len[index].tolist()
        else:
            yield meta_data[index], meta_label[index]


##################################################
# 从参数字典中虎丘列表形式的参数，用于torch.autograd.grad
# 等需要参数列表的场合
##################################################
def collectParamsFromStateDict(par_dict):
    pars = []
    for n,p in par_dict.items():
        pars.append(p)
    return pars




