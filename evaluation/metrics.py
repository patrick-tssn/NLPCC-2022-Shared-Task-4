import os, re, json, sys, time, copy, datetime
from typing import Dict

import torch
import torchmetrics

sys.path.append('coco-caption')
from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap

class F1ScoreMetric(torchmetrics.classification.F1):
    def __init__(self, average, num_classes, multiclass, threshold, **metric_args):

        metrics_args = {"average":average, "num_classes":num_classes, "multiclass":multiclass, "threshold":threshold, "compute_on_step": False, "dist_sync_on_step": True}

        super().__init__(**metrics_args)

class SegMetric(torchmetrics.classification.Accuracy):
    """
    ref:
        - https://github.com/PyTorchLightning/metrics/blob/master/torchmetrics/classification/accuracy.py
        - https://github.com/PyTorchLightning/metrics/blob/f61317ca17e3facc16e09c0e6cef0680961fc4ff/torchmetrics/functional/classification/accuracy.py#L72
    """

    def __init__(self, **metric_args):

        metrics_args = {"compute_on_step": False, "dist_sync_on_step": True}

        super().__init__(**metrics_args)

        self.eps = 1e-5
        self.threshold = 0.5
        self.add_state("tp", default=torch.tensor(0), dist_reduce_fx="sum")
        self.add_state("fp", default=torch.tensor(0), dist_reduce_fx="sum")
        self.add_state("tn", default=torch.tensor(0), dist_reduce_fx="sum")
        self.add_state("fn", default=torch.tensor(0), dist_reduce_fx="sum")

    def update(self, pred, labels):

        assert isinstance(pred, torch.LongTensor) or isinstance(
            pred, torch.cuda.LongTensor
        )
        assert isinstance(labels, torch.LongTensor) or isinstance(
            labels, torch.cuda.LongTensor
        )

        gt_one = labels == 1
        gt_zero = labels == 0
        pred_one = pred == 1
        pred_zero = pred == 0

        self.tp += (gt_one * pred_one).sum()
        self.fp += (gt_zero * pred_one).sum()
        self.tn += (gt_zero * pred_zero).sum()
        self.fn += (gt_one * pred_zero).sum()

    def compute(self) -> Dict[str, torch.Tensor]:
        # compute final result
        tp = self.tp
        fp = self.fp
        tn = self.tn
        fn = self.fn

        assert (tp + fn) > 0
        assert (fp + tn) > 0

        output = {}
        output["acc1"] = 100.0 * tp / (tp + fn)
        output["acc0"] = 100.0 * tn / (fp + tn)
        output["acc"] = 100.0 * (tp + tn) / (tp + fn + fp + tn)
        output["prec"] = 100.0 * tp / (tp + fn)
        output["rec"] = 100.0 * tp / (tp + fp)
        output["f1"] = (2 * output["prec"] * output["rec"]) / (output["prec"] + output["rec"])

        return output

def eval_gen(hyps, exp_id, ref_path):
    annos = []
    img_id = 1
    for hyp in hyps.values():
        annos.append({'image_id':img_id, 'caption':hyp})
        img_id += 1
    hyp_fn = exp_id.replace('.json', '_tmp.json')
    with open(hyp_fn, 'w') as jh:
        json.dump(annos, jh, indent=4)
    coco = COCO(ref_path)
    cocoRes = coco.loadRes(hyp_fn)
    cocoEval = COCOEvalCap(coco, cocoRes)
    cocoEval.params['image_id'] = cocoRes.getImgIds()
    cocoEval.evaluate()
    os.remove(hyp_fn)
    return cocoEval.eval.items()
    






