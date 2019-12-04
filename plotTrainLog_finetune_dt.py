import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import random
import json
from basicFun import FILES
import sys
def load_data(data_file):
    data = {'iter':[],'lr':[],'loss':[]}
    with open(data_file, 'r') as f:
        for line in f:
            line = line.strip("logging.log_json_stats:")
            jLine=json.loads(line)
            data['iter'].append(int(jLine['iter']))
            data['lr'].append(float(jLine['lr']))
            data['loss'].append(float(jLine['loss']))
    return data
if __name__=="__main__":
    data_file=sys.argv[1]
    print(data_file)
    data = load_data(data_file)
    linewidth = 0.75
    pallet={'lr':(0,1,0),'loss':(0,0,1)}
    fig,left_axis=plt.subplots()
    right_axis = left_axis.twinx()
    left_axis.set_xlabel('iters')
    left_axis.set_ylabel('lr')
    left_axis.set_ylim(min(data['lr']),1.1*max(data['lr']))
    # right_axis.set_ylim(min(data['loss']),10*min(data['loss']))
    right_axis.set_ylim(min(data['loss']),max(data['loss']))
    right_axis.set_ylabel('loss')
    ll=left_axis.plot(data['iter'], data['lr'], label = "lr", color = pallet['lr'],linewidth = linewidth)
    rl=right_axis.plot(data['iter'], data['loss'], label = "loss", color = pallet['loss'],linewidth = linewidth)    
    lns=ll+rl
    labs = [l.get_label() for l in lns]
    right_axis.legend(lns, labs, loc=5)
    # plt.show()
    plt.savefig(data_file.split('.log')[0]+'.png')
