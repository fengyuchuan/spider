# -*- coding: utf-8 -*-
import re,time,os,sys
from HttpClient import HttpClient


class jiandan(HttpClient):

    def __init__(self):
        self._Url = "http://jandan.net/ooxx/"
        self._pageIndex = "0"
        self._dir = "D:\img"

    def _getNewPage(self):
        relurl = self._Url + "page-" +self._pageIndex + "#comments"
        pageCode = self.Get(relurl)
        pattern = re.compile('<span class="current-comment-page">(.*?)</span>',re.S)
        CurPage = re.search(pattern,pageCode.decode('utf-8'))
        pageNum = re.sub(r'\D', "", CurPage.group(1))
        return pageNum


    def _getAllPic(self,pageNum):
        relurl = self._Url + "page-" + str(pageNum) + "#comments"
        pageCode = self.Get(relurl)
        pattern = re.compile('<p>.*?<a .*?view_img_link">.*?</a>.*?<img src="(.*?)".*?</p>', re.S)
        pic = re.findall(pattern,pageCode.decode('utf-8'))
        return pic

    def _savePic(self,img_addr,folder,page):
        for item in img_addr:
            filename = item.split('/')[-1]
            print "save pic:" + filename
            DownUrl = str("http:" + item)
            pageFolder = folder + "\\" + str(page)
            isExists = os.path.exists(pageFolder)
            if not isExists:
                os.mkdir(pageFolder)
            os.chdir(pageFolder)
            with open(filename,'wb') as file:
                img = self.Get(DownUrl)
                file.write(img)


    def _start(self, number):
        newPage = self._getNewPage()
        targetPage = int(newPage) - number
        for i in range(int(newPage), targetPage, -1):
            img_add = self._getAllPic(i)
            self._savePic(img_add,self._dir,i)

jd = jiandan()
jd._start(2)