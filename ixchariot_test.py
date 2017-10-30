import var as v
from common import *



ixChariot_result_name = 'fengjiang' + "_TX.tst"
throughputResult = runIxChariot(v.IXIA_LAN_PC, v.IXIA_STA_IP, ixChariot_result_name)
