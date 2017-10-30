# -*- coding: utf8 -*-
from unittest import *
import os
import api
from common import *
from common2 import *
import var as v
import data
import time as t


class AP_CLEAR_CHAN(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_lan_wifi_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='STA got no ip address.')
            else:
                os.popen('arp -d')
                lan_wifi = chkOSPingAvailable(result['ip'], 5, self.__class__.__name__)
                self.assertTrue(lan_wifi, "Lan to Wifi ping Failed.")
        else:
            self.assertTrue(res2gConn, "STA association wasnot successful.")

    def assoc_lan_wifi_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='STA got no ip address.')
            else:
                os.popen('arp -d')
                lan_wifi = chkOSPingAvailable(result['ip'], 5, self.__class__.__name__)
                self.assertTrue(lan_wifi, "Lan to Wifi ping Failed.")
        else:
            self.assertTrue(res5gConn, "STA association wasnot successful.")

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

class AP_WPS(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': 'miwifi_wps',
            'encryption': 'mixed-psk',
            'pwd': '12345678',
            'channel': v.CHANNEL13
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': 'miwifi_wps_5G',
            'encryption': 'mixed-psk',
            'pwd': '12345678',
            'channel': v.CHANNEL36
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setWpsOn(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        api.setWpsOff(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_wps(self):

        wpsStatus = api.checkWpsStatus(self.dut, self.__class__.__name__)
        if wpsStatus['status'] == None:
            self.fail(msg='Cannot Open WPS')
        self.assertEqual(wpsStatus['status'], 1, 'Cannot Open WPS')

        wpsConn = setAdbWps(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        if wpsConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='WPS STA got no ip address.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(wpsConn, "WPS Connection Failed.")

class AP_CLEAR_LOW(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'min',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'min',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_CLEAR_MID(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_CLEAR_HIGH(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'max',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'max',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_CLEAR_LOW_TXPOWER(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = ShellClient(v.CONNECTION_TYPE)
        self.dut2 = api.HttpClient()
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Connection is failed. please check your remote settings.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def autochan_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def autochan_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'min',
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan1_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan6_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL6,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan11_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL11,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan13_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL13,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan36_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan52_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL52,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan149_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL149,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan165_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL165,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")


class AP_CLEAR_MID_TXPOWER(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = ShellClient(v.CONNECTION_TYPE)
        self.dut2 = api.HttpClient()
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Connection is failed. please check your remote settings.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def autochan_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def autochan_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'mid',
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan1_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan6_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL6,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan11_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL11,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan13_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL13,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan36_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan52_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL52,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan149_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL149,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan165_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL165,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")


class AP_CLEAR_HIGH_TXPOWER(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = ShellClient(v.CONNECTION_TYPE)
        self.dut2 = api.HttpClient()
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Connection is failed. please check your remote settings.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def autochan_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def autochan_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'max',
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan1_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan6_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL6,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan11_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL11,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan13_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL13,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan36_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan52_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL52,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan149_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL149,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan165_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL165,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

class AP_MIXEDPSK_CHAN_CHECK(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = ShellClient(v.CONNECTION_TYPE)
        self.dut2 = api.HttpClient()
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Connection is failed. please check your remote settings.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def chan1_check_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        chan_expect = api.getWifiChannel(self.dut2, '2g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)

        if int(eval(v.CHANNEL1)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 1 Setup failed.")

    def chan6_check_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        chan_expect = api.getWifiChannel(self.dut2, '2g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)

        if int(eval(v.CHANNEL6)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 6 Setup failed.")

    def chan11_check_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        chan_expect = api.getWifiChannel(self.dut2, '2g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)

        if int(eval(v.CHANNEL11)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 11 Setup failed.")

    def chan13_check_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        chan_expect = api.getWifiChannel(self.dut2, '2g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)

        if int(eval(v.CHANNEL13)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 13 Setup failed.")

    def chan36_check_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        chan_expect = api.getWifiChannel(self.dut2, '5g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL36)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 36 Setup failed.")

    def chan44_check_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL44,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        chan_expect = api.getWifiChannel(self.dut2, '5g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL44)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 44 Setup failed.")

    def chan52_check_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        chan_expect = api.getWifiChannel(self.dut2, '5g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL52)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 52 Setup failed.")

    def chan60_check_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL60,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        chan_expect = api.getWifiChannel(self.dut2, '5g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL60)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 60 Setup failed.")

    def chan157_check_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        chan_expect = api.getWifiChannel(self.dut2, '5g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL157)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 157 Setup failed.")

    def chan165_check_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        chan_expect = api.getWifiChannel(self.dut2, '5g', self.__class__.__name__)
        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL165)) == chan_expect == chan_actually:
            pass
        else:
            self.fail("Channel 165 Setup failed.")


class AP_CLEAR_CHANSELECTION(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Http connection is failed. please check your remote settings.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def chanselection_2g(self):
        count = 0
        chan2g = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        while count < 5:
            api.setWifi(self.dut, self.__class__.__name__, **option2g)
            channel = api.getWifiChannel(self.dut, '2g', self.__class__.__name__)
            if channel not in chan2g:
                self.fail("Current auto-selected channel isnot between 1 and 11.")
            else:
                count += 1

    def chanselection_5g(self):
        count = 0
        chan5g = [149, 153, 157, 161]
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        while count < 5:
            api.setWifi(self.dut, self.__class__.__name__, **option5g)
            channel = api.getWifiChannel(self.dut, '5g', self.__class__.__name__)
            if channel not in chan5g:
                self.fail("Current auto-selected channel isnot between 149 and 161.")
            else:
                count += 1


class AP_CLEAR_CHAN_WHITELIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        option = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 0
        }
        api.setEditDevice(self.dut, self.__name__, **option)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

    @classmethod
    def tearDownClass(self):

        option = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 1
        }
        api.setEditDevice(self.dut, self.__name__, **option)

        option2 = {
            'model': 1,
            'enable': 0
        }
        api.setWifiMacFilter(self.dut, self.__name__, **option2)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_clear_sta_in_whitelist_2g(self):

        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                passPercent = resPingPercent['pass']
            else:
                passPercent = 0

        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        if res2gConn is False:
            self.fail("Association wasnot successful which sta in whitelist.")
        self.assertGreaterEqual(passPercent, v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")
        # connType = api.getOnlineDeviceType(self.dut, self.__class__.__name__)
        # if self.staMac in connType.keys():
        #     self.fail(msg='STA should be kicked off.'

    def assoc_clear_sta_in_whitelist_5g(self):

        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                passPercent = resPingPercent['pass']
            else:
                passPercent = 0

        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 1
        }

        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        if res5gConn is False:
            self.fail("Association wasnot successful which sta in whitelist.")
        self.assertGreaterEqual(passPercent, v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")
        # connType = api.getOnlineDeviceType(self.dut, self.__class__.__name__)
        # if self.staMac in connType.keys():
        #     self.fail(msg='STA should be kicked off.')

    def assoc_clear_sta_outof_whitelist_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        self.assertFalse(res2gConn, "Association wasnot supposed to be successful which sta outof whitelist.")
        # 鍒犻櫎鎵�鏈墂hitelist鍒欑櫧鍚嶅崟涓嶅啀鐢熸晥
        # option = {
        #     'model': 1,
        #     'mac': '11:22:33:44:55:66',
        #     'option': 1
        # }
        # api.setEditDevice(self.dut, self.__class__.__name__, **option)
        #
        # res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        # self.assertTrue(res2gConn, "Association should be successful when no sta in whitelist at all.")
        #
        # option = {
        #     'model': 1,
        #     'mac': '11:22:33:44:55:66',
        #     'option': 0
        # }
        # api.setEditDevice(self.dut, self.__class__.__name__, **option)

    def assoc_clear_sta_outof_whitelist_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        self.assertFalse(res5gConn, "Association wasnot supposed to be successful which sta outof whitelist.")
        # 鍒犻櫎鎵�鏈墂hitelist鍒欑櫧鍚嶅崟涓嶅啀鐢熸晥
        # option = {
        #     'model': 1,
        #     'mac': '11:22:33:44:55:66',
        #     'option': 1
        # }
        # api.setEditDevice(self.dut, self.__class__.__name__, **option)
        #
        # res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        # self.assertTrue(res5gConn, "Association should be successful when no sta in whitelist at all.")
        #
        # option = {
        #     'model': 1,
        #     'mac': '11:22:33:44:55:66',
        #     'option': 0
        # }
        # api.setEditDevice(self.dut, self.__class__.__name__, **option)


class AP_CLEAR_CHAN_BLACKLIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        option = {
            'model': 0,
            'mac': '11:22:33:44:55:66',
            'option': 0
        }
        api.setEditDevice(self.dut, self.__name__, **option)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

    @classmethod
    def tearDownClass(self):
        option = {
            'model': 0,
            'mac': '11:22:33:44:55:66',
            'option': 1
        }
        api.setEditDevice(self.dut, self.__name__, **option)

        api.setWifiMacFilter(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_clear_sta_outof_blacklist_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association should be successful which sta outof blacklist.")

    def assoc_clear_sta_outof_blacklist_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association should be successful which sta outof blacklist.")

    def assoc_clear_sta_in_blacklist_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        self.assertTrue(res2gConn, "Association should be successful which sta outof blacklist.")

        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        connType = api.getOnlineDeviceType(self.dut, self.__class__.__name__)

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        if self.staMac in connType.keys():
            self.fail(msg='STA should be kicked off.')

        self.assertFalse(res2gConn, "Association wasnot supposed to be successful which sta in blacklist.")

    def assoc_clear_sta_in_blacklist_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        self.assertTrue(res5gConn, "Association should be successful which sta outof blacklist.")

        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        connType = api.getOnlineDeviceType(self.dut, self.__class__.__name__)

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        if self.staMac in connType.keys():
            self.fail(msg='STA should be kicked off.')

        self.assertFalse(res5gConn, "Association wasnot supposed to be successful which sta in blacklist.")


class AP_CLEAR_CHAN_REPEAT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_repeat_clear_sta_2g(self):

        res2gConn = setAdbClearStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_clear_sta_5g(self):

        res5gConn = setAdbClearStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        self.assertTrue(res5gConn, "Not all association were successful.")


class AP_PSK2_CHAN(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_PSK2_CHAN_REPEAT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'psk2',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_repeat_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        self.assertTrue(res5gConn, "Not all association were successful.")


class AP_MIXEDPSK_BW_CHECK(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = ShellClient(v.CONNECTION_TYPE)
        self.dut2 = api.HttpClient()
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Connection is failed. please check your remote settings.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def autochan_BW_check_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        bw = getWlanBWRate(self.dut, "2g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "2g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Auto BW isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 20:
                pass
            else:
                self.fail("Auto BW isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            if bw == v.R1CL_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Auto BW isnot correct.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Auto BW isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Auto BW isnot correct.")

    def autochan_BW_check_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        bw = getWlanBWRate(self.dut, "5g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_5G['80']:
                pass
            else:
                self.fail("Auto BW isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 80:
                pass
            else:
                self.fail("Auto BW isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Donot Support 5G.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_5G['80']:
                pass
            else:
                self.fail("Auto BW isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_5G['80']:
                pass
            else:
                self.fail("Auto BW isnot correct.")

    def chan1_BW40_CHECK_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL1,
            'bandwidth': '40',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        bw = getWlanBWRate(self.dut, "2g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "2g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 1 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 40:
                pass
            else:
                self.fail("Channel 1 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            if bw == v.R1CL_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 1 BW40 isnot correct.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 1 BW40 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 1 BW40 isnot correct.")

    def chan6_BW20_CHECK_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL6,
            'bandwidth': '20',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        bw = getWlanBWRate(self.dut, "2g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "2g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 6 BW20 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 20:
                pass
            else:
                self.fail("Channel 6 BW20 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            if bw == v.R1CL_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 6 BW20 isnot correct.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 6 BW20 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 6 BW20 isnot correct.")

    def chan11_BW40_CHECK_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL11,
            'bandwidth': '40',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        bw = getWlanBWRate(self.dut, "2g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "2g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 11 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 40:
                pass
            else:
                self.fail("Channel 11 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            if bw == v.R1CL_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 11 BW40 isnot correct.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 1 BW40 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_2G['40']:
                pass
            else:
                self.fail("Channel 11 BW40 isnot correct.")

    def chan13_BWauto_CHECK_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL13,
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        bw = getWlanBWRate(self.dut, "2g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "2g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 13 BWauto isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 20:
                pass
            else:
                self.fail("Channel 13 BWauto isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            if bw == v.R1CL_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 13 BWauto isnot correct.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 13 BWauto isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_2G['20']:
                pass
            else:
                self.fail("Channel 13 BWauto isnot correct.")

    def chan36_BW20_CHECK_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '20',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        bw = getWlanBWRate(self.dut, "5g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 36 BW20 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 20:
                pass
            else:
                self.fail("Channel 36 BW20 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Donot Support 5G.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 36 BW20 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 36 BW20 isnot correct.")

    def chan48_BW40_CHECK_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL48,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '40',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        bw = getWlanBWRate(self.dut, "5g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_5G['40']:
                pass
            else:
                self.fail("Channel 48 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 40:
                pass
            else:
                self.fail("Channel 48 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Donot Support 5G.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_5G['40']:
                pass
            else:
                self.fail("Channel 48 BW40 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_5G['40']:
                pass
            else:
                self.fail("Channel 48 BW40 isnot correct.")

    def chan52_BW80_CHECK_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '80',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        bw = getWlanBWRate(self.dut, "5g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_5G['80']:
                pass
            else:
                self.fail("Channel 52 BW80 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 80:
                pass
            else:
                self.fail("Channel 52 BW80 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Donot Support 5G.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_5G['80']:
                pass
            else:
                self.fail("Channel 52 BW80 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_5G['80']:
                pass
            else:
                self.fail("Channel 52 BW80 isnot correct.")

    def chan64_BW20_CHECK_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL64,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '20',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        bw = getWlanBWRate(self.dut, "5g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 64 BW20 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 20:
                pass
            else:
                self.fail("Channel 64 BW20 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Donot Support 5G.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 64 BW20 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 64 BW20 isnot correct.")

    def chan157_BW40_CHECK_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '40',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        bw = getWlanBWRate(self.dut, "5g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_5G['40']:
                pass
            else:
                self.fail("Channel 157 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 40:
                pass
            else:
                self.fail("Channel 157 BW40 isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Donot Support 5G.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_5G['40']:
                pass
            else:
                self.fail("Channel 157 BW40 isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_5G['40']:
                pass
            else:
                self.fail("Channel 157 BW40 isnot correct.")

    def chan165_BWauto_CHECK_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        bw = getWlanBWRate(self.dut, "5g", self.__class__.__name__)
        bw_Broadcom = getBroadcomBW(self.dut, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            if bw == v.R1CM_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 165 BWauto isnot correct.")
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            if bw_Broadcom == 20:
                pass
            else:
                self.fail("Channel 165 BWauto isnot correct.")
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Donot Support 5G.")
        if v.DUT_MODULE == 'R3P':
            if bw == v.R3P_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 165 BWauto isnot correct.")
        if v.DUT_MODULE == 'R3D':
            if bw == v.R3D_MAX_RATE_5G['20']:
                pass
            else:
                self.fail("Channel 165 BWauto isnot correct.")


class AP_MIXEDPSK_CHAN(TestCase):
    '''
    channel 随机在可用信道中选取
    '''
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")
        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        if ret3 is False:
            raise Exception("SSH/Telnet connection is failed. please check your remote settings.")

        self.channel2 = generateRandomChannel(v.CHANNEL_2_ALL)
        self.channel5 = generateRandomChannel(v.CHANNEL_5_ALL)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': self.channel2,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': self.channel5,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_router_ping_psk2_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getPingStatus(self.dut2, result['ip'], v.PING_BIG_COUNT,
                                                  self.__class__.__name__, v.PING_BIG_SIZE)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_BIG_PERCENT_PASS,
                                        "Router Ping Sta with BigSizePacket Failed.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)

    def assoc_router_ping_psk2_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getPingStatus(self.dut2, result['ip'], v.PING_BIG_COUNT,
                                                  self.__class__.__name__, v.PING_BIG_SIZE)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_BIG_PERCENT_PASS,
                                        "Router Ping Sta with BigSizePacket Failed.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_psk_sta_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_tkippsk2_sta_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_tkippsk_sta_2g(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)


class AP_MIXEDPSK_CHAN_BW80(TestCase):
    '''
    AP_MIXEDPSK_CHAN can cover this case
    '''
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '80',
        }

        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_MIXEDPSK_CHAN_BW40(TestCase):
    '''
    2.4g BW40M covered by AP_MIXEDPSK_CHAN
    '''
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        # option2g = {
        #     'wifiIndex': 1,
        #     'ssid': v.SSID,
        #     'channel': v.CHANNEL11,
        #     'encryption': 'mixed-psk',
        #     'pwd': v.KEY,
        #     'bandwidth': '40'
        # }
        self.channel5 = generateRandomChannel(v.CHANNEL_5_ALL)
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': self.channel5,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '40'
        }

        # api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        # option2g = {
        #     'wifiIndex': 1,
        #     'on': 0,
        # }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        # api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    # def assoc_psk2_sta_2g(self):
    #
    #     res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
    #     if res2gConn:
    #         result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
    #         if result['ip'] == '':
    #             self.fail(msg='no ip address got.')
    #         else:
    #             resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
    #                                               self.__class__.__name__)
    #             self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
    #                                     "Ping responsed percent werenot good enough.")
    #     else:
    #         self.assertTrue(res2gConn, "Association wasnot successful.")
    #
    # def assoc_psk_sta_2g(self):
    #
    #     res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
    #     if res2gConn:
    #         result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
    #         if result['ip'] == '':
    #             self.fail(msg='no ip address got.')
    #         else:
    #             resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
    #                                               self.__class__.__name__)
    #             self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
    #                                     "Ping responsed percent werenot good enough.")
    #     else:
    #         self.assertTrue(res2gConn, "Association wasnot successful.")

    # def assoc_tkippsk2_sta_2g(self):
    #
    #     res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
    #     if res2gConn:
    #         result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
    #         if result['ip'] == '':
    #             self.fail(msg='no ip address got.')
    #         else:
    #             resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
    #                                               self.__class__.__name__)
    #             self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
    #                                     "Ping responsed percent werenot good enough.")
    #     else:
    #         self.assertTrue(res2gConn, "Association wasnot successful.")
    #
    # def assoc_tkippsk_sta_2g(self):
    #
    #     res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
    #     if res2gConn:
    #         result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
    #         if result['ip'] == '':
    #             self.fail(msg='no ip address got.')
    #         else:
    #             resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
    #                                               self.__class__.__name__)
    #             self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
    #                                     "Ping responsed percent werenot good enough.")
    #     else:
    #         self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_MIXEDPSK_CHAN_BW20(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        self.channel2 = generateRandomChannel(v.CHANNEL_2_ALL)
        self.channel5 = generateRandomChannel(v.CHANNEL_5_ALL)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': self.channel2,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '20'
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': self.channel5,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '20'
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel5)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. Channel = %s" % self.channel5)

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)

    def assoc_psk_sta_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)

    def assoc_tkippsk2_sta_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)

    def assoc_tkippsk_sta_2g(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. Channel = %s' % self.channel2)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. Channel = %s" % self.channel2)


class AP_MIXEDPSK_CHAN_SSIDSPEC(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SPECIAL_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SPECIAL_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_ssidspec_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.SPECIAL_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. SSID = %s" % v.SPECIAL_SSID)

    def assoc_psk2_sta_ssidspec_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.SPECIAL_SSID_5G)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. SSID = %s" % v.SPECIAL_SSID_5G)

class AP_MIXEDPSK_CHAN_KEYSPEC(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.SPECIAL_KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.SPECIAL_KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_keyspec_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. KEY = %s' % v.SPECIAL_KEY)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. KEY = %s" % v.SPECIAL_KEY)

    def assoc_psk2_sta_keyspec_5g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. KEY = %s' % v.SPECIAL_KEY)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. KEY = %s" % v.SPECIAL_KEY)

class AP_MIXEDPSK_CHAN_SSIDCHINESE(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.CHINESE_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.CHINESE_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_ssidchinese_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.CHINESE_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. SSID = %s" % v.CHINESE_SSID)

    def assoc_psk2_sta_ssidchinese_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.CHINESE_SSID_5G)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. SSID = %s" % v.CHINESE_SSID_5G)

class AP_MIXEDPSK_CHAN_REPEAT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_repeat_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        self.assertTrue(res5gConn, "Not all association were successful.")

    def assoc_repeat_psk_sta_2g(self):

        res2gConn = setAdbPskStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_psk_sta_5g(self):

        res5gConn = setAdbPskStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        self.assertTrue(res5gConn, "Not all association were successful.")

    def assoc_repeat_tkippsk2_sta_2g(self):

        res2gConn = setAdbTkipPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        self.assertTrue(res5gConn, "Not all association were successful.")

    def assoc_repeat_tkippsk_sta_2g(self):

        res2gConn = setAdbTkipPskStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        self.assertTrue(res5gConn, "Not all association were successful.")

class AP_CLEAR_BSD(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'none',
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_clear_near_field_sta(self):

        resConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(resConn, msg="Association wasnot successful.")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

        resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertTrue(resConn2, msg="STA Online Successfully, But doesnot associate with 5g")


class AP_MIXEDPSK_BSD(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta(self):

        resConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertTrue(resConn, msg="Association wasnot successful.")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

        resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertTrue(resConn2, msg="STA Online Successfully, But doesnot associate with 5g")

    def assoc_psk2_near_field_sta_repeat(self):

        count = 0
        failedCount = 0
        assoc5gCount = 0
        assoc2gCount = 0

        while count < 10:
            resConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)

            if resConn and result['ip'] != '':
                resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                if resConn2:
                    assoc5gCount += 1
                else:
                    assoc2gCount += 1
            else:
                failedCount += 1

            count += 1

        self.assertEqual(failedCount, 0, 'STA try to assoc 10 times, Failed %d, 5G Online %d, 2G Online %d' % (failedCount, assoc5gCount, assoc2gCount))
        self.assertEqual(assoc2gCount, 0, 'STA try to assoc 10 times, 5G Online %d, 2G Online %d' % (assoc5gCount, assoc2gCount))


    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

class AP_BSD_CHAN_CHECK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Connection is failed. please check your remote settings.")

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def chan_1_36_check_bsd(self):

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'channel1': v.CHANNEL1,
            'channel2': v.CHANNEL36,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        chan_expect_2g = api.getWifiChannel(self.dut, '2g', self.__class__.__name__)
        chan_actually_2g = getWlanChannel(self.dut2, "2g", self.__class__.__name__)

        if int(eval(v.CHANNEL1)) == chan_expect_2g == chan_actually_2g:
            pass
        else:
            self.fail("Channel 1 Setup failed.")

        chan_expect_5g = api.getWifiChannel(self.dut, '5g', self.__class__.__name__)
        chan_actually_5g = getWlanChannel(self.dut2, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL36)) == chan_expect_5g == chan_actually_5g:
            pass
        else:
            self.fail("Channel 36 Setup failed.")

    def chan_6_52_check_bsd(self):

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'channel1': v.CHANNEL6,
            'channel2': v.CHANNEL52,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        chan_expect_2g = api.getWifiChannel(self.dut, '2g', self.__class__.__name__)
        chan_actually_2g = getWlanChannel(self.dut2, "2g", self.__class__.__name__)

        if int(eval(v.CHANNEL6)) == chan_expect_2g == chan_actually_2g:
            pass
        else:
            self.fail("Channel 6 Setup failed.")

        chan_expect_5g = api.getWifiChannel(self.dut, '5g', self.__class__.__name__)
        chan_actually_5g = getWlanChannel(self.dut2, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL52)) == chan_expect_5g == chan_actually_5g:
            pass
        else:
            self.fail("Channel 52 Setup failed.")

    def chan_13_165_check_bsd(self):

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'channel1': v.CHANNEL13,
            'channel2': v.CHANNEL165,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        chan_expect_2g = api.getWifiChannel(self.dut, '2g', self.__class__.__name__)
        chan_actually_2g = getWlanChannel(self.dut2, "2g", self.__class__.__name__)

        if int(eval(v.CHANNEL13)) == chan_expect_2g == chan_actually_2g:
            pass
        else:
            self.fail("Channel 13 Setup failed.")

        chan_expect_5g = api.getWifiChannel(self.dut, '5g', self.__class__.__name__)
        chan_actually_5g = getWlanChannel(self.dut2, "5g", self.__class__.__name__)

        if int(eval(v.CHANNEL165)) == chan_expect_5g == chan_actually_5g:
            pass
        else:
            self.fail("Channel 165 Setup failed.")

class AP_BSD_BW_CHECK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Connection is failed. please check your remote settings.")

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def autochan_BW_check_bsd(self):

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)
        bw_2g = getWlanBWRate(self.dut2, "2g", self.__class__.__name__)
        bw_5g = getWlanBWRate(self.dut2, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            self.assertEqual(bw_2g, v.R1CM_MAX_RATE_2G['20'], 'BSD 2g Auto BW isnot correct.')
            self.assertEqual(bw_5g, v.R1CM_MAX_RATE_5G['80'], 'BSD 5g Auto BW isnot correct.')
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            self.assertEqual(bw_2g, v.R1D_MAX_RATE_2G['20'], 'BSD 2g Auto BW isnot correct.')
            self.assertEqual(bw_5g, v.R1D_MAX_RATE_5G['80'], 'BSD 5g Auto BW isnot correct.')
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Device Donot Support BSD.")
        if v.DUT_MODULE == 'R3P':
            self.assertEqual(bw_2g, v.R3P_MAX_RATE_2G['20'], 'BSD 2g Auto BW isnot correct.')
            self.assertEqual(bw_5g, v.R3P_MAX_RATE_5G['80'], 'BSD 5g Auto BW isnot correct.')
        if v.DUT_MODULE == 'R3D':
            self.assertEqual(bw_2g, v.R3D_MAX_RATE_2G['20'], 'BSD 2g Auto BW isnot correct.')
            self.assertEqual(bw_5g, v.R3D_MAX_RATE_5G['80'], 'BSD 5g Auto BW isnot correct.')

    def chan6_48_BW40_20_check_bsd(self):

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'channel1': v.CHANNEL6,
            'bandwidth1': '40',
            'channel2': v.CHANNEL48,
            'bandwidth2': '20',

        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)
        bw_2g = getWlanBWRate(self.dut2, "2g", self.__class__.__name__)
        bw_5g = getWlanBWRate(self.dut2, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            self.assertEqual(bw_2g, v.R1CM_MAX_RATE_2G['40'], 'BSD 2g BW40 isnot correct.')
            self.assertEqual(bw_5g, v.R1CM_MAX_RATE_5G['20'], 'BSD 5g BW20 isnot correct.')
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            self.assertEqual(bw_2g, v.R1D_MAX_RATE_2G['40'], 'BSD 2g BW40 isnot correct.')
            self.assertEqual(bw_5g, v.R1D_MAX_RATE_5G['20'], 'BSD 5g BW20 isnot correct.')
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Device Donot Support BSD.")
        if v.DUT_MODULE == 'R3P':
            self.assertEqual(bw_2g, v.R3P_MAX_RATE_2G['40'], 'BSD 2g BW40 isnot correct.')
            self.assertEqual(bw_5g, v.R3P_MAX_RATE_5G['20'], 'BSD 5g BW20 isnot correct.')
        if v.DUT_MODULE == 'R3D':
            self.assertEqual(bw_2g, v.R3D_MAX_RATE_2G['40'], 'BSD 2g BW40 isnot correct.')
            self.assertEqual(bw_5g, v.R3D_MAX_RATE_5G['20'], 'BSD 5g BW20 isnot correct.')

    def chan13_64_BW20_40_check_bsd(self):

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'channel1': v.CHANNEL13,
            'bandwidth1': '20',
            'channel2': v.CHANNEL64,
            'bandwidth2': '40',

        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)
        bw_2g = getWlanBWRate(self.dut2, "2g", self.__class__.__name__)
        bw_5g = getWlanBWRate(self.dut2, "5g", self.__class__.__name__)

        if v.DUT_MODULE in ['R1CM', 'R3', 'R3A', 'R3G']:
            self.assertEqual(bw_2g, v.R1CM_MAX_RATE_2G['20'], 'BSD 2g BW20 isnot correct.')
            self.assertEqual(bw_5g, v.R1CM_MAX_RATE_5G['40'], 'BSD 5g BW40 isnot correct.')
        if v.DUT_MODULE == 'R1D' or v.DUT_MODULE == 'R2D':
            self.assertEqual(bw_2g, v.R1D_MAX_RATE_2G['20'], 'BSD 2g BW20 isnot correct.')
            self.assertEqual(bw_5g, v.R1D_MAX_RATE_5G['40'], 'BSD 5g BW40 isnot correct.')
        if v.DUT_MODULE == 'R1CL' or v.DUT_MODULE == 'R3L':
            self.fail("Device Donot Support BSD.")
        if v.DUT_MODULE == 'R3P':
            self.assertEqual(bw_2g, v.R3P_MAX_RATE_2G['20'], 'BSD 2g BW20 isnot correct.')
            self.assertEqual(bw_5g, v.R3P_MAX_RATE_5G['40'], 'BSD 5g BW40 isnot correct.')
        if v.DUT_MODULE == 'R3D':
            self.assertEqual(bw_2g, v.R3D_MAX_RATE_2G['20'], 'BSD 2g BW20 isnot correct.')
            self.assertEqual(bw_5g, v.R3D_MAX_RATE_5G['40'], 'BSD 5g BW40 isnot correct.')

class AP_MIXEDPSK_BSD_SSIDSPEC(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'bsd': 1,
            'ssid1': v.SPECIAL_SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SPECIAL_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SPECIAL_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SPECIAL_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SPECIAL_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")


class AP_MIXEDPSK_BSD_KEYSPEC(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.SPECIAL_KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.SPECIAL_KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.SPECIAL_KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.SPECIAL_KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.SPECIAL_KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")


class AP_MIXEDPSK_BSD_SSIDCHINESE(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'bsd': 1,
            'ssid1': v.CHINESE_SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.CHINESE_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.CHINESE_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.CHINESE_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.CHINESE_SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")


class AP_MIXEDPSK_BSD_WHITELIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

        option = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 0
        }
        api.setEditDevice(self.dut, self.__name__, **option)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo['mac'].upper()

    @classmethod
    def tearDownClass(self):
        option = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 1
        }
        api.setEditDevice(self.dut, self.__name__, **option)
        api.setWifiMacFilter(self.dut, self.__name__)

        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta_in_whitelist(self):

        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                passPercent = resPingPercent['pass']
            else:
                passPercent = 0

        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        if res2gConn is False:
            self.fail("Association wasnot successful which sta in whitelist.")
        self.assertGreaterEqual(passPercent, v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk2_near_field_sta_outof_whitelist(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        self.assertFalse(res2gConn, "Association wasnot supposed to be successful which sta outof whitelist.")


class AP_MIXEDPSK_BSD_BLACKLIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo['mac'].upper()

    @classmethod
    def tearDownClass(self):
        api.setWifiMacFilter(self.dut, self.__name__)

        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta_outof_blacklist(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association should be successful which sta outof blacklist.")

    def assoc_psk2_near_field_sta_in_blacklist(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        self.assertTrue(res2gConn, "Association should be successful which sta outof blacklist.")

        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        connType = api.getOnlineDeviceType(self.dut, self.__class__.__name__)

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        if self.staMac in connType.keys():
            self.fail(msg='STA should be kicked off.')

        self.assertFalse(res2gConn, "Association wasnot supposed to be successful which sta in blacklist.")


class AP_MIXEDPSK_BSD_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo['mac'].upper()

    @classmethod
    def tearDownClass(self):
        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")


class AP_GUEST_CLEAR(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_clear_sta_guest(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_GUEST_PSK2(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_psk2_sta_guest(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_GUEST_MIXEDPSK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_psk2_sta_guest(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_guest(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_guest(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_guest(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_GUEST_CLEAR_WHITELIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

        option = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 0
        }
        api.setEditDevice(self.dut, self.__name__, **option)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

    @classmethod
    def tearDownClass(self):
        option = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 1
        }
        api.setEditDevice(self.dut, self.__name__, **option)
        option2 = {
            'model': 1,
            'enable': 0
        }
        api.setWifiMacFilter(self.dut, self.__name__, **option2)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_clear_sta_in_whitelist_guest(self):
        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                passPercent = resPingPercent['pass']
            else:
                passPercent = 0

        option = {
            'model': 1,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        if res2gConn is False:
            self.fail("Association wasnot successful which sta in whitelist.")
        self.assertGreaterEqual(passPercent, v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

        # connType = api.getOnlineDeviceType(self.dut, self.__class__.__name__)
        # if self.staMac in connType.keys():
        #     self.fail(msg='STA should be kicked off.')

    def assoc_clear_sta_outof_whitelist_guest(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        self.assertFalse(res2gConn, "Association wasnot supposed to be successful which sta outof whitelist.")
        # option = {
        #     'model': 1,
        #     'mac': '11:22:33:44:55:66',
        #     'option': 1
        # }
        # api.setEditDevice(self.dut, self.__class__.__name__, **option)
        #
        # res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        # self.assertTrue(res2gConn, "Association should be successful when no sta in whitelist at all.")
        #
        # option = {
        #     'model': 1,
        #     'mac': '11:22:33:44:55:66',
        #     'option': 0
        # }
        # api.setEditDevice(self.dut, self.__class__.__name__, **option)


class AP_GUEST_CLEAR_BLACKLIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

        option = {
            'model': 0,
            'mac': '11:22:33:44:55:66',
            'option': 0
        }
        api.setEditDevice(self.dut, self.__name__, **option)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

    @classmethod
    def tearDownClass(self):
        option = {
            'model': 0,
            'mac': '11:22:33:44:55:66',
            'option': 1
        }
        api.setEditDevice(self.dut, self.__name__, **option)
        api.setWifiMacFilter(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_clear_sta_outof_blacklist_guest(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association should be successful which sta outof blacklist.")

    def assoc_clear_sta_in_blacklist_guest(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)
        self.assertTrue(res2gConn, "Association should be successful which sta outof blacklist.")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 0,
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        # connType = api.getOnlineDeviceType(self.dut, self.__class__.__name__)
        checkSTA = True
        if v.DUT_MODULE in ['R1CM', "R3", "R3P", "R3A", "R3G", "R1CL", "R3L"]:
            checkSTA = chkStaOnline(self.dut2, 'MTK_guest', result['ip'], self.__class__.__name__)
        if v.DUT_MODULE in ['R1D', 'R2D']:
            checkSTA = chkStaOnline(self.dut2, 'Broadcom_guest', result['ip'], self.__class__.__name__)
        if v.DUT_MODULE in ["R3D"]:
            checkSTA = chkStaOnline(self.dut2, 'Qualcomm_guest', result['ip'], self.__class__.__name__)

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 1,
        }
        api.setEditDevice(self.dut, self.__class__.__name__, **option)

        # if self.staMac in connType.keys():
        #     self.fail(msg='STA should be kicked off.')
        self.assertFalse(checkSTA, "STA should be kicked off.")

        self.assertFalse(res2gConn, "Association wasnot supposed to be successful which sta in blacklist.")


class AP_GUEST_CLEAR_REPEAT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_repeat_clear_sta_guest(self):

        res2gConn = setAdbClearStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")


class AP_GUEST_MIXEDPSK_REPEAT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_repeat_psk2_sta_guest(self):

        res2gConn = setAdbPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_psk_sta_guest(self):

        res2gConn = setAdbPskStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_tkippsk2_sta_guest(self):

        res2gConn = setAdbTkipPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")

    def assoc_repeat_tkippsk_sta_guest(self):

        res2gConn = setAdbTkipPskStaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")


class AP_GUEST_PSK2_REPEAT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_repeat_psk2_sta_guest(self):

        res2gConn = setAdbPsk2StaConnRepeat(v.ANDROID_SERIAL_NUM, "normal", "guest", self.__class__.__name__)

        self.assertTrue(res2gConn, "Not all association were successful.")


class AP_SSIDHIDE_CHECK(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def ap_clear_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_clear_ssidhide_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'hidden': 1
        }

        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

    def ap_psk2_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_psk2_ssidhide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

    def ap_mixedpsk_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_mixedpsk_ssidhide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')


class AP_MIXEDPSK_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1,
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_BSD_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def ap_clear_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'none',
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

    def ap_psk2_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'psk2',
            'pwd': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

    def ap_mixedpsk_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

class AP_MUMIMO(TestCase):
    '''
    MU-MIMO 配置下发check，并检查sta是否能关联
    '''
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)
        ret3 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")
        if ret2 is False:
            raise Exception('Connection is failed. please check your remote settings.')
        if ret3 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def MUMIMO_check(self):
        mumimo = getMU_MIMO(self.dut2, "5g", self.__class__.__name__, v.DUT_MODULE)
        self.assertTrue(mumimo, "MU-MIMO should be Opened by Default")

        option = {
            'wifiIndex': 2,
            'txbf': 0
        }
        api.setMU_MIMO(self.dut, self.__class__.__name__, **option)
        mumimo2 = getMU_MIMO(self.dut2, "5g", self.__class__.__name__, v.DUT_MODULE)
        self.assertFalse(mumimo2, "MU-MIMO should be Closed When the Switch of Web is Off")

        option2 = {
            'wifiIndex': 2,
            'txbf': 3
        }
        api.setMU_MIMO(self.dut, self.__class__.__name__, **option2)
        mumimo3 = getMU_MIMO(self.dut2, "5g", self.__class__.__name__, v.DUT_MODULE)
        self.assertTrue(mumimo3, "MU-MIMO should be Opened When the Switch of Web is On")

    def assoc_noMUMIMO_5g(self):

        option = {
            'wifiIndex': 2,
            'txbf': 0
        }
        api.setMU_MIMO(self.dut, self.__class__.__name__, **option)

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

        option2 = {
            'wifiIndex': 2,
            'txbf': 3
        }
        api.setMU_MIMO(self.dut, self.__class__.__name__, **option2)


class AP_RELAY_STA_ONLINE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setDisableLanAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_clear_chan1_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)
        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_chan36_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
        }

        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk2_chan6_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'channel': v.CHANNEL6,
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_chan52_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'channel': v.CHANNEL52,
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_mixed_chan11_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL11
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_mixed_chan149_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL149
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_mixed_bw40_chan165_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_mixed_bw40_chan13_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '40'
        }

        api.setWifi(self.dut, self.__class__.__name__, **option2g)
        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_mixed_bw20_chan0_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_mixed_ssidspec_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SPECIAL_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.SPECIAL_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. SSID = %s" % v.SPECIAL_SSID)

    def assoc_mixed_ssidspec_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SPECIAL_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.SPECIAL_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. SSID = %s" % v.SPECIAL_SSID)

    def assoc_mixed_keyspec_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.SPECIAL_KEY
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. KEY = %s' % v.SPECIAL_KEY)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. KEY = %s" % v.SPECIAL_KEY)

    def assoc_mixed_keyspec_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.SPECIAL_KEY
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. KEY = %s' % v.SPECIAL_KEY)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. KEY = %s" % v.SPECIAL_KEY)

    def assoc_mixed_ssidchinese_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.CHINESE_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.CHINESE_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. SSID = %s" % v.CHINESE_SSID)

    def assoc_mixed_ssidchinese_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.CHINESE_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.CHINESE_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful. SSID = %s" % v.CHINESE_SSID)

    def assoc_ssidhide_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1,
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_ssidhide_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1,
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_CLEAR_LOW(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'min',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'min',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setDisableLanAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_CLEAR_MID(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setDisableLanAp(self.dut, self.__name__)

        self.dut.close()

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_CLEAR_HIGH(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'max',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'max',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setDisableLanAp(self.dut, self.__name__)

        self.dut.close()

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_CONFIG_CHECK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut2 = api.HttpClient()
        ret2 = self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret2 is False:
            raise Exception('Connection is failed for httpclient. please check your remote settings.')

        self.option2g = {
            'wifiIndex': 1,
            'on': "1",
            'ssid': v.SSID,
            'pwd': v.KEY,
            'encryption': 'mixed-psk',
            'channel': v.CHANNEL11,
            'bandwidth': '20',
            'hidden': "0",
            'txpwr': 'max'
        }

        self.option5g = {
            'wifiIndex': 2,
            'on': "1",
            'ssid': v.SSID_5G,
            'pwd': v.KEY,
            'encryption': 'psk2',
            'channel': v.CHANNEL149,
            'bandwidth': '40',
            'hidden': "0",
            'txpwr': 'min'
        }

        self.optionGuest = {
            'wifiIndex': 3,
            'on': "1",
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut2, self.__name__, **self.option2g)
        api.setWifi(self.dut2, self.__name__, **self.option5g)
        api.setWifi(self.dut2, self.__name__, **self.optionGuest)

        api.setLanAp(self.dut2, self.__name__)

        self.dut = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        if ret1 is False:
            raise Exception('Connection is failed for shell after setLanAp.')

    @classmethod
    def tearDownClass(self):
        self.dut.close()
        api.setDisableLanAp(self.dut2, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)
        self.dut2.close()

    def wan_port_belong_brlan(self):

        wanIfname = v.WAN_IFNAME.get(v.DUT_MODULE)
        wanInBrlan = wanIfInBrlan(self.dut, wanIfname, self.__class__.__name__)
        if v.DUT_MODULE not in ["R3P", "R3G"]:
            self.assertTrue(wanInBrlan, "wan port isnot in br-lan.")
        else:
            self.assertTrue(True)

    def wire_relay_ping_UpperRouter(self):

        resPingPercent = getPingStatus(self.dut, str(v.HOST_UPPER), v.PING_COUNT,
                                                  self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], 80,
                                        "WireRelayRouter Ping UpperRouter Failed.")

    def wire_relay_ping_internet(self):

        resPingPercent = getPingStatus(self.dut, str(v.PING_TARGET_WITHOUT_DNS), v.PING_COUNT,
                                                  self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], 80,
                                        "WireRelayRouter Ping internet Failed.")

    def wifi_config_check_2g(self):

        self.relay2g = api.getWifiDetailDic(self.dut2, self.__class__.__name__, "2g")

        self.assertDictEqual(self.relay2g, self.option2g,
                             msg="Normal router module switch over to wire relay module, wifi config should not be changed.")

    def wifi_config_check_5g(self):

        self.relay5g = api.getWifiDetailDic(self.dut2, self.__class__.__name__, "5g")
        self.assertDictEqual(self.relay5g, self.option5g,
                             msg="Normal router module switch over to wire relay module, wifi config should not be changed.")

    def wifi_config_check_guest(self):

        self.relayGuest = api.getWifiDetailDic(self.dut2, self.__class__.__name__, "guest")
        self.assertDictEqual(self.relayGuest, {}, msg="Wire relay module should not support guest wifi")

    def autochan_txpower_min_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def autochan_txpower_mid_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'mid',
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan1_txpower_max_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)

        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)
        if int(eval(v.CHANNEL1)) == chan_actually:
            pass
        else:
            self.fail("Channel 1 Setup failed.")

        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan6_txpower_min_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL6,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)

        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)
        if int(eval(v.CHANNEL6)) == chan_actually:
            pass
        else:
            self.fail("Channel 6 Setup failed.")

        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan11_txpower_mid_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL11,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)

        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)
        if int(eval(v.CHANNEL11)) == chan_actually:
            pass
        else:
            self.fail("Channel 11 Setup failed.")

        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan13_txpower_max_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL13,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)

        chan_actually = getWlanChannel(self.dut, "2g", self.__class__.__name__)
        if int(eval(v.CHANNEL13)) == chan_actually:
            pass
        else:
            self.fail("Channel 13 Setup failed.")

        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan36_txpower_min_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)

        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)
        if int(eval(v.CHANNEL36)) == chan_actually:
            pass
        else:
            self.fail("Channel 36 Setup failed.")

        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan52_txpower_mid_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL52,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)

        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)
        if int(eval(v.CHANNEL52)) == chan_actually:
            pass
        else:
            self.fail("Channel 52 Setup failed.")

        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan149_txpower_max_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL149,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)

        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)
        if int(eval(v.CHANNEL149)) == chan_actually:
            pass
        else:
            self.fail("Channel 149 Setup failed.")

        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan165_txpower_min_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL165,
            'txpwr': 'min',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)

        chan_actually = getWlanChannel(self.dut, "5g", self.__class__.__name__)
        if int(eval(v.CHANNEL165)) == chan_actually:
            pass
        else:
            self.fail("Channel 165 Setup failed.")

        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chanselection_2g(self):
        count = 0
        chan2g = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        while count < 5:
            api.setWifi(self.dut2, self.__class__.__name__, **option2g)
            channel = api.getWifiChannel(self.dut2, '2g', self.__class__.__name__)
            if channel not in chan2g:
                self.fail("Current auto-selected channel isnot between 1 and 11.")
            else:
                count += 1

    def chanselection_5g(self):
        count = 0
        chan5g = [149, 153, 157, 161]
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        while count < 5:
            api.setWifi(self.dut2, self.__class__.__name__, **option5g)
            channel = api.getWifiChannel(self.dut2, '5g', self.__class__.__name__)
            if channel not in chan5g:
                self.fail("Current auto-selected channel isnot between 149 and 161.")
            else:
                count += 1


class AP_RELAY_CLEAR_MID_TXPOWER(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut2 = api.HttpClient()
        ret2 = self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret2 is False:
            raise Exception('Connection is failed for httpclient. please check your remote settings.')

        api.setLanAp(self.dut2, self.__name__)

        self.dut = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        if ret1 is False:
            raise Exception('Connection is failed for shell after setLanAp.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)

        api.setDisableLanAp(self.dut2, self.__name__)
        
        self.dut.close()
        self.dut2.close()

    def autochan_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def autochan_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'mid',
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan1_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan6_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL6,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan11_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL11,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan13_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL13,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan36_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan52_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL52,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan149_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL149,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan165_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL165,
            'txpwr': 'mid',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")


class AP_RELAY_CLEAR_HIGH_TXPOWER(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut2 = api.HttpClient()
        ret2 = self.dut2.connect(host=v.HOST, password=v.WEB_PWD)
        if ret2 is False:
            raise Exception('Connection is failed for httpclient. please check your remote settings.')

        api.setLanAp(self.dut2, self.__name__)

        self.dut = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        if ret1 is False:
            raise Exception('Connection is failed for shell after setLanAp.')

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)

        api.setDisableLanAp(self.dut2, self.__name__)

        self.dut.close()
        self.dut2.close()

    def autochan_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def autochan_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'txpwr': 'max',
        }

        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan1_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan6_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL6,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan11_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL11,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan13_txpower_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL13,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option2g)
        power = getWlanTxPower(self.dut, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan36_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan52_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL52,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan149_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL149,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

    def chan165_txpower_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL165,
            'txpwr': 'max',
        }
        api.setWifi(self.dut2, self.__class__.__name__, **option5g)
        power = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")


class AP_RELAY_CLEAR_CHANSELECTION(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Http connection is failed. please check your remote settings.')

        api.setLanAp(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setDisableLanAp(self.dut, self.__name__)

        self.dut.close()

    def chanselection_2g(self):
        count = 0
        chan2g = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        while count < 10:
            api.setWifi(self.dut, self.__class__.__name__, **option2g)
            channel = api.getWifiChannel(self.dut, '2g', self.__class__.__name__)
            if channel not in chan2g:
                self.fail("Current auto-selected channel isnot between 1 and 11.")
            else:
                count += 1

    def chanselection_5g(self):
        count = 0
        chan5g = [149, 153, 157, 161]
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        while count < 10:
            api.setWifi(self.dut, self.__class__.__name__, **option5g)
            channel = api.getWifiChannel(self.dut, '5g', self.__class__.__name__)
            if channel not in chan5g:
                self.fail("Current auto-selected channel isnot between 149 and 161.")
            else:
                count += 1


class AP_RELAY_PSK2(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setDisableLanAp(self.dut, self.__name__)

        self.dut.close()

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_MIXEDPSK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_2g(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_MIXEDPSK_CHAN_BW80(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '80',
        }

        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_MIXEDPSK_CHAN_BW40(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '40'
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '40'
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_2g(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_RELAY_MIXEDPSK_CHAN_BW20(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '20'
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'bandwidth': '20'
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_2g(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_RELAY_MIXEDPSK_SSIDSPEC(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SPECIAL_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SPECIAL_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_ssidspec_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_ssidspec_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_ssidspec_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "spec", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_ssidspec_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "spec", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_ssidspec_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_ssidspec_5g(self):
        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_ssidspec_2g(self):
        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "spec", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_ssidspec_5g(self):
        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "spec", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_MIXEDPSK_KEYSPEC(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.SPECIAL_KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.SPECIAL_KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_keyspec_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_keyspec_5g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_keyspec_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_keyspec_5g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_keyspec_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_keyspec_5g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_keyspec_2g(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_keyspec_5g(self):

        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_RELAY_MIXEDPSK_SSIDCHINESE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.CHINESE_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.CHINESE_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_ssidchinese_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_ssidchinese_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_ssidchinese_2g(self):

        res2gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "chinese", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_ssidchinese_5g(self):

        res5gConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "chinese", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_ssidchinese_2g(self):

        res2gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_ssidchinese_5g(self):
        res5gConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_ssidchinese_2g(self):
        res2gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "chinese", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_ssidchinese_5g(self):
        res5gConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "chinese", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_BSD(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta(self):

        resConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        self.assertTrue(resConn, msg="Association wasnot successful.")

        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")
        resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertTrue(resConn2, msg="STA online Success, But doesnot associate with 5g")

    def assoc_psk2_near_field_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

        resConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        self.assertTrue(resConn, msg="Association wasnot successful.")

        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

        resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertTrue(resConn2, msg="STA online Success, But doesnot associate with 5g")


class AP_RELAY_MIXEDPSK_BSD_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")


class AP_RELAY_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        self.dut.close()

    def ap_clear_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_clear_ssidhide_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'hidden': 1
        }

        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

    def ap_psk2_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_psk2_ssidhide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

    def ap_mixedpsk_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_mixedpsk_ssidhide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')


class AP_RELAY_MIXEDPSK_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1,
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_2g(self):

        res2gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_5g(self):

        res5gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_2g(self):

        res2gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_5g(self):

        res5gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_2g(self):

        res2gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_5g(self):

        res5gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_RELAY_BSD_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)

        self.dut.close()

    def ap_clear_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'none',
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

    def ap_psk2_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'psk2',
            'pwd': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

    def ap_mixedpsk_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')


class AP_RELAY_WIFI_CHECK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        self.option2g = {
            'wifiIndex': 1,
            'on': "1",
            'ssid': v.SSID,
            'pwd': v.KEY,
            'encryption': 'mixed-psk',
            'channel': v.CHANNEL11,
            'bandwidth': '20',
            'hidden': "0",
            'txpwr': 'max'
        }

        self.option5g = {
            'wifiIndex': 2,
            'on': "1",
            'ssid': v.SSID_5G,
            'pwd': v.KEY,
            'encryption': 'psk2',
            'channel': v.CHANNEL149,
            'bandwidth': '40',
            'hidden': "0",
            'txpwr': 'min'
        }

        self.optionGuest = {
            'wifiIndex': 3,
            'on': "1",
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **self.option2g)
        api.setWifi(self.dut, self.__name__, **self.option5g)
        api.setWifi(self.dut, self.__name__, **self.optionGuest)
        api.setLanAp(self.dut, self.__name__)

        self.relay2g = api.getWifiDetailDic(self.dut, self.__name__, "2g")
        self.relay5g = api.getWifiDetailDic(self.dut, self.__name__, "5g")
        self.relayGuest = api.getWifiDetailDic(self.dut, self.__name__, "guest")

        api.setDisableLanAp(self.dut, self.__name__)

        self.router2g = api.getWifiDetailDic(self.dut, self.__name__, "2g")
        self.router5g = api.getWifiDetailDic(self.dut, self.__name__, "5g")
        self.routerGuest = api.getWifiDetailDic(self.dut, self.__name__, "guest")

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def config_check_2g(self):

        self.assertDictEqual(self.relay2g, self.option2g,
                             msg="Normal router module switch over to wire relay module, wifi config should not be changed.")
        self.assertDictEqual(self.router2g, self.option2g,
                             msg="Wire relay module switch back to normal router module, wifi config should not be changed.")

    def config_check_5g(self):

        self.assertDictEqual(self.relay5g, self.option5g,
                             msg="Normal router module switch over to wire relay module, wifi config should not be changed.")
        self.assertDictEqual(self.router5g, self.option5g,
                             msg="Wire relay module switch back to normal router module, wifi config should not be changed.")

    def config_check_guest(self):

        # when wire relay module switch back to normal router module, guest wifi is turned off
        self.optionGuest["on"] = "0"
        self.assertDictEqual(self.relayGuest, {}, msg="Wire relay module should not support guest wifi")
        self.assertDictEqual(self.routerGuest, self.optionGuest,
                             msg="Wire relay switch back to normal router module, guest wifi should be turned off.")

class AP_RELAY_CONFIG_SYNC(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")
        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        self.dut2 = api.HttpClient()
        ret3 = self.dut2.connect(host=v.HOST_UPPER, password=v.WEB_PWD_UPPER)
        if ret3 is False:
            raise Exception("Http connection To Upper Router is failed after setLanAp")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__name__, **option2g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

    @classmethod
    def tearDownClass(self):

        api.setDisableLanAp(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

        self.dut.close()
        self.dut2.close()

    def assoc_blacklist_sync(self):
        # sta in blacklist
        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut2, self.__class__.__name__, **option)
        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        # sta out of blacklist
        option = {
            'model': 0,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut2, self.__class__.__name__, **option)
        api.setWifiMacFilter(self.dut2, self.__class__.__name__)
        res2gConn2 = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertFalse(res2gConn, "Sta in Upper Router Blacklist, But Online wireRelay Router.")
        self.assertTrue(res2gConn2, "Upper Router Blacklist Deleted, Sta Online wireRelay Router Failed.")

    def assoc_whitelist_sync(self):
        # sta out of whitelist
        option = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 0
        }
        api.setEditDevice(self.dut2, self.__class__.__name__, **option)
        # option2 = {
        #     'model': 1,
        #     'enable': 1
        # }
        # api.setWifiMacFilter(self.dut2, self.__class__.__name__, **option2)
        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        # sta in whitelist
        option3 = {
            'model': 1,
            'mac': self.staMac,
            'option': 0
        }
        api.setEditDevice(self.dut2, self.__class__.__name__, **option3)
        # api.setWifiMacFilter(self.dut2, self.__class__.__name__, **option2)
        res2gConn2 = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        # delete and turnoff whitelist
        option4 = {
            'model': 1,
            'mac': '11:22:33:44:55:66',
            'option': 1
        }
        api.setEditDevice(self.dut2, self.__class__.__name__, **option4)
        option5 = {
            'model': 1,
            'mac': self.staMac,
            'option': 1
        }
        api.setEditDevice(self.dut2, self.__class__.__name__, **option5)
        option6 = {
            'model': 1,
            'enable': 0
        }
        api.setWifiMacFilter(self.dut2, self.__class__.__name__, **option6)
        res2gConn3 = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        self.assertFalse(res2gConn, "Sta not in Upper Router Whitelist, But Online wireRelay Router.")
        self.assertTrue(res2gConn2, "Sta in Upper Router Whitelist, But Online wireRelay Router Failed.")
        self.assertTrue(res2gConn3, "Upper Router Whitelist Turned off, Sta Online wireRelay Router Failed.")


class AP_QOS_MIXEDPSK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

        optionQos = {
            'mac': self.staMac,
            'upload': v.QOS_MAXUP,
            'download': v.QOS_MAXDOWN,
        }

        api.setQosBand(self.dut, self.__name__)
        api.setQosSwitch(self.dut, self.__name__)
        api.setMACQoSInfo(self.dut, self.__name__, **optionQos)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        api.setMACQosOff(self.dut, self.__name__)
        optionQosSwitch = {
            'on': 0,
        }
        api.setQosSwitch(self.dut, self.__name__, **optionQosSwitch)

        self.dut.close()

    def assoc_psk2_sta_speedtest_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.5,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.5,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_speedtest_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.5,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.5,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_speedtest_2g(self):

        res2gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_speedtest_5g(self):

        res5gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_speedtest_2g(self):

        res2gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_speedtest_5g(self):

        res5gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_speedtest_2g(self):

        res2gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_speedtest_5g(self):

        res5gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_QOS_CLEAR(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

        optionQos = {
            'mac': self.staMac,
            'upload': v.QOS_MAXUP,
            'download': v.QOS_MAXDOWN,
        }

        api.setQosSwitch(self.dut, self.__name__)
        api.setMACQoSInfo(self.dut, self.__name__, **optionQos)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        optionQosSwitch = {
            'on': 0,
        }
        api.setQosSwitch(self.dut, self.__name__, **optionQosSwitch)

        self.dut.close()

    def assoc_clear_sta_speedtest_2g(self):

        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_clear_sta_speedtest_5g(self):

        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_QOS_PSK2(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

        optionQos = {
            'mac': self.staMac,
            'upload': v.QOS_MAXUP,
            'download': v.QOS_MAXDOWN,
        }

        api.setQosSwitch(self.dut, self.__name__)
        api.setMACQoSInfo(self.dut, self.__name__, **optionQos)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        optionQosSwitch = {
            'on': 0,
        }
        api.setQosSwitch(self.dut, self.__name__, **optionQosSwitch)

        self.dut.close()

    def assoc_psk2_sta_speedtest_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_speedtest_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], v.QOS_MAXDOWN * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], v.QOS_MAXDOWN))
                self.assertLessEqual(speedTestRes['up'], v.QOS_MAXUP * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (speedTestRes['up'], v.QOS_MAXUP))
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_QOS_GUEST_MIXEDPSK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)
        api.setQosBand(self.dut, self.__name__)
        api.setQosSwitch(self.dut, self.__name__)

        optionGuestQos = {
            'percent': 0.02,
            'percent_up': 0.02,
        }

        self.guestQos = api.setQosGuest2(self.dut, self.__name__, **optionGuestQos)

    @classmethod
    def tearDownClass(self):

        api.setQosGuest2(self.dut, self.__name__)
        optionQosSwitch = {
            'on': 0
        }

        api.setQosSwitch(self.dut, self.__name__, **optionQosSwitch)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_psk2_sta_speedtest_guest(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.GUEST_SSID, v.KEY, "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], self.guestQos['guest']['down'] * 1.5,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], self.guestQos['guest']['down']))
                self.assertLessEqual(speedTestRes['up'], self.guestQos['guest']['up'] * 1.5,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (
                                         speedTestRes['up'], self.guestQos['guest']['up']))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_speedtest_guest(self):

        res2gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.GUEST_SSID, v.KEY, "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], self.guestQos['guest']['down'] * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], self.guestQos['guest']['down']))
                self.assertLessEqual(speedTestRes['up'], self.guestQos['guest']['up'] * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (
                                         speedTestRes['up'], self.guestQos['guest']['up']))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_speedtest_guest(self):

        res2gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.GUEST_SSID, v.KEY, "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], self.guestQos['guest']['down'] * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], self.guestQos['guest']['down']))
                self.assertLessEqual(speedTestRes['up'], self.guestQos['guest']['up'] * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (
                                         speedTestRes['up'], self.guestQos['guest']['up']))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_speedtest_guest(self):

        res2gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.GUEST_SSID, v.KEY, "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speedTestRes = getAdbOoklaSpeedTestResult(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
                self.assertLessEqual(speedTestRes['down'], self.guestQos['guest']['down'] * 1.1,
                                     "Downlink rate %s KB/s exceed maxdown %s KB/s" % (
                                         speedTestRes['down'], self.guestQos['guest']['down']))
                self.assertLessEqual(speedTestRes['up'], self.guestQos['guest']['up'] * 1.1,
                                     "Uplink rate %s KB/s exceed maxup %s KB/s" % (
                                         speedTestRes['up'], self.guestQos['guest']['up']))
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

class AP_QOS_ROUTERSELF(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")
        if ret2 is False:
            raise Exception("Connection is failed. please check your remote settings.")

        api.setQosBand(self.dut, self.__name__)
        api.setQosSwitch(self.dut, self.__name__)

        optionRouterSelf = {
            'percent': 0.05,
            'percent_up': 0.05,
        }

        self.routerSelfQos = api.setQosRouterSelf(self.dut, self.__name__, **optionRouterSelf)

    @classmethod
    def tearDownClass(self):

        api.setQosRouterSelf(self.dut, self.__name__)
        optionQosSwitch = {
            'on': 0
        }
        api.setQosSwitch(self.dut, self.__name__, **optionQosSwitch)

        self.dut.close()
        self.dut2.close()

    def routerSelf_speedtest(self):

        xqSpeedDown = getRouterSpeedtest(self.dut2, "down", self.__class__.__name__)
        xqSpeedUp = getRouterSpeedtest(self.dut2, "up", self.__class__.__name__)

        if xqSpeedDown == None or xqSpeedUp == None:
            self.fail(msg='RouterSelf Speedtest failed')
        else:
            self.assertLessEqual(xqSpeedDown, self.routerSelfQos['local']['down'] * 1.5,
                            "RouterSelf Downlink rate %s Mb/s exceed maxdown %s Mb/s" % (
                            xqSpeedDown, self.routerSelfQos['local']['down']))
            self.assertLessEqual(xqSpeedUp, self.routerSelfQos['local']['up'] * 1.5,
                            "RouterSelf Uplink rate %s Mb/s exceed maxup %s Mb/s" % (
                            xqSpeedUp, self.routerSelfQos['local']['up']))


class AP_WIRELESS_RELAY_MIXEDPSK_KEYSPEC(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            # 'encryption': 'WPA2PSK',
            # 'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            # 'channel': v.ROOT_AP_CHANNEL,
            # 'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_SSID,
            'nencryption': 'mixed-psk',
            'npassword': v.SPECIAL_KEY,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableAp(self.dut, self.__name__)

        self.dut.close()

    def assoc_psk2_sta_keyspec_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID, v.SPECIAL_KEY, "2g",
                                  self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_keyspec_5g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID_5G, v.SPECIAL_KEY, "5g",
                                  self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_keyspec_2g(self):

        res2gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID, v.SPECIAL_KEY, "2g",
                                 self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_keyspec_5g(self):

        res2gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID_5G, v.SPECIAL_KEY, "5g",
                                 self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_keyspec_2g(self):

        res2gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID, v.SPECIAL_KEY, "2g",
                                      self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_keyspec_5g(self):

        res2gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID_5G, v.SPECIAL_KEY, "5g",
                                      self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_keyspec_2g(self):

        res2gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID, v.SPECIAL_KEY, "2g",
                                     self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_keyspec_5g(self):

        res2gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID_5G, v.SPECIAL_KEY, "5g",
                                     self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_WIRELESS_RELAY_MIXEDPSK_SSIDCHINESE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            # 'encryption': 'WPA2PSK',
            # 'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            # 'channel': v.ROOT_AP_CHANNEL,
            # 'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_CHINESE_SSID,
            'nencryption': 'mixed-psk',
            'npassword': v.KEY,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableAp(self.dut, self.__name__)

        self.dut.close()

    def assoc_psk2_sta_ssidchinese_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID, v.KEY, "2g",
                                  self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_ssidchinese_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID_5G, v.KEY, "5g",
                                  self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_ssidchinese_2g(self):

        res2gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID, v.KEY, "2g",
                                 self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_ssidchinese_5g(self):

        res5gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID_5G, v.KEY, "5g",
                                 self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_ssidchinese_2g(self):

        res2gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID, v.KEY, "2g",
                                      self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_ssidchinese_5g(self):
        res5gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID_5G, v.KEY, "5g",
                                      self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_ssidchinese_2g(self):
        res2gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID, v.KEY, "2g",
                                     self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_ssidchinese_5g(self):
        res5gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_CHINESE_SSID_5G, v.KEY, "5g",
                                     self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

class AP_WIRELESS_RELAY_CLEAR_CHANSELECTION(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception('Http connection is failed. please check your remote settings.')

        option = {
            'ssid': v.ROOT_AP_SSID,
            # 'encryption': 'WPA2PSK',
            # 'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            # 'channel': v.ROOT_AP_CHANNEL,
            # 'bandwidth': '20',
            'nssid': v.SSID,
            'nencryption': 'WPA2PSK',
            'npassword': v.ROOT_AP_PWD,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableAp(self.dut, self.__name__)

        self.dut.close()

    def chanselection_2g(self):
        count = 0
        chan2g = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        while count < 10:
            api.setWifi(self.dut, self.__class__.__name__, **option2g)
            channel = api.getWifiChannel(self.dut, '2g', self.__class__.__name__)
            if channel not in chan2g:
                self.fail("Current auto-selected channel isnot between 1 and 11.")
            else:
                count += 1

    def chanselection_5g(self):
        count = 0
        chan5g = [149, 153, 157, 161]
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        while count < 10:
            api.setWifi(self.dut, self.__class__.__name__, **option5g)
            channel = api.getWifiChannel(self.dut, '5g', self.__class__.__name__)
            if channel not in chan5g:
                self.fail("Current auto-selected channel isnot between 149 and 161.")
            else:
                count += 1

class AP_WIRELESS_RELAY_MIXEDPSK_BSD(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            'encryption': 'WPA2PSK',
            'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            'channel': v.ROOT_AP_CHANNEL,
            'bandwidth': '20',
            'nssid': v.SSID,
            'nencryption': 'WPA2PSK',
            'npassword': v.ROOT_AP_PWD,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableAp(self.dut, self.__name__)

        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")


class AP_WIRELESS_RELAY_MIXEDPSK_BSD_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            'encryption': 'WPA2PSK',
            'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            'channel': v.ROOT_AP_CHANNEL,
            'bandwidth': '20',
            'nssid': v.SSID,
            'nencryption': 'WPA2PSK',
            'npassword': v.ROOT_AP_PWD,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd1': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableAp(self.dut, self.__name__)

        api.setAllWifi(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_psk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk2_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")

    def assoc_tkippsk_near_field_sta(self):
        count = 0
        while count <= 1:
            resConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
            resConn2 = chkAdb5gFreq(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if resConn and resConn2:
                break
            else:
                resConn2 = False
            count += 1

        self.assertTrue(resConn, msg="Association wasnot successful.")
        self.assertTrue(resConn2, msg="STA doesnot associate with 5g")
        result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
        self.assertIsNot(result['ip'], "", msg='no ip address got.')
        resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT, self.__class__.__name__)
        self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                "Ping responsed percent werenot good enough.")


class AP_WIRELESS_RELAY_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            # 'encryption': 'WPA2PSK',
            # 'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            # 'channel': v.ROOT_AP_CHANNEL,
            # 'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_SSID,
            'nencryption': 'WPA2PSK',
            'npassword': v.ROOT_AP_PWD,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableAp(self.dut, self.__name__)

        self.dut.close()

    def ap_clear_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SSID, self.__class__.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_clear_ssidhide_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'hidden': 1
        }

        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SSID_5G, self.__class__.__name__)

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

    def ap_psk2_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SSID, self.__class__.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_psk2_ssidhide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SSID_5G, self.__class__.__name__)

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

    def ap_mixedpsk_ssidhide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        ret2g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SSID, self.__class__.__name__)

        option2g = {
            'wifiIndex': 1,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)

        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden..')

    def ap_mixedpsk_ssidhide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        ret5g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SSID_5G, self.__class__.__name__)

        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)

        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')


class AP_WIRELESS_RELAY_BSD_SSIDHIDE(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            'encryption': 'WPA2PSK',
            'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            'channel': v.ROOT_AP_CHANNEL,
            'bandwidth': '20',
            'nssid': v.SSID,
            'nencryption': 'WPA2PSK',
            'npassword': v.ROOT_AP_PWD,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        api.setDisableAp(self.dut, self.__name__)

        self.dut.close()

    def ap_clear_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'none',
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

    def ap_psk2_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'psk2',
            'pwd': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')

    def ap_mixedpsk_ssidhide(self):
        option = {
            'bsd': 1,
            'ssid1': v.SSID,
            'encryption1': 'mixed-psk',
            'pwd': v.KEY,
            'hidden1': 1,
        }
        api.setAllWifi(self.dut, self.__class__.__name__, **option)

        ret = setAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)

        api.setAllWifi(self.dut, self.__class__.__name__)

        if ret is False:
            self.fail(msg='ssid should be hidden when bsd is on')


class AP_WIRELESS_RELAY_CONFIG_CHECK(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        self.option2g = {
            'wifiIndex': 1,
            'on': "1",
            'ssid': v.SSID,
            'pwd': v.KEY,
            'encryption': 'mixed-psk',
            'channel': v.CHANNEL11,
            'bandwidth': '20',
            'hidden': "0",
            'txpwr': 'max'
        }

        self.option5g = {
            'wifiIndex': 2,
            'on': "1",
            'ssid': v.SSID_5G,
            'pwd': v.KEY,
            'encryption': 'psk2',
            'channel': v.CHANNEL149,
            'bandwidth': '40',
            'hidden': "0",
            'txpwr': 'min'
        }

        self.optionGuest = {
            'wifiIndex': 3,
            'on': "1",
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **self.option2g)
        api.setWifi(self.dut, self.__name__, **self.option5g)
        api.setWifi(self.dut, self.__name__, **self.optionGuest)

        option = {
            'ssid': v.ROOT_AP_SSID,
            # 'encryption': 'WPA2PSK',
            # 'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            # 'channel': v.ROOT_AP_CHANNEL,
            # 'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_SSID,
            'nencryption': 'WPA2PSK',
            'npassword': v.ROOT_AP_PWD,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

        self.relayConfGuest = api.getWifiDetailDic(self.dut, self.__name__, "guest")

        api.setDisableAp(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def config_check_2g(self):
        routerConf2g = api.getWifiDetailDic(self.dut, self.__class__.__name__, "2g")

        self.assertDictEqual(routerConf2g, self.option2g,
                             msg="Wireless relay module switch back to normal router module, wifi config should not be changed.")

    def config_check_5g(self):
        routerConf5g = api.getWifiDetailDic(self.dut, self.__class__.__name__, "5g")

        self.assertDictEqual(routerConf5g, self.option5g,
                             msg="Wireless relay module switch back to normal router module, wifi config should not be changed.")

    def config_check_guest(self):
        routerConfGuest = api.getWifiDetailDic(self.dut, self.__class__.__name__, "guest")

        self.optionGuest["on"] = "0"
        self.assertDictEqual(self.relayConfGuest, {}, msg="Wireless relay module should not support guest wifi")
        self.assertDictEqual(routerConfGuest, self.optionGuest,
                             msg="Wireless relay switch back to normal router module, guest wifi should be turned off.")


class AP_WIRELESS_RELAY_2G(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        if ret is False:
            raise Exception("Http connection is failed. please check your remote settings.")
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        self.option2g = {
            'wifiIndex': 1,
            'on': "1",
            'ssid': v.SSID,
            'pwd': v.KEY,
            'encryption': 'mixed-psk',
            'channel': v.CHANNEL11,
            'bandwidth': '40',
            'hidden': "0",
            'txpwr': 'min'
        }

        self.option5g = {
            'wifiIndex': 2,
            'on': "1",
            'ssid': v.SSID_5G,
            'pwd': v.KEY,
            'encryption': 'psk2',
            'channel': v.CHANNEL149,
            'bandwidth': '40',
            'hidden': "0",
            'txpwr': 'max'
        }

        self.optionGuest = {
            'wifiIndex': 3,
            'on': "1",
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **self.option2g)
        api.setWifi(self.dut, self.__name__, **self.option5g)
        api.setWifi(self.dut, self.__name__, **self.optionGuest)

        self.UpperOption = {
            'ssid': v.WIRELESS_2G_RELAY_UPPER_SSID,
            'encryption': '',
            'enctype': '',
            'password': v.WIRELESS_2G_RELAY_UPPER_PW,
            'channel': '',
            'band': ''
        }
        res, wifiInfo = api.chkWifiInfo(self.dut, self.__name__, **self.UpperOption)
        if res is False:
            raise Exception('UpperRouter SSID isnot in ScanList, WirelessRelay TestCase Break')

        for item in self.UpperOption.keys():
            if item in wifiInfo.keys():
                self.UpperOption[item] = wifiInfo[item]

        dut3 = ShellClient(v.CONNECTION_TYPE)
        ret3 = dut3.connect(v.HOST, v.USR, v.PASSWD)
        if ret3 is False:
            raise Exception('Connection is failed for shell.')
        shutdownWan(dut3, v.WAN_IFNAME.get(v.DUT_MODULE), self.__name__)
        dut3.close()

        self.result = api.setWifiAp(self.dut, self.__name__, **self.UpperOption)
        if self.result is None:
            raise Exception('Connect to specified wifi return None, Break')
        if self.result['code'] != 0:
            raise Exception('Failed to connect to specified wifi, Please check your password')

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)
        if ret1 is False:
            raise Exception('Connection is failed for shell after setWifiAp.')

    @classmethod
    def tearDownClass(self):

        self.dut2.close()
        api.setDisableAp(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def wifiRelay_switchCheck_2g(self):

        apcli0 = getWifiRelayStatus(self.dut2, "2g", self.__class__.__name__)
        self.assertTrue(apcli0, 'The device is in wireless relay mode, but the connection to the parent wifi fails')

    def config_check_5g(self):
        relayConf5g = api.getWifiDetailDic(self.dut, self.__class__.__name__, "5g")
        self.assertDictEqual(relayConf5g, self.option5g,
                             msg="Switch to 2.4g Wireless relay ,5g wifi config should not changed.")

    def config_check_guest(self):

        relayConfGuest = api.getWifiDetailDic(self.dut, self.__class__.__name__, "guest")
        self.assertDictEqual(relayConfGuest, {}, msg="2.4g Wireless relay mode should not support guest wifi")

    def config_check_2g(self):
        routerConf2g = api.getWifiDetailDic(self.dut, self.__class__.__name__, "2g")
        self.assertEqual(routerConf2g['on'], self.option2g['on'],
                             msg="Switch to 2.4g Wireless relay ,2g wifi is down.")
        self.assertEqual(routerConf2g['ssid'], self.option2g['ssid'],
                             msg="Switch to 2.4g Wireless relay ,2g wifi ssid changed.")
        self.assertEqual(routerConf2g['encryption'], self.option2g['encryption'],
                             msg="Switch to 2.4g Wireless relay ,2g wifi encryption changed.")

        power = getWlanTxPower(self.dut2, "2g", self.__class__.__name__)
        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015
        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Switch to 2.4g Wireless relay ,2g wifi txpower isnot max.")

    def assoc_afterModeChange_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_afterModeChange_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_ch36Clr_txMin_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
            'channel': v.CHANNEL36,
            'txpwr': 'min',
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        t.sleep(20)
        chan_actually = getWlanChannel(self.dut2, "5g", self.__class__.__name__)
        if int(eval(v.CHANNEL36)) == chan_actually:
            pass
        else:
            self.fail("Channel 36 Setup failed.")

        power = getWlanTxPower(self.dut2, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

        res5gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_ch52Psk2BW40_txMid_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'channel': v.CHANNEL52,
            'txpwr': 'mid',
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        t.sleep(20)
        chan_actually = getWlanChannel(self.dut2, "5g", self.__class__.__name__)
        if int(eval(v.CHANNEL52)) == chan_actually:
            pass
        else:
            self.fail("Channel 52 Setup failed.")

        power = getWlanTxPower(self.dut2, "5g", self.__class__.__name__)

        minPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower5GL.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_ch165Mixd_txMax_5g(self):

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL165,
            'txpwr': 'max',
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        t.sleep(20)
        chan_actually = getWlanChannel(self.dut2, "5g", self.__class__.__name__)
        if int(eval(v.CHANNEL165)) == chan_actually:
            pass
        else:
            self.fail("Channel 165 Setup failed.")

        power = getWlanTxPower(self.dut2, "5g", self.__class__.__name__)

        minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_ssidSpecHide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SPECIAL_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)
        t.sleep(20)
        ret2g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SPECIAL_SSID, self.__class__.__name__)
        if ret2g is False:
            self.fail(msg='2.4g wifi is not hidden.')

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.SPECIAL_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association Special&Hidden SSID failed. SSID = %s" % v.SPECIAL_SSID)

    def assoc_ssidChineseHide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.CHINESE_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        t.sleep(20)
        ret5g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.CHINESE_SSID_5G, self.__class__.__name__)
        if ret5g is False:
            self.fail(msg='5g wifi is not hidden..')

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.CHINESE_SSID_5G)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association Chinese&Hidden SSID failed. SSID = %s" % v.CHINESE_SSID_5G)


class AP_WIRELESS_RELAY_5G(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        if ret is False:
            raise Exception("Http connection is failed. please check your remote settings.")
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        self.option2g = {
            'wifiIndex': 1,
            'on': "1",
            'ssid': v.SSID,
            'pwd': v.KEY,
            'encryption': 'psk2',
            'channel': v.CHANNEL13,
            'bandwidth': '40',
            'hidden': "0",
            'txpwr': 'max'
        }

        self.option5g = {
            'wifiIndex': 2,
            'on': "1",
            'ssid': v.SSID_5G,
            'pwd': v.KEY,
            'encryption': 'mixed-psk',
            'channel': v.CHANNEL36,
            'bandwidth': '20',
            'hidden': "0",
            'txpwr': 'min'
        }

        self.optionGuest = {
            'wifiIndex': 3,
            'on': "1",
            'ssid': v.GUEST_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **self.option2g)
        api.setWifi(self.dut, self.__name__, **self.option5g)
        api.setWifi(self.dut, self.__name__, **self.optionGuest)

        self.UpperOption = {
            'ssid': v.WIRELESS_5G_RELAY_UPPER_SSID,
            'encryption': '',
            'enctype': '',
            'password': v.WIRELESS_5G_RELAY_UPPER_PW,
            'channel': '',
            'band': ''
        }
        res, wifiInfo = api.chkWifiInfo(self.dut, self.__name__, **self.UpperOption)
        if res is False:
            raise Exception('UpperRouter SSID isnot in ScanList, WirelessRelay TestCase Break')

        for item in self.UpperOption.keys():
            if item in wifiInfo.keys():
                self.UpperOption[item] = wifiInfo[item]

        dut3 = ShellClient(v.CONNECTION_TYPE)
        ret3 = dut3.connect(v.HOST, v.USR, v.PASSWD)
        if ret3 is False:
            raise Exception('Connection is failed for shell.')
        shutdownWan(dut3, v.WAN_IFNAME.get(v.DUT_MODULE), self.__name__)
        dut3.close()

        self.result = api.setWifiAp(self.dut, self.__name__, **self.UpperOption)
        if self.result is None:
            raise Exception('Connect to specified wifi return None, Break')
        if self.result['code'] != 0:
            raise Exception('Failed to connect to specified wifi, Please check your password')

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)
        if ret1 is False:
            raise Exception('Connection is failed for shell after setWifiAp.')

    @classmethod
    def tearDownClass(self):

        self.dut2.close()
        api.setDisableAp(self.dut, self.__name__)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def wifiRelay_switchCheck_5g(self):

        apclii0 = getWifiRelayStatus(self.dut2, "5g", self.__class__.__name__)
        self.assertTrue(apclii0, 'The device is in wireless relay mode, but the connection to the parent wifi fails')

    def config_check_2g(self):
        relayConf2g = api.getWifiDetailDic(self.dut, self.__class__.__name__, "2g")
        self.assertDictEqual(relayConf2g, self.option2g,
                             msg="Switch to 5g Wireless relay ,2g wifi config should not changed.")

    def config_check_guest(self):

        relayConfGuest = api.getWifiDetailDic(self.dut, self.__class__.__name__, "guest")
        self.assertDictEqual(relayConfGuest, {}, msg="5g Wireless relay mode should not support guest wifi")

    def config_check_5g(self):
        routerConf5g = api.getWifiDetailDic(self.dut, self.__class__.__name__, "5g")
        self.assertEqual(routerConf5g['on'], self.option5g['on'],
                             msg="Switch to 5g Wireless relay ,5g wifi is down.")
        self.assertEqual(routerConf5g['ssid'], self.option5g['ssid'],
                             msg="Switch to 5g Wireless relay ,5g wifi ssid changed.")
        self.assertEqual(routerConf5g['encryption'], self.option5g['encryption'],
                             msg="Switch to 5g Wireless relay ,5g wifi encryption changed.")

        power = getWlanTxPower(self.dut2, "5g", self.__class__.__name__)

        if self.UpperOption['channel'] >= 100:
            minPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 0.985
            maxPower = data.txPower5GH.get(v.DUT_MODULE)[2] * 1.015
        else:
            minPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 0.985
            maxPower = data.txPower5GL.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Switch to 5g Wireless relay ,5g wifi txpower isnot max.")

    def assoc_afterModeChange_2g(self):

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_afterModeChange_5g(self):

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_ch1Clr_txMin_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
            'channel': v.CHANNEL1,
            'txpwr': 'min',
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)
        t.sleep(10)
        chan_actually = getWlanChannel(self.dut2, "2g", self.__class__.__name__)
        if int(eval(v.CHANNEL1)) == chan_actually:
            pass
        else:
            self.fail("Channel 1 Setup failed.")

        power = getWlanTxPower(self.dut2, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[0] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[0] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

        res2gConn = setAdbClearStaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_ch6Psk2BW40_txMid_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'psk2',
            'pwd': v.KEY,
            'channel': v.CHANNEL6,
            'txpwr': 'mid',
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)
        t.sleep(10)
        chan_actually = getWlanChannel(self.dut2, "2g", self.__class__.__name__)
        if int(eval(v.CHANNEL6)) == chan_actually:
            pass
        else:
            self.fail("Channel 6 Setup failed.")

        power = getWlanTxPower(self.dut2, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[1] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[1] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_ch13keySpec_txMax_2g(self):

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.SPECIAL_KEY,
            'channel': v.CHANNEL13,
            'txpwr': 'max',
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)
        t.sleep(10)
        chan_actually = getWlanChannel(self.dut2, "2g", self.__class__.__name__)
        if int(eval(v.CHANNEL13)) == chan_actually:
            pass
        else:
            self.fail("Channel 13 Setup failed.")

        power = getWlanTxPower(self.dut2, "2g", self.__class__.__name__)

        minPower = data.txPower2G.get(v.DUT_MODULE)[2] * 0.985
        maxPower = data.txPower2G.get(v.DUT_MODULE)[2] * 1.015

        if minPower <= power <= maxPower:
            pass
        else:
            self.fail("Txpower isnot correct.")

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "normal", "2g", self.__class__.__name__, key="spec")
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. KEY = %s' % v.SPECIAL_KEY)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful. KEY = %s" % v.SPECIAL_KEY)


    def assoc_ssidSpecHide_5g(self):
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SPECIAL_SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option5g)
        t.sleep(10)
        ret5g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.SPECIAL_SSID_5G, self.__class__.__name__)
        if ret5g is False:
            self.fail(msg='5g wifi is not hidden.')

        res5gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "spec", "5g", self.__class__.__name__)
        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.SPECIAL_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res5gConn, "Association Special&Hidden SSID failed. SSID = %s" % v.SPECIAL_SSID_5G)

    def assoc_ssidChineseHide_2g(self):
        option2g = {
            'wifiIndex': 1,
            'ssid': v.CHINESE_SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'hidden': 1
        }
        api.setWifi(self.dut, self.__class__.__name__, **option2g)
        t.sleep(10)
        ret2g = chkAdbScanSsidNoExist(v.ANDROID_SERIAL_NUM, v.CHINESE_SSID, self.__class__.__name__)
        if ret2g is False:
            self.fail(msg='2g wifi is not hidden..')

        res2gConn = setAdbPsk2StaConn(v.ANDROID_SERIAL_NUM, "chinese", "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got. SSID = %s' % v.CHINESE_SSID)
            else:
                resPingPercent = getAdbPingStatus(v.ANDROID_SERIAL_NUM, v.PING_TARGET, v.PING_COUNT,
                                                  self.__class__.__name__)
                self.assertGreaterEqual(resPingPercent['pass'], v.PING_PERCENT_PASS,
                                        "Ping responsed percent werenot good enough.")
        else:
            self.assertTrue(res2gConn, "Association Chinese&Hidden SSID failed. SSID = %s" % v.CHINESE_SSID)


class AP_MIXEDPSK_WEB_ACCESS(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()

        option = {
            'open': 1,
            'opt': 0,
            'mac': self.staMac,
        }

        api.setWebAccessOpt(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        option = {
            'open': 0,
        }

        api.setWebAccessOpt(self.dut, self.__name__, **option)

        self.dut.close()

    def assoc_psk2_sta_access_web_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk_sta_access_web_2g(self):
        res2gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_access_web_2g(self):
        res2gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_access_web_2g(self):
        res2gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")

    def assoc_psk2_sta_access_web_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_psk_sta_access_web_5g(self):
        res5gConn = setAdbPskSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk2_sta_access_web_5g(self):
        res5gConn = setAdbTkipPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")

    def assoc_tkippsk_sta_access_web_5g(self):
        res5gConn = setAdbTkipPskSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res5gConn:
            ret1 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 1,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)

            ret2 = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL, self.__class__.__name__)

            option = {
                'open': 1,
                'opt': 0,
                'mac': self.staMac,
            }

            api.setWebAccessOpt(self.dut, self.__class__.__name__, **option)
            if ret1 is False:
                self.fail("STA in whitelist should be allowed access web")
            self.assertFalse(ret2, "STA out of whitelist should not be allowed access web")
        else:
            self.assertTrue(res5gConn, "Association wasnot successful.")


class AP_CLEAR_CHAN1_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN6_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN11_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN13_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN1_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN6_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN11_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN13_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN1_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN6_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN11_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN13_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN1_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN6_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN11_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN13_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN165_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN44_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL44,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN60_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL60,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN157_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW80_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW80_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW80_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN165_BW20_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN44_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL44,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN60_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL60,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN157_BW40_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW80_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW80_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW80_DUT_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        self.dut2 = ShellClient(v.CONNECTION_TYPE)
        ret3 = self.dut2.connect(v.HOST, v.USR, v.PASSWD)

        if ret3 is False:
            raise Exception('Connection is failed. please check your remote settings.')

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.dut2.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(4.0)
            ret = setIperfFlow2(self.dut2, result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN1_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN6_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN11_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN13_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN1_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN6_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN11_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN13_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN1_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN6_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN11_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN13_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN1_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN6_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN11_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN13_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN165_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN44_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL44,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN60_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL60,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN157_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW80_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW80_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW80_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN165_BW20_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN44_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL44,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN60_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL60,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN157_BW40_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW80_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW80_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW80_LAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow(result["ip"], v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)
            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN1_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN6_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN11_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN13_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN1_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN6_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN11_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN13_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN1_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN6_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN11_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN13_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN1_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN6_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN11_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN13_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL13,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN165_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'bandwidth': '20'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN44_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL44,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN60_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL60,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN157_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'bandwidth': '40'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN36_BW80_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN52_BW80_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_CLEAR_CHAN149_BW80_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '80'
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN165_BW20_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL165,
            'bandwidth': '20',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN44_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL44,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN60_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL60,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN157_BW40_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL157,
            'bandwidth': '40',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN36_BW80_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN52_BW80_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL52,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN149_BW80_WAN_THROUGHPUT(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.PC_HOST, userid=v.PC_USERNAME, password=v.PC_PWD)

        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '80',
            'encryption': 'psk2',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.wanStatus = api.getPppoeStatus(self.dut, self.__name__)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def assoc_sta_throughput_5g(self):
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn is True:
            staStatus = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            optionRedirect = {
                "name": "iperf",
                "proto": 1,
                "sport": v.IPERF_PORT,
                "ip": staStatus.get('ip'),
                "dport": v.IPERF_PORT,
            }
            api.setAddRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            iperfOn = SetAdbIperfOn(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            iperfOn.start()
            t.sleep(3.0)
            ret = setIperfFlow2(self.pc, self.wanStatus.get('ip'), v.IPERF_INTERVAL, v.IPERF_TIME, self.__class__.__name__)

            optionRedirect = {
                'port': v.IPERF_PORT
            }
            api.setDelRedirect(self.dut, self.__class__.__name__, **optionRedirect)
            api.setRedirectApply(self.dut, self.__class__.__name__)

            self.assertTrue(ret, "Excute iperf flow error, connection refused.")
        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class AP_PSK2_CHAN11_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'psk2',
            'pwd': v.KEY
        }

        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_psk2_sta_speedtest_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_CLEAR_CHAN11_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_clear_sta_speedtest_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_PSK2_CHAN149_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_psk2_sta_speedtest_5g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_CLEAR_CHAN149_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()

    def assoc_clear_sta_speedtest_5g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_GUEST_PSK2_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_psk2_sta_speedtest_guest(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.GUEST_SSID, v.KEY, "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_GUEST_CLEAR_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        optionGuest = {
            'wifiIndex': 3,
            'ssid': v.GUEST_SSID,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **optionGuest)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()

    def assoc_clear_sta_speedtest_guest(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.GUEST_SSID, "guest", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_RELAY_PSK2_CHAN11_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setDisableLanAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_psk2_sta_speedtest_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_RELAY_CLEAR_CHAN11_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'channel': v.CHANNEL11,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setDisableLanAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_clear_sta_speedtest_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_RELAY_PSK2_CHAN149_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'psk2',
            'pwd': v.KEY
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        api.setDisableLanAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_psk2_sta_speedtest_5g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_RELAY_CLEAR_CHAN149_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        api.setLanAp(self.dut, self.__name__)

        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'channel': v.CHANNEL149,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        api.setDisableLanAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_clear_sta_speedtest_5g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_WIRELESS_RELAY_PSK2_CHAN11_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            'encryption': 'WPA2PSK',
            'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            'channel': v.ROOT_AP_CHANNEL,
            'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_SSID,
            'nencryption': 'psk2',
            'npassword': v.KEY,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setDisableAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_psk2_sta_speedtest_2g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID, v.KEY, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_WIRELESS_RELAY_CLEAR_CHAN11_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            'encryption': 'WPA2PSK',
            'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            'channel': v.ROOT_AP_CHANNEL,
            'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_SSID,
            'nencryption': 'none',
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setDisableAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_clear_sta_speedtest_2g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID, "2g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_WIRELESS_RELAY_PSK2_CHAN149_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            'encryption': 'WPA2PSK',
            'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            'channel': v.ROOT_AP_CHANNEL,
            'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_SSID,
            'nencryption': 'psk2',
            'npassword': v.KEY,
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setDisableAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_psk2_sta_speedtest_5g(self):
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID_5G, v.KEY, "5g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_WIRELESS_RELAY_CLEAR_CHAN149_OOKLA(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)

        option = {
            'ssid': v.ROOT_AP_SSID,
            'encryption': 'WPA2PSK',
            'enctype': 'TKIPAES',
            'password': v.ROOT_AP_PWD,
            'channel': v.ROOT_AP_CHANNEL,
            'bandwidth': '20',
            'nssid': v.WIRELESS_RELAY_SSID,
            'nencryption': 'none',
        }
        api.setWifiAp(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        api.setDisableAp(self.dut, self.__name__)
        self.dut.close()

    def assoc_clear_sta_speedtest_5g(self):
        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.WIRELESS_RELAY_SSID_5G, "5g", self.__class__.__name__)
        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] == '':
                self.fail(msg='no ip address got.')
            else:
                speed = getAdbOoklaSpeedTestShot(v.ANDROID_SERIAL_NUM, self.__class__.__name__, self.__class__.__name__)
                self.assertTrue(speed, "Ookla speedtest run for wrong.")
        else:
            self.assertTrue(res2gConn, "Association wasnot successful.")


class AP_WAN_BANDWIDTH(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

    @classmethod
    def tearDownClass(self):
        self.dut.close()

    def test_wan_bandwidth(self):
        ret, speedDict= api.getWanBandwidth(self.dut, self.__class__.__name__)
        self.assertTrue(ret, "WAN port bandwidth test run for wrong.")

class AP_MIXEDPSK_NET_FORBIDDEN(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()
        option = {
            'mac': self.staMac,
            'wan': '0'
        }
        api.setNetMacFilter(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option = {
            'mac': self.staMac,
            'wan': '1'
        }
        api.setNetMacFilter(self.dut, self.__name__, **option)
        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_netForbidden_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA Access to website should be Forbidden')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_netForbidden_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA Access to website should be Forbidden')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_netForbidden_off_2g(self):

        option = {
            'mac': self.staMac,
            'wan': '1'
        }
        api.setNetMacFilter(self.dut, self.__class__.__name__, **option)
        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                option = {
                    'mac': self.staMac,
                    'wan': '0'
                }
                api.setNetMacFilter(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA Access to website should NOT be Forbidden')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_netForbidden_off_5g(self):

        option = {
            'mac': self.staMac,
            'wan': '1'
        }
        api.setNetMacFilter(self.dut, self.__class__.__name__, **option)
        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                option = {
                    'mac': self.staMac,
                    'wan': '0'
                }
                api.setNetMacFilter(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA Access to website should NOT be Forbidden')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


class AP_MIXEDPSK_NET_WHITELIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()
        option = {
            'mac': self.staMac,
            'mode': 'white'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option = {
            'mac': self.staMac,
            'mode': 'none'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_in_whitelist_2g(self):

        option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                    }
        api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                    }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website in whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_in_whitelist_5g(self):

        option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                    }
        api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':

                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website in whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_outof_whitelist_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA should not browser website outof whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_outof_whitelist_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA should not browser website outof whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


class AP_CLEAR_NET_WHITELIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()
        option = {
            'mac': self.staMac,
            'mode': 'white'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option = {
            'mac': self.staMac,
            'mode': 'none'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_clear_sta_in_whitelist_2g(self):

        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website in whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_in_whitelist_5g(self):

        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'white',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website in whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


    def assoc_clear_sta_outof_whitelist_2g(self):

        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA should not browser website outof whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_outof_whitelist_5g(self):

        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA should not browser website outof whitelist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


class AP_MIXEDPSK_NET_BLACKLIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()
        option = {
            'mac': self.staMac,
            'mode': 'black'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option = {
            'mac': self.staMac,
            'mode': 'none'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_in_blacklist_2g(self):

        option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
        api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertFalse(ret, msg='STA should not browser website in blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_in_blacklist_5g(self):

        option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
        api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertFalse(ret, msg='STA should not browser website in blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


    def assoc_psk2_outof_blacklist_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertTrue(ret, msg='STA should browser website outof blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_outof_blacklist_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertTrue(ret, msg='STA should browser website outof blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


class AP_CLEAR_NET_BLACKLIST(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()
        option = {
            'mac': self.staMac,
            'mode': 'black'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option = {
            'mac': self.staMac,
            'mode': 'none'
        }
        api.setParentCtrlFilter(self.dut, self.__name__, **option)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_clear_sta_in_blacklist_2g(self):

        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':

                option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertFalse(ret, msg='STA should not browser website in blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_in_blacklist_5g(self):

        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '0',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)

                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)

                option = {
                    'mac': self.staMac,
                    'mode': 'black',
                    'opt': '1',
                    'url': v.CHECK_ACCESS_URL2.split("//")[1],
                }
                api.setParentCtrlUrl(self.dut, self.__class__.__name__, **option)
                self.assertFalse(ret, msg='STA should not browser website in blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_outof_blacklist_2g(self):

        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertTrue(ret, msg='STA should browser website outof blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_outof_blacklist_5g(self):

        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertTrue(ret, msg='STA should browser website outof blacklist')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


class AP_MIXEDPSK_NET_CUTOFF_LIMITED(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()
        option = {
            'mac': self.staMac,
            'mode': 'limited',
            'enable': '1',
        }
        api.setNetAccessCtrl(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option = {
            'mac': self.staMac,
            'mode': 'none',
            'enable': '1',
        }
        api.setNetAccessCtrl(self.dut, self.__name__, **option)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_psk2_sta_2g(self):

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                # for url in iter(v.CHECK_ACCESS_URL_LIST):
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA should not browser website when net cutoff.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_sta_ctrloff_2g(self):

        option = {
            'mac': self.staMac,
            'mode': 'none',
            'enable': '1',
        }
        api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)

        res2gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID, v.KEY, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                # for url in iter(v.CHECK_ACCESS_URL_LIST):
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                    # if ret is False:
                    #     break
                option = {
                    'mac': self.staMac,
                    'mode': 'limited',
                    'enable': '1',
                }
                api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website when net control off.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_sta_5g(self):

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                # for url in iter(v.CHECK_ACCESS_URL_LIST):
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                self.assertFalse(ret, msg='STA should not browser website when net cutoff.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_psk2_sta_ctrloff_5g(self):

        option = {
            'mac': self.staMac,
            'mode': 'none',
            'enable': '1',
        }
        api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)

        res5gConn = setAdbPsk2Sta(v.ANDROID_SERIAL_NUM, v.SSID_5G, v.KEY, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':

                # for url in iter(v.CHECK_ACCESS_URL_LIST):
                ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, v.CHECK_ACCESS_URL2, self.__class__.__name__)
                    # if ret is False:
                    #     break
                option = {
                    'mac': self.staMac,
                    'mode': 'limited',
                    'enable': '1',
                }
                api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website when net control off.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


class AP_CLEAR_NET_CUTOFF_LIMITED(TestCase):
    @classmethod
    def setUpClass(self):
        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        ret2 = chkAdbDevice(v.ANDROID_SERIAL_NUM)

        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Device %s is not ready!" % v.ANDROID_SERIAL_NUM)
        option2g = {
            'wifiIndex': 1,
            'ssid': v.SSID,
            'encryption': 'none',
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': v.SSID_5G,
            'encryption': 'none',
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        wlanInfo = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__name__)
        self.staMac = wlanInfo["mac"].upper()
        option = {
            'mac': self.staMac,
            'mode': 'limited',
            'enable': '1',
        }
        api.setNetAccessCtrl(self.dut, self.__name__, **option)

    @classmethod
    def tearDownClass(self):

        option = {
            'mac': self.staMac,
            'mode': 'none',
            'enable': '1',
        }
        api.setNetAccessCtrl(self.dut, self.__name__, **option)

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        option5g = {
            'wifiIndex': 2,
            'on': 0
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        api.setWifi(self.dut, self.__name__, **option5g)

        self.dut.close()

    def assoc_clear_sta_2g(self):

        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                for url in iter(v.CHECK_ACCESS_URL_LIST):
                    ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, url, self.__class__.__name__)
                    self.assertFalse(ret, msg='STA should not browser website when net cutoff.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_ctrloff_2g(self):

        res2gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID, "2g", self.__class__.__name__)

        if res2gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                option = {
                    'mac': self.staMac,
                    'enable': '0',
                }
                api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)

                for url in iter(v.CHECK_ACCESS_URL_LIST):
                    ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, url, self.__class__.__name__)
                    if ret is False:
                        break
                option = {
                    'mac': self.staMac,
                    'mode': 'limited',
                    'enable': '1',
                }
                api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website when net control off.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_5g(self):

        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                for url in iter(v.CHECK_ACCESS_URL_LIST):
                    ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, url, self.__class__.__name__)
                    self.assertFalse(ret, msg='STA should not browser website when net cutoff.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")

    def assoc_clear_sta_ctrloff_5g(self):

        res5gConn = setAdbClearSta(v.ANDROID_SERIAL_NUM, v.SSID_5G, "5g", self.__class__.__name__)

        if res5gConn:
            result = getAdbShellWlan(v.ANDROID_SERIAL_NUM, self.__class__.__name__)
            if result['ip'] != '':
                option = {
                    'mac': self.staMac,
                    'enable': '0',
                }
                api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)

                for url in iter(v.CHECK_ACCESS_URL_LIST):
                    ret = chkAdbBrowserWebsite(v.ANDROID_SERIAL_NUM, url, self.__class__.__name__)
                    if ret is False:
                        break
                option = {
                    'mac': self.staMac,
                    'mode': 'limited',
                    'enable': '1',
                }
                api.setNetAccessCtrl(self.dut, self.__class__.__name__, **option)
                self.assertTrue(ret, msg='STA should browser website when net control off.')
            else:
                self.fail("STA should get IP address.")
        else:
            self.fail("Association should be successful.")


class AP_CHECK(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        self.dut2 = api.HttpClient()
        ret2 = self.dut2.connect(host=v.HOST, password=v.WEB_PWD)

        if ret1 is False:
            raise Exception("Connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': 'peanuts_check',
            'encryption': 'mixed-psk',
            'pwd': v.KEY,
            'channel': v.CHANNEL11,
        }
        option5g = {
            'wifiIndex': 2,
            'ssid': 'peanuts_check',
            'encryption': 'mixed',
            'pwd': v.KEY,
            'channel': v.CHANNEL149,
        }
        api.setWifi(self.dut2, self.__name__, **option2g)
        api.setWifi(self.dut2, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):
        pass

    def check_ap_reboot_lastestpower(self):
        count = 0
        while count <= 800:
            setMvFile(self.dut, self.__class__.__name__, src='/tmp/messages', dst='/tmp/message1')
            setReboot(self.dut, self.__class__.__name__)
            t.sleep(60)
            while 1:
                try:
                    self.dut = ShellClient(v.CONNECTION_TYPE)
                    ret = self.dut.connect(v.HOST, v.USR, v.PASSWD)
                    if ret is True:
                        chkCount = 0
                        while 1:
                            if chkCount < 20:
                                result = chkBootingUpFinished(self.dut, self.__class__.__name__)
                                if result is True:
                                    break
                                else:
                                    chkCount += 1
                                    t.sleep(10)
                            else:
                                self.fail(msg='reboot is failed')
                        break
                    else:
                        t.sleep(10)
                except Exception, e:
                    raise e

            power2g = 0
            power5g = 0
            while power2g == 0 or power5g == 0:
                power2g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "2g", self.__class__.__name__)
                txPower2g = getWlanTxPower(self.dut, "2g", self.__class__.__name__)
                t.sleep(1)
                power5g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "5g", self.__class__.__name__)
                txPower5g = getWlanTxPower(self.dut, "5g", self.__class__.__name__)
                t.sleep(1)

            if power2g <= (txPower2g - 5) or power5g <= (txPower5g - 5):
                loop = 0
                while loop < 120:
                    getWlanLastEstPower(self.dut, v.DUT_MODULE, "2g", self.__class__.__name__)
                    getWlanLastEstPower(self.dut, v.DUT_MODULE, "5g", self.__class__.__name__)
                    loop += 1
                    t.sleep(300)
                self.fail(msg='last est power check is failed')
            count += 1

    def check_ap_upgrade_lastestpower(self):
        count = 0
        while count <= 800:
            upgradefile = getFilePath(self.dut, self.__class__.__name__, path='/extdisks', pattern='brcm4709*')
            if len(upgradefile) is not 0:
                setCopyFile(self.dut, self.__class__.__name__, src=upgradefile, dst='/tmp/upgrade.bin')
                while not getFilePath(self.dut, self.__class__.__name__, path='/tmp', pattern='upgrade.bin'):
                    t.sleep(1)
                setMvFile(self.dut, self.__class__.__name__, src='/tmp/messages', dst='/tmp/message1')
                setUpgradeSystem(self.dut, '/tmp/upgrade.bin', self.__class__.__name__)
                t.sleep(60)
                while 1:
                    try:
                        self.dut = ShellClient(v.CONNECTION_TYPE)
                        ret = self.dut.connect(v.HOST, v.USR, v.PASSWD)
                        if ret is True:
                            chkCount = 0
                            while 1:
                                if chkCount < 20:
                                    result = chkBootingUpFinished(self.dut, self.__class__.__name__)
                                    if result is True:
                                        break
                                    else:
                                        chkCount += 1
                                        t.sleep(10)
                                else:
                                    self.fail(msg='upgrade is failed')
                            break
                        else:
                            t.sleep(10)
                    except Exception, e:
                        raise e

            power2g = 0
            power5g = 0
            while power2g == 0 or power5g == 0:
                power2g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "2g", self.__class__.__name__)
                txPower2g = getWlanTxPower(self.dut, "2g", self.__class__.__name__)
                t.sleep(1)
                power5g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "5g", self.__class__.__name__)
                txPower5g = getWlanTxPower(self.dut, "5g", self.__class__.__name__)
                t.sleep(1)

            if power2g <= (txPower2g - 5) or power5g <= (txPower5g - 5):
                loop = 0
                while loop < 120:
                    getWlanLastEstPower(self.dut, v.DUT_MODULE, "2g", self.__class__.__name__)
                    getWlanLastEstPower(self.dut, v.DUT_MODULE, "5g", self.__class__.__name__)
                    loop += 1
                    t.sleep(300)
                self.fail(msg='last est power check is failed')
            else:
                self.fail(msg='fail to find upgrade file!')
            count += 1

    def check_ap_reset_lastestpower(self):
        count = 0
        while count <= 800:
            setMvFile(self.dut, self.__class__.__name__, src='/tmp/messages', dst='/tmp/message1')
            api.setReset(self.dut2, self.__class__.__name__)
            t.sleep(60)
            while 1:
                try:
                    self.dut = ShellClient(v.CONNECTION_TYPE)
                    ret = self.dut.connect(v.HOST, v.USR, v.PASSWD)
                    if ret is True:
                        chkCount = 0
                        while 1:
                            if chkCount < 20:
                                result = chkBootingUpFinished(self.dut, self.__class__.__name__)
                                if result is True:
                                    break
                                else:
                                    chkCount += 1
                                    t.sleep(10)
                            else:
                                self.fail(msg='reboot is failed')
                        break
                    else:
                        t.sleep(10)
                except Exception, e:
                    raise e

            # router_init
            option = {
                'name': 'peanuts',
                'locale': '公司',
                'ssid': 'peanuts_check',
                'encryption': 'mixed-psk',
                'password': v.KEY,
                'txpwr': 1,
            }
            webclient = api.HttpClient()
            webclient.connect(host=v.HOST, password=v.WEB_PWD, init=1)
            api.setRouterNormal(webclient, self.__class__.__name__, **option)
            webclient.close()

            txPower2g = 0
            txPower5g = 0
            while txPower2g == 0 or txPower5g == 0:
                power2g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "2g", self.__class__.__name__)
                txPower2g = getWlanTxPower(self.dut, "2g", self.__class__.__name__)
                t.sleep(1)
                power5g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "5g", self.__class__.__name__)
                txPower5g = getWlanTxPower(self.dut, "5g", self.__class__.__name__)
                t.sleep(1)

            loop = 0
            while power2g <= (txPower2g - 5) or power5g <= (txPower5g - 5):
                t.sleep(10)
                power2g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "2g", self.__class__.__name__)
                txPower2g = getWlanTxPower(self.dut, "2g", self.__class__.__name__)
                power5g = getWlanLastEstPower(self.dut, v.DUT_MODULE, "5g", self.__class__.__name__)
                txPower5g = getWlanTxPower(self.dut, "5g", self.__class__.__name__)

                loop += 1
                if loop >= 360:
                    self.fail(msg='last est power check is failed')
            count += 1
            self.dut2.connect(host=v.HOST, password=v.WEB_PWD)

class STA_CHECK(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = ShellClient(v.CONNECTION_TYPE)
        ret1 = self.dut.connect(v.HOST, v.USR, v.PASSWD)
        self.dut2 = api.HttpClient()
        ret2 = self.dut2.connect(host=v.HOST, password=v.WEB_PWD)

        if ret1 is False:
            raise Exception("Connection is failed. please check your remote settings.")

        if ret2 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        # option = {
        #     'bsd': 1,
        #     'ssid1': 'aiCheckAfterApReboot',
        #     'encryption1': 'mixed-psk',
        #     'pwd1': '12345678',
        # }
        # api.setAllWifi(self.dut2, self.__name__, **option)

    @classmethod
    def tearDownClass(self):
        pass

    def check_sta_after_apReboot(self):
        count = 0
        while count <= int(v.AP_REBOOT_COUNT):
            setReboot(self.dut, self.__class__.__name__)
            t.sleep(90)
            while 1:
                try:
                    self.dut = ShellClient(v.CONNECTION_TYPE)
                    ret = self.dut.connect(v.HOST, v.USR, v.PASSWD)
                    if ret is True:
                        chkCount = 0
                        while 1:
                            if chkCount < 20:
                                result = chkBootingUpFinished(self.dut, self.__class__.__name__)
                                if result is True:
                                    break
                                else:
                                    chkCount += 1
                                    t.sleep(10)
                            else:
                                self.fail(msg='reboot is failed')
                        break
                    else:
                        t.sleep(10)
                except Exception, e:
                    raise e

            t.sleep(10)

            if v.CHECK_STA_MAC2 == '':
                self.check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC, self.__class__.__name__)
                self.check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC, self.__class__.__name__)

                if self.check2g is False and self.check5g is False:
                    loop = 0
                    while loop < 30:
                        t.sleep(10)
                        self.check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC, self.__class__.__name__)
                        self.check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC, self.__class__.__name__)
                        loop += 1
                        if self.check2g is True or self.check5g is True:
                            break

                if self.check2g is False and self.check5g is False:
                    self.fail(msg='After AP %d times Reboot, Specified Sta1 Online Failed within 5 minutes' % count+1)

            else:
                self.check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC, self.__class__.__name__)
                self.check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC, self.__class__.__name__)
                self.sta2check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC2, self.__class__.__name__)
                self.sta2check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC2, self.__class__.__name__)

                allFailed = (self.check2g is False and self.check5g is False) and \
                        (self.sta2check2g is False and self.sta2check5g is False)
                sta1Failed = (self.check2g is False and self.check5g is False) and \
                        (self.sta2check2g is True or self.sta2check5g is True)
                sta2Failed = (self.check2g is True or self.check5g is True) and \
                        (self.sta2check2g is False and self.sta2check5g is False)

                if sta1Failed:
                    loop = 0
                    while loop < 30:
                        t.sleep(10)
                        self.check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC, self.__class__.__name__)
                        self.check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC, self.__class__.__name__)
                        loop += 1
                        if self.check2g is True or self.check5g is True:
                            break

                if sta2Failed:
                    loop = 0
                    while loop < 30:
                        t.sleep(10)
                        self.sta2check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC2, self.__class__.__name__)
                        self.sta2check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC2, self.__class__.__name__)
                        loop += 1
                        if self.sta2check2g is True or self.sta2check5g is True:
                            break

                if allFailed:
                    loop = 0
                    while loop < 30:
                        t.sleep(10)
                        self.check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC, self.__class__.__name__)
                        self.check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC, self.__class__.__name__)
                        self.sta2check2g = chkStaOnline(self.dut, '2g', v.CHECK_STA_MAC2, self.__class__.__name__)
                        self.sta2check5g = chkStaOnline(self.dut, '5g', v.CHECK_STA_MAC2, self.__class__.__name__)
                        loop += 1
                        if (self.check2g is True or self.check5g is True) and \
                            (self.sta2check2g is True or self.sta2check5g is True):
                            break

                if self.check2g is False and self.check5g is False:
                    if self.sta2check2g is False and self.sta2check5g is False:
                        self.fail(msg='After AP %d times Reboot, Specified 2 Stas Online Failed within 5 minutes' % count+1)
                    else:
                        self.fail(msg='After AP %d times Reboot, Specified Sta1 Online Failed within 5 minutes' % count+1)
                if self.sta2check2g is False and self.sta2check5g is False:
                    self.fail(msg='After AP %d times Reboot, Specified Sta2 Online Failed within 5 minutes' % count+1)

            count += 1


class IxChariot_Lan2Wifi_2g_CHAN1_BW20(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.THROUGHPUT_SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_1_20_tx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")

    def rx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_1_20_rx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class IxChariot_Lan2Wifi_2g_CHAN6_BW20(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.THROUGHPUT_SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '20',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_6_20_tx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")

    def rx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_6_20_rx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class IxChariot_Lan2Wifi_2g_CHAN11_BW20(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.THROUGHPUT_SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '20',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_11_20_tx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")

    def rx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_11_20_rx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class IxChariot_Lan2Wifi_2g_CHAN1_BW40(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.THROUGHPUT_SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '40',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_1_40_tx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")

    def rx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_1_40_rx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class IxChariot_Lan2Wifi_2g_CHAN6_BW40(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.THROUGHPUT_SSID,
            'channel': v.CHANNEL6,
            'bandwidth': '40',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_6_40_tx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")

    def rx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_6_40_rx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class IxChariot_Lan2Wifi_2g_CHAN11_BW40(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.THROUGHPUT_SSID,
            'channel': v.CHANNEL11,
            'bandwidth': '40',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option2g)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_11_40_tx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")

    def rx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_11_40_rx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


class IxChariot_Lan2Wifi_5g_CHAN36_BW80(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option5g = {
            'wifiIndex': 2,
            'ssid': v.THROUGHPUT_SSID_5G,
            'channel': v.CHANNEL36,
            'bandwidth': '80',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res5gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'conn', self.__class__.__name__)
        if res5gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_5g_36_80_tx'] = throughputResult

        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")

    def rx(self):

        res5gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'conn', self.__class__.__name__)
        if res5gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_5g_36_80_rx'] = throughputResult

        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class IxChariot_Lan2Wifi_5g_CHAN149_BW80(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option5g = {
            'wifiIndex': 2,
            'ssid': v.THROUGHPUT_SSID_5G,
            'channel': v.CHANNEL149,
            'bandwidth': '80',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option5g)

    @classmethod
    def tearDownClass(self):

        option5g = {
            'wifiIndex': 2,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option5g)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res5gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'conn', self.__class__.__name__)
        if res5gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_5g_149_80_tx'] = throughputResult

        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")

    def rx(self):

        res5gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'conn', self.__class__.__name__)
        if res5gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID_5G, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_5g_149_80_rx'] = throughputResult

        else:
            self.assertTrue(res5gConn, "Connecting wifi is failed.")


class IxChariot_Wan2Wifi_2g_CHAN1_BW20(TestCase):
    @classmethod
    def setUpClass(self):

        self.dut = api.HttpClient()
        ret1 = self.dut.connect(host=v.HOST, password=v.WEB_PWD)
        self.pc = ShellClient(4)
        ret3 = self.pc.connect(host=v.IXIA_STA_HOST, userid=v.IXIA_STA_USERNAME, password=v.IXIA_STA_PWD)
        if ret3 is False:
            raise Exception("PC telnet connection is failed, please check network.")
        if ret1 is False:
            raise Exception("Http connection is failed. please check your remote settings.")

        option2g = {
            'wifiIndex': 1,
            'ssid': v.THROUGHPUT_SSID,
            'channel': v.CHANNEL1,
            'bandwidth': '20',
            'encryption': 'mixed-psk',
            'pwd': v.THROUGHPUT_PW,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        optionWan = {
            'wanType': 'static',
            'staticIp': '192.168.1.1',
            'staticMask': '255.255.255.0',
            'staticGateway': '192.168.1.2',
            'dns1': '192.168.1.2',
            'dns2': '',
        }
        api.setWan(self.dut, self.__name__, **optionWan)
        optionWan1 = {
            'wanType': 'dhcp',
            'autoset': '0'
        }
        api.setWan(self.dut, self.__name__, **optionWan1)

    @classmethod
    def tearDownClass(self):

        option2g = {
            'wifiIndex': 1,
            'on': 0,
        }
        api.setWifi(self.dut, self.__name__, **option2g)
        optionWan = {
            'wanType': 'dhcp',
            'autoset': '0'
        }
        api.setWan(self.dut, self.__name__, **optionWan)
        self.dut.close()
        self.pc.close()

    def tx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_TX.tst"
            throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_1_20_tx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")

    def rx(self):

        res2gConn = setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'conn', self.__class__.__name__)
        if res2gConn is True:

            lan_wifi = chkOSPingAvailable(v.IXIA_STA_IP, 5, self.__class__.__name__)
            self.assertTrue(lan_wifi, "Lan ping Wifi Failed.")

            ixChariot_result_name = self.__class__.__name__ + "_RX.tst"
            throughputResult = runIxChariot(v.IXIA_STA_IP, v.IXIA_LAN_PC, ixChariot_result_name)
            setWindowsSta(self.pc, v.THROUGHPUT_SSID, 'disconn', self.__class__.__name__)
            # call tcl with ixchariot will change the redirect the path to ixchariot install path
            os.chdir(v.DEFAULT_PATH)
            # throughputResult type is str
            if throughputResult in v.TCL_RETURN:
                self.fail(msg=v.TCL_RETURN[throughputResult])
            v.THROUGHPUT_RESULT['lan2wifi_2g_1_20_rx'] = throughputResult

        else:
            self.assertTrue(res2gConn, "Connecting wifi is failed.")


if __name__ == '__main__':
    v.HOST = "192.168.31.1"
    v.WEB_PWD = "12345678"
    v.ANDROID_SERIAL_NUM = "4ea65416"
    cases = [
        'assoc_sta_throughput_2g',
    ]

    suite = TestSuite(map(AP_CLEAR_CHAN1_BW20_WAN_THROUGHPUT, cases))
    curTime = t.strftime('%Y.%m.%d %H.%M.%S', t.localtime())
    f = open(curTime + '_RESULT.log', 'a')
    runner = TextTestRunner(f, verbosity=2)
    runner.run(suite)
    f.close()
