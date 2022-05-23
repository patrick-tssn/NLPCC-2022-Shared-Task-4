import os, re, json, torch
from metrics import SegMetric, eval_gen

""" 
input type:
{"vid": answer, ...}
metrics:
segmentation: acc. f1.
generation: bleu, rouge, meteor, cider
"""
def eval_task1(eval_path, ref_path):
    with open(ref_path) as jh:
        scene_ref = json.load(jh)['scene']
    with open(eval_path) as jh:
        scene_pred = json.load(jh)
    seg_metric = SegMetric()
    for vid, scene in scene_ref.items():
        seg_metric.update(torch.Tensor(scene_pred[vid]).long()[:len(scene)], torch.Tensor(scene).long())
    output = seg_metric.compute()    
    acc, f1 = output['acc'], output['f1']
    print("acc:{} f1:{}".format(acc, f1))

def eval_task2(eval_path, ref_path):
    with open(ref_path) as jh:
        session_ref = json.load(jh)['session']
    with open(eval_path) as jh:
        session_pred = json.load(jh)
    seg_metric = SegMetric()
    for vid, session in session_ref.items():
        seg_metric.update(torch.Tensor(session_pred[vid]).long()[:len(session)], torch.Tensor(session).long())
    output = seg_metric.compute()    
    acc, f1 = output['acc'], output['f1']
    print("acc:{} f1:{}".format(acc, f1))

def eval_task3(eval_path, ref_path):
    with open(eval_path) as jh:
        gen_hyp = json.load(jh)
    res_gen = eval_gen(gen_hyp, eval_path, ref_path)
    for metric, score in res_gen:
        print('%s: %.3f'%(metric, score))

if __name__ == '__main__':
    # you will replace the file name with yours
    eval_task1('hyps/Random_track1.json', 'refs/valid_ref_seg.json')
    eval_task2('hyps/Random_track2.json', 'refs/valid_ref_seg.json')
    eval_task3('hyps/Random_track3.json', 'refs/valid_ref_gen.json')
    