import sys

sys.path.insert(0, '/data1/xinglu/prj/open-reid')

from lz import *

cfgs = [
    # edict(
    #     logs_dir='cu03det.cent.eval',
    #     dataset='cu03det', optimizer='adam', lr=3e-4,
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     dropout=0, loss='tri_center', mode='cent',
    #     cls_weight=0, tri_weight=1,
    #     random_ratio=1, weight_dis_cent=0, lr_cent=5e-1, weight_cent=1e-3, gpu_range=range(4),
    #     push_scale=1.,
    #     evaluate=True,
    #     resume='/data2/xinglu/work/reid/work/cu03det.cent/model_best.pth',
    # ),
    #
    # edict(
    #     logs_dir='cu03det.xent.eval',
    #     dataset='cu03det', optimizer='adam', lr=3e-4,
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     dropout=0, loss='tri_xent', xent_smooth=True, gpu_range=range(4),
    #     cls_weight=1, tri_weight=0, lr_mult=10,
    #     evaluate=True,
    #     resume='/data2/xinglu/work/reid/work/cu03det.xent/model_best.pth',
    # ),
    # edict(
    #     logs_dir='xent_cu01_search.improve',
    #     dataset='cuhk01',
    #     lr=3e-4, margin=0.5, area=(0.85, 1), adam_betas=(.9, .999), adam_eps=1e-8,
    #     steps=[40, 60], epochs=65,
    #     arch='resnet50', weight_decay=5e-4,
    #     log_at=np.arange(0, 185, 30),
    #     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    #     dropout=0, loss='tri_xent', mode='ccent.all.all',
    #     cls_weight=1, tri_weight=0,
    #     random_ratio=1, weight_dis_cent=0, lr_cent=0, weight_cent=0, gpu_range=(0, 1, 3),
    #     push_scale=1., xent_smooth=True, lr_mult =10.,
    #     # evaluate=True,
    # )

]

# cfg = edict(
#     logs_dir='tri_cu01_search.easy',
#     dataset='cuhk01',
#     lr=3e-4, margin=0.5, area=(0.85, 1), adam_betas=(.9, .999), adam_eps=1e-8,
#     steps=[40, 60], epochs=65,
#     arch='resnet50', weight_decay=5e-4,
#     log_at=[0, 30, 64, 65, 66],
#     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
#     dropout=0, loss='tri_center', mode='ccent.all.all',
#     cls_weight=0, tri_weight=1,
#     random_ratio=1, weight_dis_cent=0, lr_cent=0, weight_cent=0, gpu_range=(0, 1, 3),
#     push_scale=1., dataset_mode = 'easy'
#     # evaluate=True,
# )

# for lr, margin, adam_eps, batch_size in cross_iter(
#         [3e-4, 1e-4, 1e-3, 6e-4],
#         [.5, .3, ],
#         [1e-8, 1, .1, 1e-4],
#         [128, 32],
# ):
#     cfg_t = copy.deepcopy(cfg)
#     cfg_t.lr = lr
#     cfg_t.margin = margin
#     cfg_t.adam_eps = adam_eps
#     cfg_t.batch_size = batch_size
#     cfg_t.logs_dir = f'{cfg.logs_dir}.{lr:.0e}.{margin}.{adam_eps:.0e}.{batch_size}'
#     cfgs.append(cfg_t)

cfg = edict(
    logs_dir='final.tri',
    dataset='dukemtmc',
    log_at=[0, 30, 64, 65, 66],
    batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    dropout=0, loss='tri_center', mode='ccent.all.all',
    cls_weight=0, tri_weight=1,
    random_ratio=1, weight_dis_cent=0, lr_cent=0, weight_cent=0, gpu_range=(0, 1,),
    push_scale=1., embed=None
)
# cfgs.append(cfg)
for (dataset,
     weight_cent,
     dop,
     dis,
     scale,
     mode) in grid_iter(
    # ['cu01easy', 'cu01hard'],
    ['cu03lbl', 'cu03det', 'mkt', 'dukemtmc'],
    [0, ],  # weight_cent
    [1, ],  # dop
    [0, ],  # dis
    [1, ],  # scale
    ['ccent.all.all'],  # cent_mode
):
    cfg_t = copy.deepcopy(cfg)
    cfg_t.weight_cent = weight_cent
    cfg_t.random_ratio = dop
    cfg_t.dataset = dataset
    cfg_t.weight_dis_cent = dis
    cfg_t.push_scale = scale
    cfg_t.mode = mode
    cfg_t.logs_dir = f'{cfg.logs_dir}.{dataset}'
    cfgs.append(cfg_t)

cfg = edict(
    logs_dir='final.xent',
    dataset='dukemtmc',
    log_at=[0, 30, 64, 65, 66],
    batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
    dropout=0, loss='tri_xent', mode='ccent.all.all',
    cls_weight=1, tri_weight=0,
    random_ratio=1, weight_dis_cent=0, lr_cent=0, weight_cent=0, gpu_range=(3,),
    push_scale=1., embed=None
)
# cfgs.append(cfg)
for (dataset,
     weight_cent,
     dop,
     dis,
     scale,
     mode, smooth) in grid_iter(
    # ['cu01easy', 'cu01hard'],
    ['cu03lbl', 'cu03det', 'mkt', 'dukemtmc'],
    [0, ],  # weight_cent
    [1, ],  # dop
    [0, ],  # dis
    [1, ],  # scale
    ['ccent.all.all'],  # cent_mode
    [True, False]
):
    cfg_t = copy.deepcopy(cfg)
    cfg_t.weight_cent = weight_cent
    cfg_t.random_ratio = dop
    cfg_t.dataset = dataset
    cfg_t.weight_dis_cent = dis
    cfg_t.push_scale = scale
    cfg_t.mode = mode
    cfg_t.xent_smooth = smooth
    cfg_t.logs_dir = f'{cfg.logs_dir}.{dataset}.smth{smooth}'
    cfgs.append(cfg_t)

# cfg = edict(
#     logs_dir='multis',
#     dataset='dukemtmc',
#     batch_size=128, num_instances=4, gpu=range(1), num_classes=128,
#     dropout=0, loss='tri_center',
#     cls_weight=0, tri_weight=1, lr_cent=0, weight_cent=0, gpu_range=range(4),
#     random_ratio=1, weight_dis_cent=0,
#     embed=None,
#     # block_name='SEBottleneck', block_name2='SEBottleneck',
#     block_name='Bottleneck', block_name2='Bottleneck',
#     log_at=[0, 30, 64, 65, 66],
#     # evaluate=True,
#     # resume='/data1/xinglu/prj/open-reid/exps/work/multis.cu03lbl.Bottleneck.None',
# )
# cfgs.append(cfg)
# for dataset, embed, bn in grid_iter(
#         ['cu03det', 'market1501', 'cu03lbl'],
#         [None, 'concat'],
#         ['SEBottleneck', 'Bottleneck'],
# ):
#     cfg_t = copy.deepcopy(cfg)
#     if embed == 'concat' and bn == 'Bottleneck':
#         continue
#     cfg_t.dataset = dataset
#     cfg_t.embed = embed
#     cfg_t.block_name = bn
#     cfg_t.block_name2 = bn
#     if embed == 'concat':
#         # for dp in [.5, ]:
#         # cfg_t = copy.deepcopy(cfg_t)
#         cfg_t.dropout = .5
#         cfg_t.logs_dir = f'{cfg.logs_dir}.{dataset}.{bn}.{embed}'
#         cfgs.append(cfg_t)
#     else:
#         cfg_t.logs_dir = f'{cfg.logs_dir}.{dataset}.{bn}.{embed}'
#         cfgs.append(cfg_t)

base = edict(
    weight_lda=None, test_best=True, push_scale=1.,
    lr=3e-4, margin=0.5, area=(0.85, 1), margin2=0.4, margin3=1.3,
    steps=[40, 60], epochs=65,
    arch='resnet50', block_name='Bottleneck', block_name2='Bottleneck', convop='nn.Conv2d',
    weight_dis_cent=0,
    weight_cent=0, lr_cent=0.5, xent_smooth=False,
    adam_betas=(.9, .999), adam_eps=1e-8,
    lr_mult=1., fusion=None, eval_conf='market1501',
    cls_weight=0., random_ratio=1, tri_weight=1, num_deform=3, cls_pretrain=False,
    bs_steps=[], batch_size_l=[], num_instances_l=[],
    scale=(1,), translation=(0,), theta=(0,),
    hard_examples=False, has_npy=False, double=0, loss_div_weight=0,
    pretrained=True, dbg=False, data_dir='/home/xinglu/.torch/data',
    restart=True, workers=8, split=0, height=256, width=128,
    combine_trainval=True, num_instances=4,
    evaluate=False, dropout=0,
    # log_at=np.concatenate([
    #     range(0, 640, 21),
    # ]),
    log_at=[],
    weight_decay=5e-4, resume=None, start_save=0,
    seed=None, print_freq=3, dist_metric='euclidean',
    branchs=0, branch_dim=64, global_dim=1024, num_classes=128,
    loss='tri',
    # tri_mode = 'hard', cent_mode = 'ccent.all.all',
    mode='ccent.all.all',
    gpu=(0,), pin_mem=True, log_start=False, log_middle=True, gpu_range=range(4),
    # tuning
    dataset='market1501', dataset_mode='combine', dataset_val='market1501',
    batch_size=128, logs_dir='', embed=None,
    optimizer='adam', normalize=True, decay=0.1,
)

for ind, v in enumerate(cfgs):
    v = dict_update(base, v)
    cfgs[ind] = edict(v)

for ind, args in enumerate(cfgs):
    if args.dataset == 'cu03det':
        args.dataset = 'cuhk03'
        args.dataset_val = 'cuhk03'
        args.dataset_mode = 'detect'
        args.eval_conf = 'cuhk03'
    elif args.dataset == 'cu03lbl':
        args.dataset = 'cuhk03'
        args.dataset_val = 'cuhk03'
        args.dataset_mode = 'label'
        args.eval_conf = 'cuhk03'
    elif args.dataset == 'mkt' or args.dataset == 'market' or args.dataset == 'market1501':
        args.dataset = 'market1501'
        args.dataset_val = 'market1501'
        args.eval_conf = 'market1501'
    elif args.dataset == 'msmt':
        args.dataset = 'msmt17'
        args.dataset_val = 'market1501'
        args.eval_conf = 'market1501'
    elif args.dataset == 'cdm':
        args.dataset = 'cdm'
        args.dataset_val = 'market1501'
        args.eval_conf = 'market1501'
    elif args.dataset == 'viper':
        args.dataset = 'viper'
        args.dataset_val = 'viper'
        args.eval_conf = 'market1501'
    elif args.dataset == 'cu01hard':
        args.dataset = 'cuhk01'
        args.dataset_val = 'cuhk01'
        args.eval_conf = 'cuhk03'
        args.dataset_mode = 'hard'
    elif args.dataset == 'cu01easy':
        args.dataset = 'cuhk01'
        args.dataset_val = 'cuhk01'
        args.eval_conf = 'cuhk03'
        args.dataset_mode = 'easy'
    elif args.dataset == 'dukemtmc':
        args.dataset = 'dukemtmc'
        args.dataset_val = 'dukemtmc'
        args.eval_conf = 'market1501'
    else:
        raise ValueError(f'dataset ... {args.dataset}')

    cfgs[ind] = edict(args)

for ind, args in enumerate(cfgs):
    if args.evaluate is True and osp.exists(args.resume + '/conf.pkl'):
        resume = args.resume
        logs_dir = args.logs_dir
        args_ori = pickle_load(args.resume + '/conf.pkl')
        args = dict_update(args, args_ori)
        args = edict(args)
        args.resume = resume + '/model_best.pth'
        args.evaluate = True
        args.logs_dir = logs_dir + '.eval'
        args.gpu_range = range(4)
        cfgs[ind] = args


def format_cfg(cfg):
    if cfg.gpu is not None:
        cfg.pin_mem = True
        cfg.workers = len(cfg.gpu) * 8
    else:
        cfg.pin_mem = False
        cfg.workers = 4


def is_all_same(lst):
    res = [lsti == lst[0] for lsti in lst]
    try:
        return np.asarray(res).all()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    import tabulate

    df = pd.DataFrame(cfgs)
    if len(cfgs) == 1:
        print(df)
        exit(0)
    res = []
    for j in range(df.shape[1]):
        if not is_all_same(df.iloc[:, j].tolist()): res.append(j)
    res = [df.columns[r] for r in res]
    df1 = df[res]
    df1.index = df1.logs_dir
    del df1['logs_dir']
    print(tabulate.tabulate(df1, headers="keys", tablefmt="pipe"))
