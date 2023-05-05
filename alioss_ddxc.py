# -*- coding: utf-8 -*-
import json
import oss2
# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。

access_key_id = 'LTAI5t7ZSH4trjX33Q2A6B83'
access_key_secret = 'BeJGUwQdCRbAz26eEHYxjc4vJp8VoA'
bucket_name = 'cidi-ai-cloud-test1'
endpoint = 'https://oss-cn-shanghai.aliyuncs.com'


auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)


# 遍历文件。

# obj_list = []
# for b in oss2.ObjectIteratorV2(bucket, prefix='智慧物流3月测试/cidi_h5_xyc/front/'):
#     # print(b.key)
#     obj_list.append(b.key)
# obj_list.pop(0)
# print(len(obj_list))
# with open('tmp.json', 'w') as f:
#     json.dump(obj_list, f)
# exit()


with open('tmp.json', 'r') as f:
    obj_list = json.load(f)

# <yourObjectName>表示删除OSS文件时需要指定包含文件后缀，不包含Bucket名称在内的完整路径，例如abc/efg/123.jpg。
for idx, ObjectName in enumerate(obj_list):
    if idx % 2 != 0:   # 奇数 1 3 5 。。。
        bucket.delete_object(ObjectName)
        print(ObjectName)

exit()

# yourObjectName填写Object完整路径，完整路径中不能包含Bucket名称，例如exampledir/exampleobject.txt。
# yourLocalFile填写本地文件的完整路径，例如D:\\localpath\\examplefile.txt。
oss2.resumable_download(bucket, 'exampledir/exampleobject.txt', 'D:\\localpath\\examplefile.txt')
# 如未使用参数store指定目录，则会在HOME目录下建立.py-oss-upload目录来保存断点信息。

# Python SDK 2.1.0以上版本支持断点续传下载时设置以下可选参数。
# import sys
# # 当无法确定待下载的数据长度时，total_bytes的值为None。
# def percentage(consumed_bytes, total_bytes):
#     if total_bytes:
#         rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
#         print('\r{0}% '.format(rate), end='')
#         sys.stdout.flush()
# # 如果使用store指定了目录，则断点信息将保存在指定目录中。如果使用num_threads设置并发下载线程数，请将oss2.defaults.connection_pool_size设置为大于或等于并发下载线程数。默认并发下载线程数为1。
# oss2.resumable_download(bucket,  'exampledir/exampleobject.txt', 'D:\\localpath\\examplefile.txt',
#                       store=oss2.ResumableDownloadStore(root='/tmp'),
#                       # 指定当文件长度大于或等于可选参数multipart_threshold（默认值为10 MB）时，则使用断点续传下载。
#                       multiget_threshold=100*1024,
#                       # 设置分片大小，单位为字节，取值范围为100 KB~5 GB。默认值为100 KB。
#                       part_size=100*1024,
#                       # 设置下载进度回调函数。
#                       progress_callback=percentage,
#                       # 如果使用num_threads设置并发下载线程数，请将oss2.defaults.connection_pool_size设置为大于或等于并发下载线程数。默认并发下载线程数为1。
#                       num_threads=4)