import random


with open('train_old.txt', 'r') as f:
    lines_train = f.readlines()
    
with open('valid_old.txt', 'r') as f:
    lines_valid = f.readlines()
    
lines_all = lines_train + lines_valid

num_list = len(lines_all)

random.seed(666)
random.shuffle(lines_all)


train_per = 0.5
valid_per = 0.0


print('all files:', num_list)
train_point = int(num_list * train_per)
valid_point = train_point + int(num_list * valid_per)

trainf = open('train.txt', 'w')
trainvalf = open('trainval.txt', 'w')
validf = open('valid.txt', 'w')
testf = open('test.txt', 'w')


for i, line in enumerate(lines_all):

    # print(line)

    if i < train_point:
        trainf.write(line)
        trainvalf.write(line)
    elif i < valid_point:
        validf.write(line)
        trainvalf.write(line)
    else:
        testf.write(line)

trainf.close()
trainvalf.close()
validf.close()
testf.close()

print('train:{}, valid:{}'.format(train_point, valid_point-train_point))
print('test:{}'.format(num_list-valid_point))
