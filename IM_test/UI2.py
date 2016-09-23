'''
Created on 2015-3-24

@author: zhangq
'''
import wx
import sent_key

import parseIrkey

#import format_case
import globalVariable 


import os
import re


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.main_path=os.getcwd()

        self.IP="10.209.157.84"
        self.port="7777"
        self.card="BKS"
        self.delay="1000"
        self.temtext=""
        self.name=""
        self.Stream_Std="DTMB"
        self.Stream_File="\\10.209.157.77"
        self.Stream_Freq="584"
        self.Stream_Bandwidth="4"
        self.Stream_Modulation="4"
        self.filename=[]
        self.filepath=[]
        self.is_import=1
        self.tag=[]
        self.key_index=1
        
        self.TT_TAG=0
        self.B1=[]
        self.B2=[]
        self.B3=[]
        self.B4=[] 
        self.B5=[] 
        self.B6=[]  
        self.B7=[] 
        self.case_list=[]
        
        
        
        # create some sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = wx.GridBagSizer(hgap=5, vgap=5)
        self.grid_stream = wx.GridBagSizer(hgap=5, vgap=5)
        self.grid_box = wx.GridBagSizer(hgap=5, vgap=5)
        self.grid_delay = wx.GridBagSizer(hgap=5, vgap=5)
        self.grid_button = wx.GridBagSizer(hgap=5, vgap=5)
        self.case = wx.GridSizer(20,4,0,0)
        self.gs = wx.GridBagSizer(hgap=1, vgap=1)
        self.gs_case = wx.GridBagSizer(hgap=1, vgap=1)
        #self.gs = wx.GridSizer(20,3,0,0)

        
        #input case box
        self.logger = wx.TextCtrl(self, size=(320,580), style=wx.TE_MULTILINE )
        self.Bind(wx.EVT_TEXT, self.BoxText, self.logger)
        

        
        #video button
        self.button_video_cap =wx.Button(self, label="video_cap",size=(70, 25))   
        self.button_video_cap.SetBackgroundColour("Navy")    
        self.button_video_cap.SetForegroundColour("white") 
        self.Bind(wx.EVT_BUTTON, self.video_cap,self.button_video_cap)
        self.grid_button.Add(self.button_video_cap, pos=(3,1), span=(1,1)) 


        #start button
        self.button_start =wx.Button(self, label="start",size=(70, 25))        
        self.Bind(wx.EVT_BUTTON, self.start_case,self.button_start)
        self.grid_button.Add(self.button_start, pos=(1,1), span=(1,1))
        #SAVE button
        self.button =wx.Button(self, label="Save",size=(70, 25))        
        self.Bind(wx.EVT_BUTTON, self.OnClick_SAVE,self.button)
        self.grid_button.Add(self.button, pos=(1,0), span=(1,1))
        
        #format case button
        self.button =wx.Button(self, label="format",size=(70, 25))        
        self.Bind(wx.EVT_BUTTON, self.format_file,self.button)
        self.grid_button.Add(self.button, pos=(1,2), span=(1,1))
        
        """
        #Delete button
        self.button =wx.Button(self, label="Delete")        
        self.Bind(wx.EVT_BUTTON, self.OnClick_Del,self.button)
        self.grid_button.Add(self.button, pos=(1,2), span=(1,1))
        """
        #Open case button
        self.button =wx.Button(self, label="Open case",size=(70, 25))        
        self.Bind(wx.EVT_BUTTON, self.OnClick_Open_case,self.button)
        self.grid_button.Add(self.button, pos=(2,1), span=(1,1))
        #Open caselist button
        self.button =wx.Button(self, label="caselist",size=(70, 25))        
        self.Bind(wx.EVT_BUTTON, self.OnClick_Open_case_list,self.button)
        self.grid_button.Add(self.button, pos=(2,2), span=(1,1))
        #scan case button
        self.button =wx.Button(self, label="scan_case",size=(70, 25))        
        self.Bind(wx.EVT_BUTTON, self.OnClick_Scan_case,self.button)
        self.grid_button.Add(self.button, pos=(2,0), span=(1,1))
        
        # Radio Boxes
        radioList = ['libra2', 'librasd', 'Sunplus']    
        self.rb = wx.RadioBox(self, label="Choose the IR_KEY MAP ", pos=(20, 210), choices=radioList,  majorDimension=3,style=wx.RA_SPECIFY_COLS)
        self.grid.Add(self.rb, pos=(0,0), span=(1,2))     
        self.Bind(wx.EVT_RADIOBOX, self.Evt_Change_IR_MAP, self.rb)
        print "~~~~~~~~"
        print self.rb.GetItemLabel(self.rb.GetSelection())
        print "~~~~~~~~"
        
        """
        #test type box
        test_type = ['normal_test', 'mem_test']    
        self.tt = wx.RadioBox(self, label="Choose the test type ", pos=(20, 210), choices=test_type,  majorDimension=2,style=wx.RA_SPECIFY_COLS)
        self.grid.Add(self.tt, pos=(1,0), span=(1,2))     
        self.Bind(wx.EVT_RADIOBOX, self.Evt_test_type, self.tt)
        """
        
        # Case name.
        self.lblname = wx.StaticText(self, label="Case name :")
        self.grid_box.Add(self.lblname, pos=(0,0))       
        self.editname = wx.TextCtrl(self, value="APP-", size=(140,-1))
        self.grid_box.Add(self.editname, pos=(0,1))
        self.Bind(wx.EVT_TEXT, self.EvtName, self.editname)

        #input stream button
        self.button_stream =wx.Button(self, label="-->",size=(70,25))        
        self.Bind(wx.EVT_BUTTON, self.OnClick_stream,self.button_stream)
        self.grid_stream.Add(self.button_stream, pos=(0,0), span=(1,1))
        #IP drop down box
        self.sampleList = ['10.209.157.84', '10.209.157.83', '10.209.157.77']
        self.lblhear = wx.StaticText(self, label=" ip")
        self.grid_stream.Add(self.lblhear, pos=(1,0))
        self.edithear = wx.ComboBox(self, value="10.209.156.203", size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.grid_stream.Add(self.edithear, pos=(1,1))        
        self.Bind(wx.EVT_COMBOBOX, self.EvtIP, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtIP,self.edithear)
        #port drop down box
        self.sampleList1 = ['7777', '8080', '21', '777']
        self.lblhear = wx.StaticText(self, label=" port")
        self.grid_stream.Add(self.lblhear, pos=(2,0))
        self.edithear = wx.ComboBox(self, value="7777",size=(95, -1), choices=self.sampleList1, style=wx.CB_DROPDOWN)
        self.grid_stream.Add(self.edithear, pos=(2,1))        
        self.Bind(wx.EVT_COMBOBOX, self.EvtPORT, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtPORT,self.edithear)
        
        #card drop down box
        self.sampleList2 = ['BKS', 'DTK']
        self.lblhear = wx.StaticText(self, label=" card")
        self.grid_stream.Add(self.lblhear, pos=(3,0))
        self.edithear = wx.ComboBox(self,value="BKS", size=(95, -1), choices=self.sampleList2, style=wx.CB_DROPDOWN)
        self.grid_stream.Add(self.edithear, pos=(3,1))        
        self.Bind(wx.EVT_COMBOBOX, self.EvtCARD, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtCARD,self.edithear)
        
        #Stream_Bandwidth drop down box
        self.sampleList3 = ['4', '8', '16', '32']
        self.lblhear = wx.StaticText(self, label="Bandwidth")
        self.grid_stream.Add(self.lblhear, pos=(4,0))
        self.edithear = wx.ComboBox(self,value="4", size=(95, -1), choices=self.sampleList3, style=wx.CB_DROPDOWN)
        self.grid_stream.Add(self.edithear, pos=(4,1))        
        self.Bind(wx.EVT_COMBOBOX, self.Evt_Stream_Bandwidth, self.edithear)
        self.Bind(wx.EVT_TEXT, self.Evt_Stream_Bandwidth,self.edithear)
        #Stream_Modulation drop down box
        self.sampleList4 = ['4','8','16', '32', '64']
        self.lblhear = wx.StaticText(self, label="Modulation")
        self.grid_stream.Add(self.lblhear, pos=(5,0))
        self.edithear = wx.ComboBox(self,value="4", size=(95, -1), choices=self.sampleList4, style=wx.CB_DROPDOWN)
        self.grid_stream.Add(self.edithear, pos=(5,1))        
        self.Bind(wx.EVT_COMBOBOX, self.Evt_Stream_Modulation, self.edithear)
        self.Bind(wx.EVT_TEXT, self.Evt_Stream_Modulation,self.edithear)
        
        #Stream_Modulation drop down box
        self.sampleList5 = ['DTMB','dvb']
        self.lblhear = wx.StaticText(self, label=" Stream_Std")
        self.grid_stream.Add(self.lblhear, pos=(6,0))
        self.edithear = wx.ComboBox(self, value="DTMB",size=(95, -1), choices=self.sampleList5, style=wx.CB_DROPDOWN)
        self.grid_stream.Add(self.edithear, pos=(6,1))        
        self.Bind(wx.EVT_COMBOBOX, self.Evt_Stream_Std, self.edithear)
        self.Bind(wx.EVT_TEXT, self.Evt_Stream_Std,self.edithear)
        
        #Stream_Modulation drop down box
        self.sampleList6 = ['F:\\zhangq\\0.3.0_loader_stream.ts','\\\\10.209.156.121\\111.ts']
        self.lblhear =wx.Button(self, label="Stream_File",size=(70, 25))        
        self.Bind(wx.EVT_BUTTON, self.Choose_ts_file,self.lblhear)      
        self.grid_stream.Add(self.lblhear, pos=(7,0),span=(1,1))
        
        self.tsfile = wx.TextCtrl(self, value="input stream file path", size=(140,-1))
        self.grid_stream.Add(self.tsfile, pos=(7,1))        
        #self.Bind(wx.EVT_COMBOBOX, self.Evt_Stream_File, self.tsfile)
        self.Bind(wx.EVT_TEXT, self.Evt_Stream_File,self.tsfile)
        #Stream_Modulation drop down box
        self.sampleList7 = ['474','714','666']
        self.lblhear = wx.StaticText(self, label=" Stream_Freq")
        self.grid_stream.Add(self.lblhear, pos=(8,0))
        self.edithear = wx.ComboBox(self, value="474",size=(95, -1), choices=self.sampleList7, style=wx.CB_DROPDOWN)
        self.grid_stream.Add(self.edithear, pos=(8,1))        
        self.Bind(wx.EVT_COMBOBOX, self.Evt_Stream_Freq, self.edithear)
        self.Bind(wx.EVT_TEXT, self.Evt_Stream_Freq,self.edithear)


        
        #hSizer.Add(self.button, 0, wx.CENTER)
        self.grid.Add(self.grid_box, pos=(2,0))
        self.grid.Add(self.grid_stream, pos=(4,0))
        self.grid.Add(self.grid_button, pos=(5,0))
        self.hSizer.Add(self.grid, 0, wx.ALL, 5)
        
        """
        #add case_group_button
        self.case = wx.GridSizer(1000,3,0,0)
        self.case_list = self.scan_case((os.getcwd()+'\caseInfo'+'\Case'),postfix='.conf')
        self.gs_case = wx.GridBagSizer()
        self.Add_case(self.case_list)
        self.gs_case.Add(self.case,pos=(0,0))
        self.hSizer.Add(self.gs_case)
        """
        
        
        
        #add logger window
        self.hSizer.Add(self.logger)
        self.Evt_Change_IR_MAP('libra2')
        

        #self.hSizer.Add(self.gs)
        
        #mainSizer.Add(self.gs, 0, wx.CENTER)
        self.mainSizer.Add(self.hSizer, 0, wx.CENTER, 5)
        self.s_key=sent_key.send_key()

        self.SetSizerAndFit(self.mainSizer)
        
       
    def scan_case(self,directory,prefix=None,postfix=None):  
        files_list=[]  
        for root, sub_dirs, files in os.walk(directory):  
            for special_file in files:  
                if postfix:  
                    if special_file.endswith(postfix):  
                        files_list.append(((special_file),(os.path.join(root,special_file))))  
                elif prefix:  
                    if special_file.startswith(prefix):  
                        files_list.append(((special_file),(os.path.join(root,special_file))))  
                else:  
                    files_list.append(((special_file),(os.path.join(root,special_file))))  
                            
            return files_list
    def EvtIP(self, event):
        #self.logger.AppendText('EvtIP: %s\n' % event.GetString())
        self.IP='%s' % event.GetString()
        #self.logger.AppendText('%s\n' % self.IP)
        

        
    def EvtPORT(self, event):
        #self.logger.AppendText('EvtIP: %s\n' % event.GetString())
        self.port='%s' % event.GetString()
        #self.logger.AppendText('%s\n' % self.port)   
        
    def EvtCARD(self, event):
        #self.logger.AppendText('EvtIP: %s\n' % event.GetString())
        self.card='%s' % event.GetString()
        #self.logger.AppendText('%s\n' % self.card)  
    
    def Evt_Stream_Std(self, event):
        self.Stream_Std='%s' % event.GetString()
    def Evt_Stream_File(self, event):
        self.Stream_File='%s' % event.GetString()  
    def Evt_Stream_Freq(self, event):
        self.Stream_Freq='%s' % event.GetString()
    def Evt_Stream_Bandwidth(self, event):
        self.Stream_Bandwidth='%s' % event.GetString()    
    def Evt_Stream_Modulation(self, event):
        self.Stream_Modulation='%s' % event.GetString()  
    def EvtRadioBox(self, event):
        self.logger.AppendText('%s' % event.GetString())
    def EvtComboBox(self, event):
        self.logger.AppendText('%s' % event.GetString())
        
    def OnClick(self,event,mark):
        if self.temtext:
            index_list=re.findall(r"Input_(.)",self.temtext)
            if index_list:
                self.position=self.logger.GetInsertionPoint()
                self.current_text=self.logger.GetRange(0,self.position)
                self.tag=self.current_text.split("\n")
                
                if self.tag[-2]:
                    print "~~~~~~~~~~~~~~~~~%s" % self.tag[-2]
                    if re.search('F*,',self.tag[-2]):
                        self.is_import=0
                        self.logger.WriteText("%s  ,  %s  ,  F  ,  1\n" % (mark, self.delay))
                        #if self.is_import:
                        #    self.logger.AppendText("[Input_%s]\nIRList=" % (str(self.key_index)))
                    if re.search("Input_(.)",self.tag[-2])or re.search('duration',self.tag[-2]):
                        self.logger.WriteText("IRList=%s  ,  %s  ,  F  ,  1\n" % (mark, self.delay))
        print self.delay
        self.is_import=1
        self.s_key.send_one_key(mark)
    def OnClick_SAVE(self,event):
        #self.s_key.send_one_key('MENU')
        #self.logger.AppendText(" Stream_ServerIp= %s\nStream_ServerPORT=%s\nCard_Type=%s\n" % (self.IP, self.port, self.card))
        print self.name
        main_dir=os.path.join(os.getcwd(),'caseInfo')
        if self.name=="caselist.txt":
            
            tmp_case=open(os.path.join(main_dir,'caselist.txt'),"wb")
            tmp_case.write(self.temtext)
            tmp_case.close
        else:
            case=open(os.path.join(main_dir,'Case',self.name),"wb")
            case.write(self.temtext)
            case.close
        
        
    def OnClick_Scan_case(self,event):
        
        self.case_list = self.scan_case((os.getcwd()+'\caseInfo'+'\Case'),postfix='.conf')

        
        
        """
        #refresh case button
        self.gs_case.Hide(self.case)
        self.gs_case.Remove(self.case)
        self.gs_case.Layout()
        
        self.case = wx.GridSizer(20,1,0,0)
        self.case_list = self.scan_case((os.getcwd()+'\caseInfo'+'\Case'),postfix='.conf')
        self.Add_case(self.case_list)
        
        self.gs_case.Add(self.case,pos=(0,0))
        self.hSizer.Layout()
        """
    
        #add cast list to caselist.txt
        #f = open(os.path.join(main_dir,'caselist.txt'),"a")
        #f.truncate()
        self.editname.Clear()
        self.editname.AppendText('%s' % 'caselist.txt')
        self.logger.Clear()
        for i in self.case_list:
            self.logger.AppendText(i[0]+"\n")
        #f.close()
    
    """
    def OnClick_Del(self,event):
        print self.name
        file_dir=os.path.join(os.getcwd(),'caseInfo','Case',self.name)
        print file_dir
        os.remove (file_dir)
        #refresh case button
        self.gs_case.Hide(self.case)
        self.gs_case.Remove(self.case)
        
        self.case = wx.GridSizer(20,1,0,0)
        self.case_list = self.scan_case((os.getcwd()+'\caseInfo'+'\Case'),postfix='.conf')
        self.Add_case(self.case_list)
        
        self.gs_case.Add(self.case,pos=(0,0))
        self.hSizer.Layout()
    """
    def Choose_file(self,event):

        dialog = wx.FileDialog(self,"Open file...",os.getcwd(),style=wx.OPEN,wildcard="*.bmp")
        if dialog.ShowModal() == wx.ID_OK:
            self.filepath.append(dialog.GetPath())
            self.filename.append(dialog.GetPath().split('\\')[-1])
            print self.filename[-1]
            self.logger.AppendText("bmpFile=%s\n" % (self.filename[-1]))
            self.is_import=1 
        dialog.Destroy()
        os.system ("copy %s %s" % (self.filepath[-1], os.path.join(self.main_path,'caseInfo', 'Case_pic')))


    def Choose_ircase_file(self,event):

        dialog = wx.FileDialog(self,"Open file...",os.getcwd(),style=wx.OPEN,wildcard="*.ircase")
        if dialog.ShowModal() == wx.ID_OK:
            
            filename=(dialog.GetPath().split('\\')[-1])
            print self.filename
            self.logger.AppendText("[Input_%s]\nIRFile=%s\n" % (str(self.key_index-1),filename))
            self.is_import=1 
        dialog.Destroy()
    
    def Choose_ts_file(self,event):

        #dialog = wx.FileDialog(self,"Open file...",os.getcwd(),style=wx.OPEN,wildcard="TS files (*.ts)|*.ts|TRP files (*.trp)|*.trp")
        #dialog = wx.FileDialog(self,"Open file...",defaultDir="//bjfile02/BJShare/Public/TS",style=wx.OPEN,wildcard="TS files (*.ts)|*.ts|TRP files (*.trp)|*.trp")
        dialog = wx.FileDialog(self,"Open file...",defaultDir="//bjfile02/BJShare/Department/FAE/Soc/AVL8332/Stream/DTMB",style=wx.OPEN,wildcard="TS files (*.ts)|*.ts|TRP files (*.trp)|*.trp")

        if dialog.ShowModal() == wx.ID_OK:
            
            filename=(dialog.GetPath())
            print self.filename
            #self.logger.AppendText("[Input_%s]\nIRFile=%s\n" % (str(self.key_index-1),filename))
            self.tsfile.Clear()
            self.tsfile.AppendText('%s' % filename)
 
        dialog.Destroy()
    

    def OnClick_Open_case(self,event):
        default_pwd="caseInfo/Case"
        dialog = wx.FileDialog(self,"Open file...",defaultDir=default_pwd,style=wx.OPEN,wildcard="conf files (*.conf)|*.conf|all files (*.*)|*.*")
        if dialog.ShowModal() == wx.ID_OK:
            filepath=(dialog.GetPath())
            filename=(dialog.GetPath().split('\\')[-1])
            
        #filename.SetValue(filepath)
            print filepath
            f = open(filepath,"rb")
            print f
            content=f.read()
            
            
            
            self.editname.Clear()
            self.editname.AppendText('%s' % filename)
            self.logger.Clear()
            
            self.logger.AppendText("%s" % content)
            print '~~~~~~~~~~~~'
            print content
            f.close()
            
        dialog.Destroy()
            
            
    def OnClick_Open_case_list(self,event):
       
        dialog = wx.FileDialog(self,"Open file...",defaultDir="caseInfo",style=wx.OPEN,wildcard="*.txt")
        if dialog.ShowModal() == wx.ID_OK:
            filepath=(dialog.GetPath())
            filename=(dialog.GetPath().split('\\')[-1])
            
        #filename.SetValue(filepath)
            print filepath
            f = open(filepath,"rb")
            print f
            content=f.read()
            
            
            
            self.editname.Clear()
            self.editname.AppendText('%s' % filename)
            self.logger.Clear()
            
            self.logger.AppendText("%s" % content)
            print '~~~~~~~~~~~~'
            print content
            f.close()
            
        dialog.Destroy()           
            #fopen = open(self.filepath)
            #fcontent = fopen.read()
            #self.logger.AppendText("%s" % fcontent)

            #contents.SetValue(fcontent)
            #fopen.close()
    def mem_file(self,event):

        self.logger.AppendText("cmdfile=meminfo.txt\n");
    def EvtText(self, event):
        self.delay='%s' % event.GetString()
        #self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    
    """   
    def Evt_test_type(self,event):
        if self.TT_TAG==1:
            self.Evt_Change_IR_MAP(self.rb.GetItemLabel(self.rb.GetSelection()))
            
            
        if event.GetString()=='run_case':
            self.case = wx.GridSizer(20,1,0,0)
            
            #self.hSizer.Hide(self.gs)
            #self.hSizer.Remove(self.gs)        
        
            #self.hSizer.Layout()
            
            
            #self.gs_case = wx.GridBagSizer()
            #self.Add_case(self.case_list)
            #self.gs_case.Add(self.case,pos=(0,0))
            #self.hSizer.Add(self.gs_case)
            
            self.hSizer.Layout()
            self.TT_TAG=1
        elif event.GetString()=='mem_test':
            self.logger.Clear()
            self.logger.AppendText('[Input_1]\ncommand=meminfo\nduration=600\n')
            
        elif event.GetString()=='normal_test':
            self.logger.Clear()
            #self.Evt_Change_IR_MAP(self.rb.GetItemLabel(self.rb.GetSelection()))
        """

    def Evt_Change_IR_MAP(self, event):
        self.TT_TAG=0
        globalVariable.IRK_MAP = {}
        #parseIrkey.ParseIrkey.insertIrk2Map()
        self.B1=[]
        self.B2=[]
        self.B3=[]
        self.B4=[] 
        self.B5=[] 
        self.B6=[]  
        self.B7=[] 

        if isinstance(event, wx._core.CommandEvent):
            globalVariable.serial_config['target_type'] = ('%s' % event.GetString())


            #print event.GetString()
        else: 
            globalVariable.serial_config['target_type'] = ('%s' % event)
            #print event
            #ADD GS      
        
        
        self.hSizer.Hide(self.gs)
        self.hSizer.Remove(self.gs)     
  
        self.hSizer.Layout()
        
        globalVariable.IRK_MAP = {}
        parseIrkey.ParseIrkey() 
        N=globalVariable.IRK_MAP
        M=self.sort_IRK_MAP(N)

        self.gs = wx.GridBagSizer()
        self.gs1 = wx.GridBagSizer(1,3)
        self.gs2 = wx.GridBagSizer(5,3)
        self.gs3 = wx.GridBagSizer(5,3)
        self.gs4 = wx.GridBagSizer(4,3)
        self.gs5 = wx.GridSizer(1,3,0,3)
        self.gs6 = wx.GridSizer(2,3,0,3)
        self.gs7 = wx.GridSizer(20,3,0,3)
        self.grid_delay = wx.GridBagSizer(hgap=5, vgap=5)
        self.grid_tool = wx.GridBagSizer(hgap=5, vgap=5)


        
        self.Add_button(self.B1)
        self.Add_button2(self.B2)
        self.Add_button3(self.B3)
        self.Add_button4(self.B4)
        self.Add_button5(self.B5)
        self.Add_button6(self.B6)
        self.Add_button7(self.B7)
        self.Add_tool_button()
        self.Add_grid_delay()
        
        self.gs.Add(self.grid_tool,pos=(0,0))
        self.gs.Add(self.grid_delay,pos=(1,0))
        self.gs.Add(self.gs1,pos=(2,0))
        self.gs.Add(self.gs2,pos=(3,0))
        self.gs.Add(self.gs3,pos=(5,0))
        self.gs.Add(self.gs4,pos=(4,0))
        self.gs.Add(self.gs5,pos=(6,0))
        self.gs.Add(self.gs6,pos=(7,0))
        self.gs.Add(self.gs7,pos=(8,0))
        self.hSizer.Add(self.gs)

        self.hSizer.Layout()
    
    def Add_case(self,M):
        
        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(50, 20))

            #self.btn.SetBackgroundColour("gray")
            #self.btn.SetForegroundColour("white")    
  
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i : self.Run_Case(evt,mark) ,self.btn )
            self.case.Add(self.btn, 0, wx.EXPAND)
    def Add_grid_delay(self):
        #delay time
        self.lblname = wx.StaticText(self, label="delay time :")
        self.grid_delay.Add(self.lblname, pos=(0,0))
        self.delay_box = wx.TextCtrl(self, value="1000", size=(140,-1))
        self.grid_delay.Add(self.delay_box, pos=(0,1))
        self.Bind(wx.EVT_TEXT, self.EvtText, self.delay_box)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.delay_box)
    def Add_tool_button(self):


        self.btn=wx.Button(self, label='input',size=(70, 22))
        self.Bind(wx.EVT_BUTTON, lambda evt,mark='[Input_1]\n':self.OnClick_tool(evt,mark) ,self.btn )
        self.grid_tool.Add(self.btn, pos=(0,0))
        self.btn=wx.Button(self, label='output',size=(70, 22))    
        self.Bind(wx.EVT_BUTTON, lambda evt,mark='[Output_1]\n':self.OnClick_tool(evt,mark) ,self.btn )
        self.grid_tool.Add(self.btn, pos=(1,0))
        self.btn=wx.Button(self, label='meminfo',size=(70, 22))    
        self.Bind(wx.EVT_BUTTON, lambda evt,mark='command=meminfo\nduration=600\n':self.OnClick_tool(evt,mark) ,self.btn )
        self.grid_tool.Add(self.btn, pos=(0,1))
        
        #file button
        self.button_file =wx.Button(self, label="BMP FILE",size=(70, 22))        
        self.Bind(wx.EVT_BUTTON, self.Choose_file,self.button_file)
        self.grid_tool.Add(self.button_file, pos=(1,2), span=(1,1)) 
        
        #ircase file button
        self.button_file =wx.Button(self, label="ircase FILE",size=(70, 22))        
        self.Bind(wx.EVT_BUTTON, self.Choose_ircase_file,self.button_file)
        self.grid_tool.Add(self.button_file, pos=(0,2), span=(1,1))  
        
        #mem file button
        self.button_mem =wx.Button(self, label="mem_file",size=(70, 22))        
        self.Bind(wx.EVT_BUTTON, self.mem_file,self.button_mem)
        self.grid_tool.Add(self.button_mem, pos=(1,1), span=(1,1))
  
    def Add_button(self,M):

        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(70, 22))
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i[0] : self.OnClick(evt,mark) ,self.btn )
            if i[0]=="POWER":
                self.gs1.Add(self.btn, pos=(0,0))
            if i[0]=="MUTE":
                self.gs1.Add(self.btn, pos=(0,2))
        #self.btn=wx.Button(self, label="") 
        self.btn=(wx.StaticText(self))
        self.gs1.Add(self.btn, pos=(0,1),flag=wx.RIGHT, border=70)
            #self.btn.SetBackgroundColour("Navy")
            
            
            
    def Add_button2(self,M):

        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(70, 22))
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i[0] : self.OnClick(evt,mark) ,self.btn )
            if re.match(r'[1-9]',i[0]):
                self.gs2.Add(self.btn, pos=((int(i[0])-1)/3,(int(i[0])-1)%3))
                #self.btn.SetBackgroundColour("Black")
            if re.match(r'0',i[0]):
                self.gs2.Add(self.btn, pos=(3,1))
            if re.match(r'[pP][gG]\+',i[0]) or re.match(r'PgUp\+',i[0]):
                self.gs2.Add(self.btn, pos=(3,0))
            if re.match(r'[pP][gG]-',i[0]) or re.match(r'PgDn-',i[0]):
                self.gs2.Add(self.btn, pos=(3,2))
                    

            self.btn.SetForegroundColour("orange")
             
    
    def Add_button3(self,M):

        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(70, 22))
            #self.btn.SetBackgroundColour("Blue")
            #self.btn.SetForegroundColour("white")    
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i[0] : self.OnClick(evt,mark) ,self.btn )
            if i[0]=="RED":
                self.gs3.Add(self.btn, pos=(0,1))
                self.btn.SetBackgroundColour("RED")
            if i[0]=="GREEN":
                self.gs3.Add(self.btn, pos=(1,1))
                self.btn.SetBackgroundColour("GREEN")
            if i[0]=="YELLOW":
                self.gs3.Add(self.btn, pos=(2,1))
                self.btn.SetBackgroundColour("YELLOW")
            if i[0]=="BLUE":
                self.gs3.Add(self.btn, pos=(3,1))
                self.btn.SetBackgroundColour("BLUE")
                self.btn.SetForegroundColour("white") 
            if i[0]=="VOL+":
                self.gs3.Add(self.btn, pos=(0,0))
            if i[0]=="VOL-":
                self.gs3.Add(self.btn, pos=(0,2))
            if i[0]=="CH+":
                self.gs3.Add(self.btn, pos=(1,0))
            if i[0]=="CH-":
                self.gs3.Add(self.btn, pos=(1,2))

            if re.match(r'[tT][oO][Ee][nN][Dd]',i[0]) or re.match(r'>>\|',i[0]):
                self.gs3.Add(self.btn, pos=(2,0))
            if re.match(r'[Bb][sS][tT][Aa][Rr][tT]',i[0]) or re.match(r'\|<<',i[0]):
                self.gs3.Add(self.btn, pos=(2,2))
            if re.match(r'QPLAY',i[0]) or i[0]=='>>':
                self.gs3.Add(self.btn, pos=(3,0))
            if re.match(r'QBACK',i[0]) or i[0]=='<<':
                self.gs3.Add(self.btn, pos=(3,2))
        self.btn=(wx.StaticText(self))
        self.gs3.Add(self.btn, pos=(4,0),flag=wx.RIGHT, border=70)
    def Add_button4(self,M):

        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(70, 22))
            self.btn.SetBackgroundColour("Gray")
            self.btn.SetForegroundColour("white")    
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i[0] : self.OnClick(evt,mark) ,self.btn )
            if i[0]=="UP":
                self.gs4.Add(self.btn,pos=(0,1))
                self.btn.SetBackgroundColour("Black")
            if i[0]=="DOWN":
                self.gs4.Add(self.btn,pos=(2,1))
                self.btn.SetBackgroundColour("Black")

            if i[0]=="LEFT":
                self.gs4.Add(self.btn,pos=(1,0))
                self.btn.SetBackgroundColour("Black")
            if i[0]=="RIGHT":
                self.gs4.Add(self.btn,pos=(1,2))
                self.btn.SetBackgroundColour("Black")
            if i[0]=="OK":
                self.gs4.Add(self.btn,pos=(1,1))
                self.btn.SetBackgroundColour("Black")
            if i[0]=="MENU":
                self.gs4.Add(self.btn,pos=(0,0))
            if i[0]=="EXIT":
                self.gs4.Add(self.btn,pos=(0,2))
            if re.match(r'[iI][nN][fF][oO]',i[0]):
                self.gs4.Add(self.btn,pos=(2,0))
            if re.match(r'DVR',i[0]) or re.match(r'[sS][aA][Tt]',i[0]):
                self.gs4.Add(self.btn,pos=(2,2))
                
    def Add_button5(self,M):

        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(70, 22))
            self.btn.SetBackgroundColour("gray")
            self.btn.SetForegroundColour("black")    
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i[0] : self.OnClick(evt,mark) ,self.btn )
            self.gs5.Add(self.btn, 0, wx.EXPAND)
            
    def Add_button6(self,M):

        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(70, 22))
            self.btn.SetBackgroundColour("gray")
            if re.search(r'^[rR][Ee][cC]$',i[0]):
                self.btn.SetForegroundColour("orange")            
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i[0] : self.OnClick(evt,mark) ,self.btn )
            self.gs6.Add(self.btn, 0, wx.EXPAND)
    def Add_button7(self,M):

        for i in M:
            self.btn=wx.Button(self, label=i[0].lstrip(),size=(70, 22))
            #self.btn.SetBackgroundColour("Gray")
            #self.btn.SetForegroundColour("white")    
            self.Bind(wx.EVT_BUTTON, lambda evt, mark=i[0] : self.OnClick(evt,mark) ,self.btn )
            self.gs7.Add(self.btn, 0, wx.EXPAND)

    def sort_IRK_MAP(self,N):
        #SORT THE DIR IR KEY

        M=sorted(N.iteritems(), key = lambda asd:asd[0] )
        for i in M:
            if re.match(r'[pP][gG]',i[0]):
                #print i[0]
                self.B2.append(i)
                
                

            elif re.match(r'[tT][oO][Ee][nN][Dd]',i[0]) or re.match(r'>>\|',i[0]):
                print i[0]
                self.B3.append(i)

            elif re.match(r'[Bb][sS][tT][Aa][Rr][tT]',i[0]) or re.match(r'\|<<',i[0]):
                #print i[0]
                self.B3.append(i)
                

            elif re.match(r'QPLAY',i[0]) or i[0]=='>>' or re.match(r'QBACK',i[0]) or i[0]=='<<':
                #print i[0]
                self.B3.append(i)   
                
                
                
                
            elif re.match(r'VOL+',i[0]) or re.match(r'VOL-',i[0]):
                #print i[0]
                self.B3.append(i)


            elif re.match(r'CH-',i[0]) or re.match(r'CH+',i[0]):
                self.B3.append(i)  
            elif i[0]=="MENU" or i[0]=="EXIT"  or re.match(r'[iI][nN][fF][oO]',i[0]) or i[0]=="DVR" or re.match(r'[Ss][aA][tT]',i[0]):
                self.B4.append(i)
            elif i[0]=="UP" or i[0]=="DOWN" or i[0]=="LEFT" or i[0]=="RIGHT" or i[0]=="OK" :
                self.B4.append(i)
            elif i[0]=="RED" or i[0]=="GREEN" or i[0]=="BLUE" or i[0]=="YELLOW":
                self.B3.append(i)

            elif re.match(r'POWER',i[0]) or re.match(r'MUTE',i[0]):
                self.B1.append(i)
            elif re.match(r'[sS][tT][oO][pP]',i[0]) or re.match(r'[pP][lL][aA][yY]',i[0]) or re.match(r'[pP][aA][uU][sS][eE]',i[0]) or re.match(r'[Ss][tT][Aa][rR][tT]',i[0]):          
                self.B5.append(i)
            elif re.match(r'[aA][Uu][dD][Ii][oO]',i[0]) or re.match(r'[Tt][vV]/[rR]',i[0]) or re.match(r'[eE][Pp][gG]',i[0]) or re.search(r'[lL][Ii][sS][Tt]',i[0])or re.search(r'[Rr][Ee][Cc]',i[0])or re.search(r'[fF][Ii][nN][dD]',i[0]):          
                self.B6.append(i)
            elif re.match(r'[0-9]',i[0]):
                self.B2.append(i)
            else:
                self.B7.append(i)
        for i in self.B2:
            print i
        return M  
    def BoxText(self, event):
        self.temtext='%s' % event.GetString()
        
    
    def OnClick_stream(self,event):
        self.logger.AppendText("[Stream_1]\nStream_ServerIp= %s\nStream_ServerPORT=%s\nCard_Type=%s\nStream_Std=%s\nStream_File=%s\nStream_Freq=%s\nStream_Bandwidth=%s\nStream_Modulation=%s\n" % (self.IP, self.port, self.card,self.Stream_Std,self.Stream_File,self.Stream_Freq,self.Stream_Bandwidth,self.Stream_Modulation))
        self.is_import=1
    def OnClick_tool(self,event,mark):

        self.logger.AppendText("%s" % mark)
        #self.logger.AppendText("aaaa")
    def EvtName(self, event):
        self.name='%s' % event.GetString()
    def start_case(self, event):
        sent_key.main().main()
    def video_cap(self, event):    
        wx.Execute('VideoCapture.exe')
    def format_file(self,event):
        
        
        #all_lines = self.temtext.readlines()    
        all_lines = self.temtext.split("\n")
        print all_lines
        def findkeyline(strline):
            regex=re.compile(r'\[.*\]')
            if re.search(regex, strline):
                return True
            else:
                return False
        all_list = filter(findkeyline, all_lines)
        #print all_list
        n=0
        for ll in all_list:
            n += 1
            if(n>=len(all_list)):
                break
            #print ll[0].upper(),all_list[n][0].upper()
            if re.search(r"STREAM", ll.upper()):
                pattern=re.compile(r'STREAM|INPUT|SOUTPUT')
                if pattern.search(all_list[n].upper()):
                    pass
                else:
                    print 'line: ', all_list[n], ' with errors!'
                    return False
            elif re.search(r"SOUTPUT", ll.upper()):
                pattern=re.compile(r'STREAM|INPUT')
                if pattern.search(all_list[n].upper()):
                    pass
                else:
                    print 'line: ', all_list[n], ' with errors!'
                    return False
            elif re.search(r"INPUT", ll.upper()):
                pattern=re.compile(r'OUTPUT')
                if pattern.search(all_list[n].upper()):
                    pass
                else:
                    print 'line: ', all_list[n], ' with errors!'
                    return False
            elif re.search(r"OUTPUT", ll.upper()):
                pattern=re.compile(r'STREAM|INPUT')
                if pattern.search(all_list[n].upper()):
                    pass
                else:
                    print 'line: ', all_list[n], ' with errors!'
                    return False       
        print "check case file success!"  
        
        stream_num=0
        input_num=0
        new_lines=''
        for line in all_lines:
            new='';
            if re.search(r"\[STREAM", line.upper()):
                stream_num += 1
                if re.search(r'_', line):
                    new = "%s_%d]\n"%(line.split('_')[0],stream_num)
                else:
                    new = "%s_%d]\n"%(line.split(']')[0],stream_num)
            elif re.search(r"\[SOUTPUT", line.upper()):
                if re.search(r'_', line):
                    new = "%s_%d]\n"%(line.split('_')[0],stream_num)
                else:
                    new = "%s_%d]\n"%(line.split(']')[0],stream_num)
            elif re.search(r"\[INPUT", line.upper()):
                input_num += 1
                if re.search(r'_', line):
                    new = "%s_%d]\n"%(line.split('_')[0],input_num)
                else:
                    new = "%s_%d]\n"%(line.split(']')[0],input_num)
            elif re.search(r"\[OUTPUT", line.upper()):
                if re.search(r'_', line):
                    new = "%s_%d]\n"%(line.split('_')[0],input_num)
                else:
                    new = "%s_%d]\n"%(line.split(']')[0],input_num)
            else:
                new = line+'\n'
        
            new_lines += new
            
    
        print "format case file success!"  
        print new_lines
        #return new_lines
        self.logger.Clear()
        self.logger.AppendText("%s" % new_lines)
    """
    def format_case(self, event):    
        
        format_file=os.path.join(os.getcwd(),'caseInfo','Case',self.name)
        #wx.Execute('python %s %s' % (format_tool,self.name))
        format_fun=format_case.format_case()
        
        format_fun.format_file(format_file)
        f = open(format_file,"rb")
        print f
        content=f.read()

        self.logger.Clear()
        
        self.logger.AppendText("%s" % content)
        print '~~~~~~~~~~~~'
        print content
        f.close()
        #print format_tool
        """
    def Run_Case(self,event,mark):
        print mark[1]
        self.editname.Clear()
        self.editname.AppendText('%s' % mark[0])
        case=open(mark[1],"rb")
        case_content=case.read()
        case.close
        self.logger.Clear()
        self.logger.AppendText(case_content)
    
app = wx.App()
frame = wx.Frame(None,size=(800,630),pos=(0,0))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()