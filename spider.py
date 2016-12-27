# -*- coding: utf-8 -*-
import re,time,os
from HttpClient import HttpClient

class smzdm(HttpClient):

    def __init__(self):
        self._pageIndex = 1
        self._Url = "http://faxian.smzdm.com/9kuai9/p"
        print self._Url

    def _getAllGoods(self,pageIndex):
        relurl = self._Url + str(pageIndex)
        pageCode = self.Get(relurl)
        pattern = re.compile('<li timesort=.*?<h5.*?a target.*?>(.*?)</a></h5>.*?z-highlight.*?>(.*?)</div>.*?</li>',re.S)
        items = re.findall(pattern,pageCode.decode("utf-8"))
        for item in items:
            print item[0],item[1]

    def start(self):
         for i in range(1,6):
            self._getAllGoods(1)

bc = smzdm()

bc.start()
