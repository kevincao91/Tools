CATEGORIES = [
        "__background",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic_light",
        "fire_hydrant",
        "stop_sign",
        "parking_meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports_ball",
        "kite",
        "baseball_bat",
        "baseball_glove",
        "skateboard",
        "surfboard",
        "tennis_racket",
        "bottle",
        "wine_glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot_dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted_plant",
        "bed",
        "dining_table",
        "toilet",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell_phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy_bear",
        "hair_drier",
        "toothbrush",
    ]
labelmap={}
# for i in range(len(CATEGORIES)):
#   labelmap['{}'.format(i)]=CATEGORIES[i]
for i in range(len(CATEGORIES)):
    labelmap[i]=CATEGORIES[i]
labelmap_car={1:'car',}
labelmap_eRoom={1:'blue',2:'yellow',3:'other',4:'red',5:'ebox_close',6:'ebox_open'}
labelmap_checkout={1:'blue',2:'yellow',3:'other',4:'hand',5:'phone',6:'scanner',7:'pos_free',8:'pos_use',9:'bill',10:'card'}
labelmap_eRoom={1:'blue',2:'yellow',3:'other',4:'red',5:'ebox_close',6:'ebox_open'}
labelmap_isle={1:'blue',2:'yellow',3:'other',4:'red',5:'car',6:'truck',7:'bus',8:'motorcycle',9:'oilgun',10:'cover'}
labelmap_gate={1:'blue',2:'yellow',3:'other'}
labelmap_guide={1:'blue',2:'yellow',3:'other',4:'red',5:'car',6:'truck',7:'bus',8:'motorcycle',9:'oilgun',10:'neat',11:'mess'}
labelmap_safe={1:'blue',2:'yellow',3:'other',4:'security',5:'safe_close',6:'safe_hide',7:'safe_open',8:'door_close',9:'door_open',10:'cashbox_close',11:'cashbox_open'}
labelmap_unload={1:'blue',2:'yellow',3:'other',4:'red',5:'tank_open',6:'tank_close',7:'pipe_on',8:'clamp_on',9:'jug',10:'outfire',11:'tanker',12:'hole',13:'tube',14:'gray',15:'vehicle'}
#model_Detectron
model_checkout='/DATACENTER4/hao.yang/project/Qin/model/checkout/0706/checkout_0706.pkl'
model_eRoom='/DATACENTER4/hao.yang/project/Qin/model/eRoom/0701/eRoom_0701.pkl'
model_gate='/DATACENTER4/hao.yang/project/Qin/model/gate/0629/gate_0629.pkl'
model_guide='/DATACENTER4/hao.yang/project/Qin/model/guide/0624/guide_0624.pkl'
model_isle='/DATACENTER4/hao.yang/project/Qin/model/isle/0706/isle_0706.pkl'
model_safe='/DATACENTER4/hao.yang/project/Qin/model/safe/0705/safe_0705.pkl'
#model_safe='/DATACENTER4/hao.yang/project/Qin/backup/model_dt_p/safe_baselineQ_total_0529.pkl'
model_unload='/DATACENTER4/hao.yang/project/Qin/model/unload/0707/unload_0707.pkl'
# model_unload='/DATACENTER4/hao.yang/project/Qin/model/guide/test/retina.pkl'
#model_mb
model_checkout_mb='/DATACENTER4/hao.yang/project/Qin/model_mb/checkout/0605/checkout_0605_max.pth'
model_gate_mb='/disk2/hao.yang/project/Qin/model/gate/0527/gate_baselineQ_total.pkl'
model_guide_mb='/DATACENTER4/hao.yang/project/Qin/model_mb/guide/0606/guide_0606_balance.pth'
model_isle_mb='/DATACENTER4/hao.yang/project/Qin/model_mb/isle/0605/isle_0605_max.pth'
model_safe_mb='/disk2/hao.yang/project/Qin/model/safe/0528/safe_baselineQ_total_0528.pkl'
model_unload_mb='/DATACENTER4/hao.yang/project/Qin/model_mb/unload/0528/unload_baseline_dif.pth'
# model_eRoom=''
# for removeSimilarLabels.py
weight_checkout={'blue':3,'yellow':1,'other':1,'hand':0.2,'phone':1,'scanner':5,'pos_free':1,'pos_use':3,'bill':2,'card':2}
weight_eRoom={'blue':3,'yellow':1,'other':2,'red':2,'ebox_close':1,'ebox_open':2}
weight_isle={'blue':3,'yellow':1,'other':2,'red':3,'car':1,'truck':3,'bus':4,'motorcycle':3,'oilgun':1,'cover':50}
weight_gate={'blue':3,'yellow':1,'other':1}
weight_guide={'blue':3,'yellow':1,'other':2,'red':2,'car':1,'truck':3,'bus':6,'motorcycle':4,'oilgun':1,'neat':1,'mess':1}
weight_safe={'blue':3,'yellow':1,'other':1,'security':6,'safe_close':1,'safe_hide':4,'safe_open':3,'door_close':1,'door_open':2,'cashbox_close':1,'cashbox_open':4}
weight_unload={'blue':3,'yellow':1,'other':3,'red':3,'tank_open':1,'tank_close':2,'pipe_on':1,'clamp_on':1,'jug':1,'outfire':1,
'tanker':1,'hole':2,'tube':0,'gray':3,'vehicle':3}
areaNames=['blue','yellow','red','gray','security','other','car','vehicle']
thresh_checkout=3
thresh_eRoom=0.5
thresh_isle=20
thresh_gate=3
thresh_guide=20
thresh_safe=3
thresh_unload=2
# ebox_coordinate
#zhuhong
ebox_coordinate=(767,250,1280,720)
ebox_coordinate_thresh=0.8
# labelTask_hideNames
hideNames_unload=['outfire','pipe_on','tank_close','tank_open','clamp_on','tube','hole']
hideNames_checkout=['bill','card','pos_free','pos_use','scanner']
hideNames_isle=['oilgun','cover']
hideNames_safe=['door_open','door_close','safe_open','safe_close','safe_hide']
hideNames_guide=['oilgun','neat','mess']
# showNames
showNames_isle={'person':['blue','yellow','other','red'],'vehicle':['car','truck','bus','motorcycle'],'still':['oilgun','cover'],'all':None}
showNames_guide={'person':['blue','yellow','other','red'],'vehicle':['car','truck','bus','motorcycle'],'still':['oilgun','neat','mess'],'all':None}
showNames_checkout={'person':['blue','yellow','other'],'hand':['car','truck','bus','motorcycle'],'phone':['phone'],
'still':['bill','card','pos_use','pos_free'],'all':None}
showNames_safe={'person':['blue','yellow','other','security'],'cashbox':['cashbox_close','cashbox_open'],
'safe':['safe_open','safe_hide','safe_close'],'door':['door_close','door_open'],'all':None}
showNames_unload={'person':['blue','yellow','other','red','gray'],'jug':['jug'],'vehicle':['tanker','vehicle'],'tube':['tube'],
'still':['tank_close','tank_open','clamp_on','pipe_on','outfire','hole'],'all':None}
