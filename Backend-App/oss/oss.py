# -*- coding: utf-8 -*-
import oss2
import os, sys
import requests
import uuid



class OssSDK():
    def __init__(self,bucket):

        self.url= "http://%s.oss-cn-shanghai.aliyuncs.com"%bucket
        self.endpoint = "http://oss-cn-shanghai.aliyuncs.com"
        #print self.endpoint
        self.auth = oss2.Auth('LTAI4oPl28gTR8pH', 'dg3FXdjjn94p4BMKRbTpO6ryaNfrBn')
        self.bucket = oss2.Bucket(self.auth, self.endpoint, bucket)
        pass

    def clear(self):

        print "test"
        #self.put('1.mp4','1.mp4')
        #print(self.bucket.sign_url('GET', 'RadioInterfaceTBox.pb.cc', 60))
        for object_info in oss2.ObjectIterator(self.bucket):
            if object_info.key != 'NotFind.jpg':
                self.bucket.delete_object(object_info.key)
        #result = self.bucket.get_object('RadioInterfaceTBox.pb.cc')
        #print dir(result)

    def percentage(consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            if rate == 100:
                print '\r{0}% '.format(rate)

    def put_local(self,key,localfile,callback=percentage):
        return self.bucket.put_object_from_file(key,localfile,progress_callback=callback)

    def put_url(self,key,url,callback=percentage):
        r = requests.get(url)
        if r.status_code == 200:
            self.put_data(key,r.content)
            return True
        else:
            print "request url Error: %s"%url
            return False
        pass

    def put_url_auto_name(self,url,callback=percentage):
        key = str(uuid.uuid1()) + '.jpg'
        if self.put_url(key,url,callback=callback):
            print self.url + "/" + key
            return self.url + "/" + key
        else:
            return url

    def put_content_auto_name(self,content,callback=percentage):
        key = str(uuid.uuid1()) + '.jpg'
        self.put_data(key,content,callback=callback)
        print self.url + "/" + key
        return self.url + "/" + key

    def put_data(self,key,data,callback=percentage):
        return  self.bucket.put_object(key,data,progress_callback=callback)


    def test2(self):
        self.put_url_auto_name("http://img.hdwan.net/2016/11/p2389668649.jpg")

        #self.put('2.jpg',"http://img.hdwan.net/2016/11/p2389668649.jpg")