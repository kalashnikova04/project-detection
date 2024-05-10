_base_ = './dino-4scale_r50_8xb2-12e_coco.py'

data_root = 'data/license-plate-detection-9/'

metainfo = dict(
    classes=('license-plate',),
    palette=[
        (165, 42, 42),
    ]
)

model=dict(
    bbox_head=dict(
        num_classes=1
    ),
    # train_cfg=dict(
    #     assigner=dict(
    #         type='HungarianAssigner',
    #         match_costs=[
    #             dict(type='FocalLossCost', weight=2.0),
    #             dict(type='BBoxL1Cost', weight=5.0, box_format='xywh'),
    #             dict(type='IoUCost', iou_mode='giou', weight=2.0)
    #         ]))
)

work_dir = './model_output/dino'

load_from = 'https://download.openmmlab.com/mmdetection/v3.0/dino/dino-4scale_r50_8xb2-12e_coco/dino-4scale_r50_8xb2-12e_coco_20221202_182705-55b2bba2.pth'

optim_wrapper = dict(
    optimizer=dict(
        lr=0.0001,
        weight_decay=0.0001
        )
    )


train_dataloader = dict(
    # batch_size=8,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='train/_annotations.coco.json',
        data_prefix=dict(img='train/'),
    )
)

val_dataloader = dict(
    batch_size=8,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='valid/_annotations.coco.json',
        data_prefix=dict(img='valid/'),
    )
)

test_dataloader = dict(
    batch_size=8,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='test/_annotations.coco.json',
        data_prefix=dict(img='test/'),
    )
)


vis_backends = [dict(type='WandbVisBackend',
                     init_kwargs={
                         'project': 'license-plate-detection',
                         'group': 'dino-4scale_r50_1xb2-12e_lp',
                         'name': 'exp-24-05-08-1-lp9'
                     },
)]

visualizer = dict(
    type='DetLocalVisualizer', vis_backends=vis_backends, name='visualizer')

val_evaluator = dict(
    type='CocoMetric',
    ann_file = data_root + 'valid/_annotations.coco.json',
    metric=['bbox'],
    format_only=False
)

test_evaluator = dict(
    ann_file = data_root + 'test/_annotations.coco.json',
    format_only=True,
    outfile_prefix='./model_output/dino/test'
)

auto_scale_lr = dict(enable=True, base_batch_size=16)
