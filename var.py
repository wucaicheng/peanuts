# -*- coding: utf8 -*-
from common2 import *
import os

VER = '3.9.8'

TOOL_LIST = ["General", "Memory Tracking", "Test Suite"]

# ----------------General-----------------

SAVE_BTN_FLAG = False  # represent save button pressed or not

DUT_MODULE_LIST = ['R1D', 'R1CM', 'R2D', "R1CL", "R3", "R3L", "R3P", "R3D", "PLW", "R3A", "R3G"]
DUT_MODULE = DUT_MODULE_LIST[0]
HOST = "192.168.31.1"
HOST_UPPER = "192.168.100.1"
HOST_UPPER_WIRELESS = "192.168.100.1"
HOST_ORIGINAL = ""
USR = "root"
PASSWD = "admin"
WIRELESS_2G_RELAY_UPPER_SSID = 'miwifi'
WIRELESS_2G_RELAY_UPPER_PW = '12345678'
WIRELESS_5G_RELAY_UPPER_SSID = 'miwifi_5G'
WIRELESS_5G_RELAY_UPPER_PW = '12345678'
# WIRELESS_2G_RELAY_UPPER_OPTION = {
#     'ssid': '',
#     'encryption': '',
#     'enctype': '',
#     'password': '',
#     'channel': '',
#     'band': ''
# }
# WIRELESS_5G_RELAY_UPPER_OPTION = {
#     'ssid': '',
#     'encryption': '',
#     'enctype': '',
#     'password': '',
#     'channel': '',
#     'band': ''
# }

R1CM_MAX_RATE_2G = {'20': 144, '40': 300}
R1CM_MAX_RATE_5G = {'20': 173, '40': 400, '80': 867}
R3P_MAX_RATE_2G = {'20': 288, '40': 600}
R3P_MAX_RATE_5G = {'20': 346, '40': 800, '80': 1734}
R3D_MAX_RATE_2G = {'20': 378, '40': 800}
R3D_MAX_RATE_5G = {'20': 346, '40': 800, '80': 1733, '160': 1733}
R3A_MAX_RATE_2G = {'20': 144, '40': 300}
R3A_MAX_RATE_5G = {'20': 173, '40': 400, '80': 867}
R1CL_MAX_RATE_2G = {'20': 144, '40': 300}
R3G_MAX_RATE_2G = {'20': 144, '40': 300}
R3G_MAX_RATE_5G = {'20': 173, '40': 400, '80': 867}
R2D_MAX_RATE_2G = {'20': 144, '40': 300}
R2D_MAX_RATE_5G = {'20': 173, '40': 400, '80': 866}
R1D_MAX_RATE_2G = {'20': 144, '40': 300}
R1D_MAX_RATE_5G = {'20': 173, '40': 400, '80': 866}
"""
connection_type = 1 represent ssh
                  2 represent telnet
                  3 serial
                  4 pc telnet
"""
CONNECTION_TYPE = 1

SERIAL_PORT = ""
BAUDRATE = 115200

ANDROID_SERIAL_NUM = ''
ANDROID_MODEL = ''
STA_COUNT = "1"

# uci show | grep -i network.wan.ifname
WAN_IFNAME = {
    "R1D": 'eth0.2',
    "R2D": 'eth0.2',
    "R1CM": 'eth0.2',
    "R3": 'eth0.2',
    "R1CL": 'eth0.2',
    "R3L": 'eth0.2',
    "R3P": 'eth1',
    "R3D": 'eth0',
    "R3A": 'eth0.2',
    "R3G": 'eth1'
}
# -------------pc telnet------------------#
PC_USERNAME = 'jac-pc2'
PC_PWD = '12345678'
PC_HOST = '10.237.143.13'
IPERF_PORT = 5001

# ----------------Memory Tracking-----------------
# TOTAL_MEM = 256
WIDTH = 2000
WIDTH2 = 4000
INTERVAL = 1
COUNT = 10

"""
1.periodically launched by cpulimit_daemon.sh
/bin/mpstat 4 1 -P 0 | awk 'NR>6 {print $11}' | awk -F. '{print $1}'
2.periodically launched by Peanuts
ps w
"""
EXCEPTIONS = ['ps', 'awk', 'sleep', 'mpstat', 'cpulimit_daemon']
KERNEL_EXCEPTIONS = []

# ----------------Test Suite-----------------

INTF_2G = 'wl1'
INTF_5G = 'wl0'
INTF_GUEST = 'guest'

WORD_RANGE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
SPEC_RANGE = '~!@#$%^&*() =+\\|]}[{\'\";:/?.>,<'
CHINESE_RANGE = "宣室求贤访逐臣贾生才调更无伦可怜夜半虚前席不问苍生问鬼神火佛秋金"

SSID = generateRandomString(WORD_RANGE, 31)
SSID_5G = generateRandomString(WORD_RANGE, 31)
GUEST_SSID = generateRandomString(WORD_RANGE, 31)

SPECIAL_SSID = generateRandomString(SPEC_RANGE, 31)
SPECIAL_SSID_5G = generateRandomString(SPEC_RANGE, 31)

CHINESE_SSID = generateRandomString(CHINESE_RANGE, 10)
CHINESE_SSID_5G = generateRandomString(CHINESE_RANGE, 10)

WIRELESS_RELAY_SSID = generateRandomString(WORD_RANGE, 28)
WIRELESS_RELAY_SSID_5G = WIRELESS_RELAY_SSID + "_5G"
WIRELESS_RELAY_SPECIAL_SSID = generateRandomString(SPEC_RANGE, 28)
WIRELESS_RELAY_SPECIAL_SSID_5G = WIRELESS_RELAY_SPECIAL_SSID + "_5G"
WIRELESS_RELAY_CHINESE_SSID = generateRandomString(CHINESE_RANGE, 9)
WIRELESS_RELAY_CHINESE_SSID_5G = WIRELESS_RELAY_CHINESE_SSID + "_5G"

KEY = generateRandomString(WORD_RANGE, 63)
SPECIAL_KEY = generateRandomString(SPEC_RANGE, 63)

REPORT_NAME = ""
REPORT_FILE_NAME = ""
TEST_SUITE_LOG_PATH = os.getcwd() + os.sep + "TEST_SUITE_LOG" + os.sep
OOKLA_SHOT_PATH = TEST_SUITE_LOG_PATH + "OOKLA" + os.sep
IPERF_PATH = os.getcwd() + os.sep + "iperf" + os.sep
DEFAULT_PATH = os.getcwd() + os.sep
SSH_LOG_PATH = DEFAULT_PATH + "ssh_connection.log"
DEVICE_STATUS_LOG = "device_status_log"

PING_PERCENT_PASS = 60
PING_COUNT = 5
PING_BIG_PERCENT_PASS = 5
PING_BIG_SIZE = 20000
PING_BIG_COUNT = 20
PING_TARGET = 'www.baidu.com'
PING_TARGET_WITHOUT_DNS = '114.114.114.114'
CHECK_ACCESS_URL = "http://miwifi.com/cgi-bin/luci/web"
CHECK_ACCESS_URL2 = "https://m.baidu.com"
CHECK_ACCESS_URL3 = "http://www.sohu.com"
CHECK_ACCESS_URL4 = "http://m.taobao.com"
CHECK_ACCESS_URL5 = "http://m.jd.com"
CHECK_ACCESS_URL6 = "http://m.sina.cn"
CHECK_ACCESS_URL_LIST = [CHECK_ACCESS_URL2, CHECK_ACCESS_URL3, CHECK_ACCESS_URL4, CHECK_ACCESS_URL5, CHECK_ACCESS_URL6]

BSSID = ''
BSSID_5G = ''
STA_MAC = ''
STA_MAC_5G = ''

CHANNEL_2_ALL = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
CHANNEL_5_ALL = ['36', '40', '44', '48', '52', '56', '60', '64', '149', '153', '157', '161', '165']
CHANNEL_2_RANDOM = generateRandomChannel(CHANNEL_2_ALL)
CHANNEL_5_RANDOM = generateRandomChannel(CHANNEL_5_ALL)

CHANNEL1 = '1'
CHANNEL6 = '6'
CHANNEL11 = '11'
CHANNEL13 = '13'

CHANNEL36 = '36'
CHANNEL44 = '44'
CHANNEL48 = '48'
CHANNEL52 = '52'
CHANNEL60 = '60'
CHANNEL64 = '64'

CHANNEL149 = '149'
CHANNEL157 = '157'
CHANNEL165 = '165'

IPERF_INTERVAL = ""
IPERF_TIME = "60"
# IPERF_INTERVAL = "1"
# IPERF_TIME = "5"

QOS_MAXUP = 250
QOS_MAXDOWN = 250

ROOT_AP_SSID = "peanuts_automatic_test_root_ap_"
ROOT_AP_PWD = "12345678"
ROOT_AP_CHANNEL = 11

UPLOAD_LOG = 1
FAIL_RETRY = 3
MEM_MONITOR_INTERVAL = 60

# -------------api------------------#
WEB_USERNAME = 'admin'
WEB_PWD = '12345678'
WEB_PWD_UPPER = '12345678'
WEB_PWD_UPPER_WIRELESS = '12345678'
WEB_KEY = 'a2ffa5c9be07488bbb04a3a47d3c5f6a'
IV = '64175472480004614961023454661220'
# uci export account
ACCOUNT_DEFAULT_PWD = 'b3a4190199d9ee7fe73ef9a4942a69fece39a771'

# -------------process report------------------#
WIFI_MAX_THROUGHPUT = 300
REPORT_TAG_BEGIN = '----->TestSuite Execution Begin:'
REPORT_TAG_RETRY = '----->Failed or Error TestCases Retry Times:'
REPORT_TAG_END = '----->TestSuite Execution END'
# -------------mail------------------#
SEND_MAIL = 1
MAILTO_LIST = ['miwifi-test-wifi@xiaomi.com']
MAIL_HOST = "mail.srv"  #设置服务器
MAIL_USER = "robot"    #用户名
MAIL_PASS = ""   #口令
MAIL_POSTFIX="xiaomi.com"  #发件箱的后缀
MAILFROM_LIST = "robot@xiaomi.com"
MAIL_TITLE = ""

MAIL_PIC1 = TEST_SUITE_LOG_PATH + "Total_Memory_Used.png"
MAIL_PIC2 = TEST_SUITE_LOG_PATH + "DUT_to_2GHz.png"
MAIL_PIC3 = TEST_SUITE_LOG_PATH + "DUT_to_5GHz.png"
MAIL_PIC4 = TEST_SUITE_LOG_PATH + "Current_CPU_Load.png"
MAIL_PIC5 = TEST_SUITE_LOG_PATH + "LAN_to_2GHz.png"
MAIL_PIC6 = TEST_SUITE_LOG_PATH + "LAN_to_5GHz.png"
MAIL_PIC7 = TEST_SUITE_LOG_PATH + "WAN_to_2GHz.png"
MAIL_PIC8 = TEST_SUITE_LOG_PATH + "WAN_to_5GHz.png"
MAIL_PIC9 = TEST_SUITE_LOG_PATH + "Ookla_Speedtest_2GHz.png"
MAIL_PIC10 = TEST_SUITE_LOG_PATH + "Ookla_Speedtest_5GHz.png"
MAIL_XLSX = TEST_SUITE_LOG_PATH + "Memory_Tracking.xlsx"
MAIL_THROUGHPUT_XLSX_ORIGINAL = "throughput.xlsx"
MAIL_THROUGHPUT_XLSX = TEST_SUITE_LOG_PATH + MAIL_THROUGHPUT_XLSX_ORIGINAL

# ----------------------check-------------------
CHECK_STA_MAC = '0C:1D:AF:9F:DD:21'
AP_REBOOT_COUNT = 800


if __name__ == '__main__':
    print R1CM_MAX_RATE_2G['20']