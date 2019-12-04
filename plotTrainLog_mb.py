import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import random
import json,re
from basicFun import FILES
import sys
def load_data(data_file):
    data = {'iter':(),'loss':(),'loss_box_reg':(),'loss_classifier':(),'lr':()}
    with open(data_file, 'r') as f:
        for line in f:
            # line = line.strip("GeForce")
            if 'iter'in line:
                iterStep=''.join(re.findall(r"iter:(.+?)loss",line))
                iterStep=int(iterStep)
                data['iter']+=(iterStep,)
                loss=''.join(re.findall(r"loss:(.+?)loss_retina_cls",line))
                loss=float(loss.split('(')[0])
                data['loss']+=(loss,)
                # loss_box_reg=''.join(re.findall(r"loss_box_reg:(.+?)loss_classifier",line))
                # loss_box_reg=float(loss_box_reg.split('(')[0])
                # data['loss_box_reg']+=(loss_box_reg,)
                # loss_classifier=''.join(re.findall(r"loss_classifier:(.+?)loss_box_reg",line))
                # loss_classifier=float(loss_classifier.split('(')[0])
                # data['loss_classifier']+=(loss_classifier,)
                lr=''.join(re.findall(r"lr:(.+?)max mem:",line))
                lr=float(lr)
                data['lr']+=(lr,)
            else:
                continue
    return data
if __name__=="__main__":
    data_file=sys.argv[1]
    print(data_file)
    data = load_data(data_file)
    linewidth = 0.75
    pallet={'loss':(0,1,0),'lr':(0,0,1)}
    fig,left_axis=plt.subplots()
    right_axis = left_axis.twinx()
    left_axis.set_xlabel('iters')
    left_axis.set_ylabel('lr')
    left_axis.set_ylim(min(data['lr']),1.1*max(data['lr']))
    # left_axis.set_ylim(min(data['loss_box_reg']),0.15)
    right_axis.set_ylim(min(data['loss']),5*min(data['loss']))
    # left_axis.set_ylim(min(data['loss_box_reg']),max(data['loss_box_reg']))
    # right_axis.set_ylim(min(data['loss_classifier']),max(data['loss_classifier']))
    right_axis.set_ylabel('loss')
    ll=left_axis.plot(data['iter'], data['lr'], label = "lr", color = pallet['lr'],linewidth = linewidth)
    # ll=left_axis.plot(data['iter'], data['loss_box_reg'], label = "loss_box_reg", color = pallet['loss_box_reg'],linewidth = linewidth)
    rl=right_axis.plot(data['iter'], data['loss'], label = "loss", color = pallet['loss'],linewidth = linewidth)    
    lns=ll+rl
    labs = [l.get_label() for l in lns]
    right_axis.legend(lns, labs, loc=5)
    # plt.show()
    plt.savefig(data_file.split('.log')[0]+'.png')
