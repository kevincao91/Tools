import pickle
import os,sys
cptPath=sys.argv[1]
wgtPath=cptPath
with open(cptPath,'rb') as f:
    data = pickle.load(f,encoding='latin1')
keys = data['blobs'].keys()
# needs = ['conv','res','fpn',]
not_needs = ['fc1000','momentum']
output_dic={'blobs':{}}
print('filtered out:')
for key in keys:
    keep = True
    # for need in needs:
    #     if key.startswith(need):
    #         keep=True
    for not_need in not_needs:
        if not_need in key:
            keep=False
            break
    if keep:
        # if 'score' in key:
        #     print(key)
        output_dic['blobs'][key] = data['blobs'][key]
        #print(key)
    else:
        print(' - '+key)
#print(output_dic['blobs'].keys())
with open(wgtPath,'wb') as f:
    pickle.dump(output_dic,f,protocol=0)
