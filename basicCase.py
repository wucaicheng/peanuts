# ------------------- basic cases for daily--------------------
from collections import OrderedDict
import data
import ConfigParser
import var as v

class BasicCase():

    def __init__(self, configFile):
        config = ConfigParser.ConfigParser()
        with open(configFile, "r") as cfgfile:
            config.readfp(cfgfile)
        v.DUT_MODULE = config.get("config", "device")
        v.CONNECTION_TYPE = config.getint("config", "remoteControl")
        v.SEND_MAIL = config.getint("config", "sendMail")


        self.init = None
        self.token = None

    def generateCaseDict(self, caselist):

        cases = OrderedDict()
        for i in range(len(caselist)):
            if isinstance(caselist[i], str):
                cases[caselist[i]] = caselist[i+1]
        return cases



if __name__ == "__main__":

    ba = BasicCase('r3p.cfg')
    print v.DUT_MODULE, v.SEND_MAIL
    # caseDict = ba.generateCaseDict(data.BasicCase4DualBand)
