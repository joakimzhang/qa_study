# -*- coding: utf-8 -*-

import switch_stream


class switch_stream_Worker():
    def __init__(self):
        self.data={}

    def run_switch(self,ts_card,ts_file):
        print "the ts path is:%s"%ts_file
        print "the ts card is %s"%ts_card
        ts_file = r'%s'%ts_file
        argv_stream = ["-H", ts_card,"-P", "7777","-f",ts_file,'--std=DTMB',"-F", "578"]
        switch_stream.exec_switch(argv_stream)
        print "switch stream successfully"
if __name__ == "__main__":
    test = switch_stream_Worker()
    test.run_switch(r"bjdittest",r"\\10.209.156.47\scannedfiles\zhangq\yanquan.ts")
