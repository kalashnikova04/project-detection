_base_ = './cascade-rcnn_r101-dconv-c3-c5_fpn_1x_coco.py'

data_root = 'data/license-plate-detection-8/'

metainfo = dict(
    classes=('license-plate',),
    palette=[
        (165, 42, 42),
    ]
)

model = dict(
    roi_head = dict(
        bbox_head=[
            dict(
                type='Shared2FCBBoxHead',
                num_classes=1,
                in_channels=256,
                fc_out_channels=1024,
                roi_feat_size=7,
                bbox_coder=dict(
                    type='DeltaXYWHBBoxCoder',
                    target_means=[0., 0., 0., 0.],
                    target_stds=[0.1, 0.1, 0.2, 0.2]),
                reg_class_agnostic=True,
                loss_cls=dict(
                    type='CrossEntropyLoss',
                    use_sigmoid=False,
                    loss_weight=1.0),
                loss_bbox=dict(type='SmoothL1Loss', beta=1.0,
                               loss_weight=1.0)),
            dict(
                type='Shared2FCBBoxHead',
                num_classes=1,
                in_channels=256,
                fc_out_channels=1024,
                roi_feat_size=7,
                bbox_coder=dict(
                    type='DeltaXYWHBBoxCoder',
                    target_means=[0., 0., 0., 0.],
                    target_stds=[0.05, 0.05, 0.1, 0.1]),
                reg_class_agnostic=True,
                loss_cls=dict(
                    type='CrossEntropyLoss',
                    use_sigmoid=False,
                    loss_weight=1.0),
                loss_bbox=dict(type='SmoothL1Loss', beta=1.0,
                               loss_weight=1.0)),
            dict(
                type='Shared2FCBBoxHead',
                num_classes=1,
                in_channels=256,
                fc_out_channels=1024,
                roi_feat_size=7,
                bbox_coder=dict(
                    type='DeltaXYWHBBoxCoder',
                    target_means=[0., 0., 0., 0.],
                    target_stds=[0.033, 0.033, 0.067, 0.067]),
                reg_class_agnostic=True,
                loss_cls=dict(
                    type='CrossEntropyLoss',
                    use_sigmoid=False,
                    loss_weight=1.0),
                loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0))]
    )
)
    
work_dir = './model_output'

albu_train_transforms = [
    dict(type='ShiftScaleRotate', shift_limit=0.0625,
         scale_limit=0.15, rotate_limit=15, p=0.4),
#     dict(type='RandomBrightnessContrast', brightness_limit=0.2,
#          contrast_limit=0.2, p=0.5),
    dict(type='IAAAffine', shear=(-10.0, 10.0), p=0.4),
#     dict(type='MixUp', p=0.2, lambd=0.5),
#     dict(type="Blur", p=1.0, blur_limit=7),
#     dict(type='CLAHE', p=0.5),
#     dict(type='Equalize', mode='cv', p=0.4),
    dict(
        type="OneOf",
        transforms=[
            dict(type="GaussianBlur", p=1.0, blur_limit=7),
            dict(type="MedianBlur", p=1.0, blur_limit=7),
        ],
        p=0.4,
    )
]

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
    dict(type='Resize', img_scale=(1333, 800), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(
        type='Albu',
        transforms=albu_train_transforms,
        bbox_params=dict(
        type='BboxParams',
        format='coco',
        label_fields=['gt_labels'],
        min_visibility=0.0,
        filter_lost_elements=True),
        keymap=dict(img='image', gt_bboxes='bboxes'),
        update_pad_shape=False,
        skip_img_without_anno=True),
    dict(type='PackDetInputs')
]

train_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='train/_annotations.coco.json',
        data_prefix=dict(img='train/'),
    )
)

val_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='valid/_annotations.coco.json',
        data_prefix=dict(img='valid/'),
    )
)

test_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='test/_annotations.coco.json',
        data_prefix=dict(img='test/'),
    )
)

load_from = 'cascade_rcnn_r101_fpn_dconv_c3-c5_1x_coco_20200203-3b2f0594.pth'

optim_wrapper = dict(
    optimizer=dict(
        lr=0.02 / 8
        )
    )

# lr_config = dict(
#     policy='CosineAnnealing', 
#     by_epoch=False,
#     warmup='linear', 
#     warmup_iters=500, 
#     warmup_ratio=0.001,
#     min_lr=1e-07)
# ->
# param_scheduler = [
#     dict(
#         type='LinearLR',  # Use linear learning rate warmup
#         start_factor=0.001, # Coefficient for learning rate warmup
#         by_epoch=False,  # Update the learning rate during warmup at each iteration
#         begin=0,  # Starting from the first iteration
#         end=500),  # End at the 500th iteration
#     dict(
#         type='MultiStepLR',  # Use multi-step learning rate strategy during training
#         by_epoch=True,  # Update the learning rate at each epoch
#         begin=0,   # Starting from the first epoch
#         end=12,  # Ending at the 12th epoch
#         milestones=[8, 11],  # Learning rate decay at which epochs
#         gamma=0.1)  # Learning rate decay coefficient
# ]

vis_backends = [dict(type='WandbVisBackend',
                     init_kwargs={
                         'project': 'license-plate-detection',
                         'group': 'dcn-cascade-rcnn-r101-c3-c5-1x',
                         'name': 'exp-24-05-04-base'
                     },
                    #  define_metric_cfg={
                    #      'val/bbox_mAP_50': '',
                    #      'val/bbox_mAP_75': ,
                    #      'val/bbox_mAP': ,
                    #      'val/bbox_mAP_l': ,
                    #      'val/bbox_mAP_m': ,
                    #      'val/bbox_mAP_s': ,

                    #  }
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
    outfile_prefix='./model_output/test'
)

# seed = 0
# # set_random_seed(0, deterministic=False)
# gpu_ids = [0]


# from mmdet.apis import init_detector, inference_detector

# config_file = 'rtmdet_tiny_8xb32-300e_coco.py'
# checkpoint_file = 'rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth'
# model = init_detector(config_file, checkpoint_file, device='cpu')  # or device='cuda:0'
# inference_detector(model, 'demo/demo.jpg')

# auto_scale_lr = dict(enable=True, base_batch_size=2)