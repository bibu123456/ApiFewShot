import sys
import os
import shutil
import logging
import time

sys.path.append('../')

from tqdm import tqdm

from util.file import deleteDir, loadJson, dumpJson
from util.manager import PathManager
###########################################
# 本函数用于将当前项目路径添加到扫描选项中以便可以
# 导入其他模块。可以使用depth参数来调节运行路径相对
# 项目路径的深度，默认为1
###########################################
def appendProjectPath(depth=1):
    pwd = os.getcwd()  # 要正常运行，运行路径必须与本文件相同
    pwd = repr(pwd).replace('\\\\', '/')[1:-1*depth]  # 替换双斜杠
    projectPath = pwd.split('/')
    projectPath = '/'.join(projectPath[:-1])  # 获取项目路径父路径
    sys.path.append(projectPath)  # 添加当前项目路径到包搜索路径中


def saveConfigFile(folder_path, model):
    # 若目前的version已经存在，则删除之
    if os.path.exists(folder_path):
        deleteDir(folder_path)
    os.mkdir(folder_path)
    # 复制运行配置文件
    shutil.copy('./runConfig.json', folder_path + 'config.json')
    # 复制模型代码文件
    shutil.copy(f'../models/{model}.py', folder_path + f'{model}.py')


###########################################################
# 从数据集对应的doc文件夹中读取每一次运行的config和测试结果，整理到一
# 个单独的JSON文件中以便浏览
###########################################################
def generateConfigReport(dataset,
                         include_result=False,
                         dump_path=None):
    mng = PathManager(dataset)

    report = {}
    warnings = []

    for doc_dir in tqdm(os.listdir(mng.DocBase())):
        config_path = mng.DocBase() + doc_dir + '/'

        try:
            cfg = loadJson(config_path + 'config.json')

            report[int(cfg['version'])] = {
                '__model': cfg['modelName'],                # 添加下划线便于排序
                '_k-q-qk': '-'.join([str(cfg['k']),
                                    str(cfg['n']),
                                    str(cfg['qk'])]),
                'desc': cfg['description']
            }

            if include_result:
                res = loadJson(config_path + 'testResult.json')
                report[int(cfg['version'])]['results'] = res['results']

        except Exception as e:
            warnings.append('Error occurred when process %s: %s'%
                            (doc_dir, str(e)))

    for w in warnings:
        logging.warning(w)

    dump_path = mng.DatasetBase()+'summary.json' if dump_path is None else dump_path
    dumpJson(report, dump_path, sort=True)

ver_check_warning_template = '''
\n\nYour current running version is equal to the last running 
version = %d, please check if you would like to override it.
(type 'y', '1' or '' for comfirmation, otherwise to exit)\n\n
'''

#############################################################33
# Check the current running version and the last running
# version and warn users to ensure if deplicated. This prevents
# from unexpected configuration covering.
#############################################################33
def checkVersion(cur_v):
    ver_cfg = loadJson('version.json')
    last_ver = ver_cfg['lastRunVersion']

    if cur_v == last_ver:
        logging.warning(ver_check_warning_template%cur_v)
        opt = input('>>>')

        if opt == 'y' or opt == '1' or opt == '':
            return
        else:
            sys.exit(1)

    else:
        ver_cfg['lastRunVersion'] = cur_v
        dumpJson(ver_cfg, 'version.json')


###########################################################
# 将运行时的配置,如版本,数据集,模型,模型参数,运行时间等保存到文件中
###########################################################
def saveRunVersionConfig(cur_v, dataset, model, cfg):
    cfg_pack = {'__version': cur_v,
                '_model': model,
                '_dataset': dataset,
                'config': cfg,
                '_time': time.asctime()}
    ver_cfg = loadJson('version.json')
    ver_cfg[str(cur_v)] = cfg_pack

    dumpJson(ver_cfg,'version.json',sort=True)

