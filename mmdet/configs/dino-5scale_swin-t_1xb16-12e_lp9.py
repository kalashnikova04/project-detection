_base_ = "./dino-5scale_swin-l_8xb2-12e_coco.py"

data_root = "data/license-plate-detection-9/"

# pretrained = 'https://github.com/SwinTransformer/storage/releases/download/v1.0.8/swin_tiny_patch4_window7_224_22k.pth'
pretrained = "data/swin_tiny_patch4_window7_224_22k.pth"

model = dict(
    backbone=dict(
        pretrain_img_size=224,
        embed_dims=96,
        window_size=7,
        num_heads=[3, 6, 12, 24],
        init_cfg=dict(type="Pretrained", checkpoint=pretrained),
    ),
    neck=dict(in_channels=[96, 192, 384, 768]),
)

metainfo = dict(
    classes=("license-plate",),
    palette=[
        (165, 42, 42),
    ],
)

work_dir = "./model_output/dino/5scale"

train_dataloader = dict(
    batch_size=2,
    num_workers=1,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file="train/_annotations.coco.json",
        data_prefix=dict(img="train/"),
    ),
)

val_dataloader = dict(
    batch_size=1,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file="valid/_annotations.coco.json",
        data_prefix=dict(img="valid/"),
    ),
)

test_dataloader = dict(
    batch_size=1,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file="test/_annotations.coco.json",
        data_prefix=dict(img="test/"),
    ),
)

vis_backends = [
    dict(
        type="WandbVisBackend",
        init_kwargs={
            "project": "license-plate-detection",
            "group": "dino-5scale_swin-t_1xb16-12e_lp9",
            "name": "exp-24-05-16-1-base",
        },
    )
]

visualizer = dict(
    type="DetLocalVisualizer", vis_backends=vis_backends, name="visualizer"
)

val_evaluator = dict(
    type="CocoMetric",
    ann_file=data_root + "valid/_annotations.coco.json",
    metric=["bbox"],
    format_only=False,
)

test_evaluator = dict(
    ann_file=data_root + "test/_annotations.coco.json",
    format_only=True,
    outfile_prefix="./model_output/dino/5scale/test",
)

default_hooks = dict(
    early_stopping=dict(
        type="EarlyStoppingHook", monitor="coco/bbox_mAP", patience=10, min_delta=0.005
    ),
    checkpoint=dict(
        type="CheckpointHook", interval=5, save_best="auto", out_dir=work_dir
    ),
)

optim_wrapper = dict(
    type="AmpOptimWrapper",
    optimizer=dict(type="SGD", lr=1e-4),
    accumulative_counts=4
    # lr=0.0001,  # 0.0002 for DeformDETR
    # weight_decay=0.0001),
)

auto_scale_lr = dict(enable=True, base_batch_size=2)
