_base_ = "ssd512_coco.py"


data_root = "data/license-plate-detection-9/"
work_dir = "./model_output/dino/5scale"


metainfo = dict(
    classes=("license-plate",),
    palette=[
        (165, 42, 42),
    ],
)

model = dict(
    bbox_head=dict(
        num_classes=1,
    )
)

train_dataloader = dict(
    batch_size=8,
    num_workers=1,
    dataset=dict(
        dataset=dict(
            data_root=data_root,
            metainfo=metainfo,
            ann_file="train/_annotations.coco.json",
            data_prefix=dict(img="train/"),
        )
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
            "group": "ssd512_2xb8-12e_lp9",
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

auto_scale_lr = dict(base_batch_size=8)
