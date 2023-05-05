import os
import torch
import argparse
from maskrcnn_benchmark.config import cfg
from maskrcnn_benchmark.utils.c2_model_loading import load_c2_format


re_map_dict = {
'features.module.0':'conv1',
'features.module.1':'bn1',
'features.module.4':'layer1',
'features.module.5':'layer2',
'features.module.6':'layer3',
'features.module.7':'layer4',
'features.module.8':'layer_reduce',
'features.module.9':'layer_reduce_bn',
'classifier':'fc',
}
re = [
'features.module.0',
'features.module.1',
'features.module.4',
'features.module.5',
'features.module.6',
'features.module.7',
'features.module.8',
'features.module.9',
'classifier',
]


def removekey(d, listofkeys):
    r = dict(d)
    for key in listofkeys:
        print('key: {} is removed'.format(key))
        r.pop(key)
    return r


parser = argparse.ArgumentParser(description="Trim Detection weights and save in PyTorch format.")
parser.add_argument(
    "--pretrained_path",
    default="/media/kevin/备份/weather/fast-MPN-COV/Results/Finetune-ImageNet-v2_mpncovresnet101-MPNCOV-256_ObjectCategories-01-lr1.0e-3-bs64/model_best.pth.tar",
    #default="/media/kevin/备份/weather/fast-MPN-COV/pretrainData/mpncovresnet101-ade9737a.pth",
    help="path to detectron pretrained weight(.pkl)",
    type=str,
)
parser.add_argument(
    "--save_path",
    default="/media/kevin/备份/weather/fast-MPN-COV/pretrainData/v2_mpncovresnet101-256_no_last_layers.pth",
    help="path to save the converted model",
    type=str,
)
parser.add_argument(
    "--cfg",
    default="configs.yaml",
    help="path to config file",
    type=str,
)

args = parser.parse_args()
#
DETECTRON_PATH = os.path.expanduser(args.pretrained_path)
print('detectron path: {}'.format(DETECTRON_PATH))

_d = torch.load(args.pretrained_path)
d = _d['state_dict']

print('== old key ================')
for key in d:
    print(key)

newdict={}
for key in d:
    if key.startswith(re[0]):
        new_key=key.replace(re[0], re_map_dict[re[0]])
        newdict[new_key] = d[key]
    elif key.startswith(re[1]):
        new_key=key.replace(re[1], re_map_dict[re[1]])
        newdict[new_key] = d[key]
    elif key.startswith(re[2]):
        new_key=key.replace(re[2], re_map_dict[re[2]])
        newdict[new_key] = d[key]
    elif key.startswith(re[3]):
        new_key=key.replace(re[3], re_map_dict[re[3]])
        newdict[new_key] = d[key]
    elif key.startswith(re[4]):
        new_key=key.replace(re[4], re_map_dict[re[4]])
        newdict[new_key] = d[key]
    elif key.startswith(re[5]):
        new_key=key.replace(re[5], re_map_dict[re[5]])
        newdict[new_key] = d[key]
    elif key.startswith(re[6]):
        new_key=key.replace(re[6], re_map_dict[re[6]])
        newdict[new_key] = d[key]
    elif key.startswith(re[7]):
        new_key=key.replace(re[7], re_map_dict[re[7]])
        newdict[new_key] = d[key]
    elif key.startswith(re[8]):
        new_key=key.replace(re[8], re_map_dict[re[8]])
        newdict[new_key] = d[key]
    else:
        print('error!')
        exit()

print('== new key ================')
for key in newdict:
    print(key)
#exit()

newdict = removekey(newdict, ['fc.weight', 'fc.bias'])

torch.save(newdict, args.save_path)
print('saved to {}.'.format(args.save_path))







