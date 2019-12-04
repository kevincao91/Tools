import torch
pthPath='/DATACENTER4/hao.yang/project/Qin/model_mb/unload/0530/unload_0530.pth'
wgtPath=pthPath
pth=torch.load(pthPath)
cutLayer='module.roi_heads.box.predictor'
cutParas=['cls_score.weight','cls_score.bias','bbox_pred.weight','bbox_pred.bias',]
for cutPara in cutParas:
    pth['model'].pop('{}.{}'.format(cutLayer,cutPara))
# print(pth['model'].keys())
wgt=pth['model']
torch.save(wgt,wgtPath)