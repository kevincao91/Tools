# encoding=utf8
import os
from tqdm import tqdm
from basicFun import FILES


imgDir=r"/media/kevin/娱乐/xizang_database/label_data/JPEGImages"
xmlDir=r"/media/kevin/娱乐/xizang_database/label_data/Annotations"

imgType="jpg"
xmlType="xml"



def remove_xml():

    imgs = [x for x in FILES.get_sorted_files(imgDir) ]
    xmls = [x for x in FILES.get_sorted_files(xmlDir) ]
    
    # print(imgs)
    # remove xml
    count = 0
    for xml in tqdm(xmls):
        find_img_name=xml.replace(xmlType, imgType)
        # print(find_img_name)
        if find_img_name in imgs:
            pass
            # print('save %s'%xml)
        else:
            print('del %s'%xml)
            os.remove(os.path.join(xmlDir, xml))
            count+=1
    print("remove {} xmls.\n".format(count))

def remove_img():

    imgs = [x for x in FILES.get_sorted_files(imgDir) ]
    xmls = [x for x in FILES.get_sorted_files(xmlDir) ]
    
    # print(imgs)
    # remove img
    count = 0
    for img in tqdm(imgs):
        find_xml_name=img.replace(imgType, xmlType)
        # print(find_img_name)
        if find_xml_name in xmls:
            pass
            # print('save %s'%img)
        else:
            print('del %s'%img)
            os.remove(os.path.join(imgDir, img))
            count+=1
    print("remove {} imgs.\n".format(count))


if __name__ == "__main__":
    remove_img()
    remove_xml()




