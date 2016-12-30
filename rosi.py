# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from HttpClient import HttpClient
import sys,re,os
from threading import Thread
from Queue import Queue
from time import sleep


q = Queue()
imgCount = 0

class getRosiUrl(HttpClient):
    def __init__(self):
        self.__Url = "http://www.rosi8.cc/ROSIxiezhen/"
        self.__refer = 'http://www.rosi8.cc/'
        self._dir = r"D:\img\rosi"

    def _getPage(self):
        print "getpage"
        relurl =  self.__Url
        pageCode = self.Get(relurl,self.__refer)
        pattern = re.compile('<option value=\'(.*?)\'.*?</option>',re.S)
        items = re.findall(pattern,pageCode.decode("gb2312",'ignore'))
        return items


    def _getUrlList(self):
        print "geturllist"
        items = self._getPage()
        for item in items:
            relurl = self.__Url + item
            pageCode = self.Get(relurl, self.__refer)
            pattern = re.compile('<li><a href="/ROSIxiezhen/(.*?)".*?title="(.*?)".*?<i class="tit">.*?</li>', re.S)
            picitems = re.findall(pattern, pageCode.decode("gb2312", 'ignore'))
            for picitem in picitems:
                self._mkdir(picitem[1])
                self._getImgUrl(picitem[0])




    def _getImgUrl(self,piclist):
        print "getimgurl"
        relurl = self.__Url + piclist
        pageCode = self.Get(relurl,self.__refer)
        pattern = re.compile('<li><a>共(.*?)页: </a></li>',re.S)
        picitems = re.findall(pattern,pageCode.decode("gb2312", 'ignore'))
        for picitem in picitems:
            self._downImg(picitem,piclist)

    def _mkdir(self,dirname):
        dirname = dirname[0:15:]
        print dirname
        dir = self._dir + "\\" + dirname
        isExists = os.path.exists(dir)
        if not isExists:
            os.mkdir(dir)
        os.chdir(dir)


    def _downImg(self,pageNum,pageUrl):
        print "downimg"
        for i in range(1,int(pageNum)):
            imgUrl = self.__Url + pageUrl
            if i == 1:
                downUrl = imgUrl
            else:
                downUrl = imgUrl[:-5] + "_" + str(i) + ".html"

            print downUrl
            self._downPic(downUrl)


    def _downPic(self,downUrl):
        try:
            pageCode = self.Get(downUrl, self.__refer)
            pattern = re.compile(r"<img src='(.*?)'.*?alt.*?>", re.S)
            picitems = re.findall(pattern, pageCode.decode("gb2312", 'ignore'))
            print picitems[0]
            picurl = self.__refer + str(picitems[0])
            filename = picurl.split('/')[-1]
            print picurl
            isExists = os.path.exists(filename)
            if not isExists:
                print "no exist"
                with open(filename, 'wb') as file:
                    img = self.Get(picurl)
                    file.write(img)
        except Exception, e:
            print Exception, ":", e
            sleep(60)
            return self._downPic(downUrl)


rosi = getRosiUrl()

rosi._getUrlList()




