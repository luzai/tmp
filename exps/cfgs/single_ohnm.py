import sys

sys.path.insert(0, '/data1/xinglu/prj/luzai-tool')
sys.path.insert(0, '/data1/xinglu/prj/open-reid')

from lz import *

cfgs = [
    # edict(
    #     logs_dir='msmt17.res.long',
    #     arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
    #     dataset='msmt17', dataset_val='msmt17', eval_conf='market1501',
    # dataset='msmt17', dataset_val='msmt17', eval_conf='market1501',
    # dataset='market1501', dataset_val='market1501', eval_conf='market1501',
    # dataset='mars', dataset_val='mars', eval_conf='market1501',
    #     lr=3e-4, margin=0.5, area=(0.85, 1),
    #     batch_size=128, num_instances=4, gpu=(0,), num_classes=128,
    #     steps=[80, 120], epochs=125,
    #     workers=8,
    #     dropout=0, loss='tri',
    #     cls_weight=0, tri_weight=1,
    #     random_ratio=1, fusion=None,
    #     log_at=[124, 125],
    #     evaluate=True,
    #     resume='/data1/xinglu/prj/open-reid/exps/work/msmt17.res.2/model_best.pth'
    # ),

    edict(
        logs_dir='cuhk03label.center.mining',
        arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
        dataset='cuhk03', dataset_val='cuhk03', eval_conf='cuhk03',
        lr=3e-4, margin=0.5, area=(0.85, 1),
        batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
        steps=[40, 60], epochs=65,
        workers=8,
        dataset_mode='label',
        dropout=0, loss='tri_center',
        cls_weight=0, tri_weight=1,
        random_ratio=1, fusion=None, lr_cent=1e3, weight_cent=5e-4
    ),
    # edict(
    #     logs_dir='cuhk03label.xent.bs32',
    #     arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
    #     dataset='cuhk03', dataset_val='cuhk03', eval_conf='cuhk03',
    #     lr=3e-4, margin=0.5, area=(0.85, 1),
    #     batch_size=32, num_instances=4, gpu=range(1), num_classes=128,
    #     steps=[40, 60], epochs=65,
    #     workers=8,
    #     dataset_mode='label', xent_smooth=False,
    #     dropout=0, loss='xent',
    #     cls_weight=0, tri_weight=1,
    #     random_ratio=1, fusion=None,
    # ),

    # edict(
    #     logs_dir='cuhk03label.xent.smooth',
    #     arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
    #     dataset='cuhk03', dataset_val='cuhk03', eval_conf='cuhk03',
    #     lr=3e-4, margin=0.5, area=(0.85, 1),
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     steps=[40, 60], epochs=65,
    #     workers=8,
    #     dataset_mode='label', xent_smooth=True,
    #     dropout=0, loss='xent',
    #     cls_weight=0, tri_weight=1,
    #     random_ratio=1, fusion=None,
    # ),

    # edict(
    #     logs_dir='cuhk03label.res.quin',
    #     arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
    #     dataset='cuhk03', dataset_val='cuhk03', eval_conf='cuhk03',
    #     lr=3e-4, margin=0.5, area=(0.85, 1),
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     steps=[40, 60], epochs=65,
    #     workers=8,
    #     dataset_mode='label',
    #     dropout=0, loss='quin',
    #     cls_weight=0, tri_weight=1,
    #     random_ratio=1, fusion=None,
    # ),

    # edict(
    #     logs_dir='cuhk03detect.res',
    #     arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
    #     dataset='cuhk03', dataset_val='cuhk03', eval_conf='cuhk03',
    #     lr=3e-4, margin=0.5, area=(0.85, 1),
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     steps=[40, 60], epochs=65,
    #     workers=8,
    #     dataset_mode='detect',
    #     dropout=0,
    #     cls_weight=0, tri_weight=1,
    #     random_ratio=1, fusion=None,
    #     resume = '/data1/xinglu/prj/open-reid/exps/work.3.8/cuhk03detect.res/model_best.pth', evaluate =True
    # ),

    # edict(
    #     logs_dir='market1501.res.center',
    #     arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
    #     dataset='market1501', dataset_val='market1501', eval_conf='market1501',
    #     lr=3e-4, margin=0.5, area=(0.85, 1),
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     steps=[40, 60], epochs=65,
    #     workers=8, dropout=0,
    #     cls_weight=0, tri_weight=1,
    #     loss='tri_center',
    #     random_ratio=1, fusion=None,
    #     # evaluate=True, resume='/data1/xinglu/prj/open-reid/exps/work.3.8/market1501.res/model_best.pth'
    # ),

    edict(
        logs_dir='market1501.xent.32',
        arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
        dataset='market1501', dataset_val='market1501', eval_conf='market1501',
        lr=3e-4, margin=0.5, area=(0.85, 1),
        batch_size=32, num_instances=4, gpu=range(1), num_classes=128,
        steps=[40, 60], epochs=65,
        workers=8, dropout=0,
        cls_weight=0, tri_weight=1,
        loss='xent',
        random_ratio=1, fusion=None, xent_smooth=False,
        # evaluate=True, resume='/data1/xinglu/prj/open-reid/exps/work.3.8/market1501.res/model_best.pth'
    ),
    #
    # edict(
    #     logs_dir='market1501.xent.smooth',
    #     arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck',
    #     dataset='market1501', dataset_val='market1501', eval_conf='market1501',
    #     lr=3e-4, margin=0.5, area=(0.85, 1),
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     steps=[40, 60], epochs=65,
    #     workers=8, dropout=0,
    #     cls_weight=0, tri_weight=1,
    #     loss='xent',
    #     random_ratio=1, fusion=None, xent_smooth=True,
    #     # evaluate=True, resume='/data1/xinglu/prj/open-reid/exps/work.3.8/market1501.res/model_best.pth'
    # ),
]

# cfgs = [cfgs[-1]]

base = edict(
    weight_cent=5e-4, lr_cent=0.5, xent_smooth=False,
    lr_mult=0.1, fusion=None, eval_conf='cuhk03',
    cls_weight=0., random_ratio=1, tri_weight=1, num_deform=3, cls_pretrain=False,
    bs_steps=[], batch_size_l=[], num_instances_l=[],
    block_name='Bottleneck', block_name2='Bottleneck', convop='nn.Conv2d',
    scale=(1,), translation=(0,), theta=(0,),
    hard_examples=False, has_npy=False, double=0, loss_div_weight=0,
    pretrained=True, dbg=False, data_dir='/home/xinglu/.torch/data',
    restart=True, workers=8, split=0, height=256, width=128,
    combine_trainval=True, num_instances=4,
    # model
    evaluate=False, dropout=0, margin=0.45,
    # optimizer
    lr=3e-4, steps=[100, 150, 160], epochs=165,
    log_at=np.concatenate([
        range(0, 640, 21),
    ]),
    weight_decay=5e-4, resume=None, start_save=0,
    seed=1, print_freq=3, dist_metric='euclidean',
    branchs=0, branch_dim=64, global_dim=1024, num_classes=128,
    loss='tri', mode='hard',
    gpu=[0, ], pin_mem=True, log_start=False, log_middle=True,
    # tuning
    dataset='market1501', dataset_mode='combine', area=(0.85, 1), dataset_val='market1501',
    batch_size=128, logs_dir='', arch='resnet50', embed="concat",
    optimizer='adam', normalize=True, decay=0.1,
)

for k, v in enumerate(cfgs):
    v = dict_update(base, v)
    cfgs[k] = edict(v)


def format_cfg(cfg):
    if cfg.gpu is not None:
        cfg.pin_mem = True
        cfg.workers = len(cfg.gpu) * 8
    else:
        cfg.pin_mem = False
        cfg.workers = 4


def is_all_same(lst):
    return (np.asarray(lst) == lst[0]).all()


import tabulate

if __name__ == '__main__':
    df = pd.DataFrame(cfgs)
    print()

    res = []
    for j in range(df.shape[1]):
        if not is_all_same(df.iloc[:, j].tolist()): res.append(j)
    res = [df.columns[r] for r in res]
    df1 = df[res]
    df1.index = df1.logs_dir
    del df1['logs_dir']
    print(tabulate.tabulate(df1, headers="keys", tablefmt="pipe"))
