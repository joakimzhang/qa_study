r'''Parse configure file
This functions:
  --  readConfigFile ()
'''

import ConfigParser
import os,sys

import globalVariable


class ParseIrkey(object):


    def __init__(self):

        self.irkey_file = 'irKey.cfg'
        if globalVariable.serial_config['target_type'] == 'libra2':
            self.section = 'Libra2'
        elif globalVariable.serial_config['target_type'] == 'librasd':
            self.section = 'Gospell'
        elif globalVariable.serial_config['target_type'] == 'Sunplus':
            self.section = 'Sunplus'
        elif globalVariable.serial_config['target_type'] == 'SaiKeDa':
            self.section = 'SaiKeDa'
        
        self.irkey_abspath = os.path.join(os.getcwd(),
                                          'caseInfo',
                                          'irkey',
                                          self.irkey_file)
        
        self.config = ConfigParser.ConfigParser()
        
        try:
            self.cfg_fp = open(self.irkey_abspath,"r")
            self.config.readfp(self.cfg_fp)
        except Exception,e:
            print e
            sys.exit(-1)
        
        self.insertIrk2Map(self.section)
        
        

    def parseConfigItem(self, section, item, item_type='get'):
        if self.config.has_section(section):
            if self.config.has_option(section, item):
                    return getattr(self.config, item_type)(section, item)
            else:
                return False
        else:
            False

    def insertIrk2Map(self, section):
        if section=='Gospell':
            sys_code = self.parseConfigItem(self.section,'System').split(':')[0]

            power_code = self.parseConfigItem(self.section,'POWER').split(':')[0]
        
            code_1 = self.parseConfigItem(self.section,'1').split(':')[0]
            code_2 = self.parseConfigItem(self.section,'2').split(':')[0]
            code_3 = self.parseConfigItem(self.section,'3').split(':')[0]
            code_4 = self.parseConfigItem(self.section,'4').split(':')[0]
            code_5 = self.parseConfigItem(self.section,'5').split(':')[0]
            code_6 = self.parseConfigItem(self.section,'6').split(':')[0]
            code_7 = self.parseConfigItem(self.section,'7').split(':')[0]
            code_8 = self.parseConfigItem(self.section,'8').split(':')[0]
            code_9 = self.parseConfigItem(self.section,'9').split(':')[0]
            code_0 = self.parseConfigItem(self.section,'0').split(':')[0]
        
            #pgup_code = self.parseConfigItem(self.section,'PgUp+').split(':')[0]
            #pgdn_code = self.parseConfigItem(self.section,'PgDn-').split(':')[0]
            pgup_code = self.parseConfigItem(self.section,'PG+').split(':')[0]
            pgdn_code = self.parseConfigItem(self.section,'PG-').split(':')[0]
        
            menu_code = self.parseConfigItem(self.section,'MENU').split(':')[0]
            exit_code = self.parseConfigItem(self.section,'EXIT').split(':')[0]
        
            up_code = self.parseConfigItem(self.section,'UP').split(':')[0]
            dn_code = self.parseConfigItem(self.section,'DOWN').split(':')[0]
            left_code = self.parseConfigItem(self.section,'LEFT').split(':')[0]
            right_code = self.parseConfigItem(self.section,'RIGHT').split(':')[0]
        
            ok_code = self.parseConfigItem(self.section,'OK').split(':')[0]
            info_code = self.parseConfigItem(self.section,'Info').split(':')[0]
            #dvr_code = self.parseConfigItem(self.section,'DVR').split(':')[0]

            #vol_plus_code = self.parseConfigItem(self.section,'VOL+').split(':')[0]
            #vol_minus_code = self.parseConfigItem(self.section,'VOL-').split(':')[0]
        
            #list_code = self.parseConfigItem(self.section,'LIST').split(':')[0]
            #back_code = self.parseConfigItem(self.section,'BACK').split(':')[0]
        
            red_code = self.parseConfigItem(self.section,'RED').split(':')[0]
            green_code = self.parseConfigItem(self.section,'GREEN').split(':')[0]
            yellow_code = self.parseConfigItem(self.section,'YELLOW').split(':')[0]
            blue_code = self.parseConfigItem(self.section,'BLUE').split(':')[0]
        
            #ch_plus_code = self.parseConfigItem(self.section,'CH+').split(':')[0]
            #ch_minus_code = self.parseConfigItem(self.section,'CH-').split(':')[0]
        
            epg_code = self.parseConfigItem(self.section,'EPG').split(':')[0]
            #time_code = self.parseConfigItem(self.section,'TIMER').split(':')[0]
            #media_code = self.parseConfigItem(self.section,'MEDIA').split(':')[0]
            #reclist_code = self.parseConfigItem(self.section,'RECLIST').split(':')[0]
            audio_code = self.parseConfigItem(self.section,'AUDIO').split(':')[0]
            tv_radio_code = self.parseConfigItem(self.section,'TV/R').split(':')[0]
            mute_code = self.parseConfigItem(self.section,'MUTE').split(':')[0]
            #subt_code = self.parseConfigItem(self.section,'SUBT').split(':')[0]
            #vformat_code = self.parseConfigItem(self.section,'V.Format').split(':')[0]
        
            zoom_code = self.parseConfigItem(self.section,'ZOOM').split(':')[0]
            ttx_code = self.parseConfigItem(self.section,'TTX').split(':')[0]
            pav_code = self.parseConfigItem(self.section,'FAV').split(':')[0]
            find_code = self.parseConfigItem(self.section,'FIND').split(':')[0]
        
            play_code = self.parseConfigItem(self.section,'REPLAY&START').split(':')[0]
            pause_code = self.parseConfigItem(self.section,'PAUSE').split(':')[0]
            stop_code = self.parseConfigItem(self.section,'STOP').split(':')[0]
            sleep_code = self.parseConfigItem(self.section,'IGNORE').split(':')[0]
            switch_code = self.parseConfigItem(self.section,'SWITCH').split(':')[0]
            start_code = self.parseConfigItem(self.section,'START').split(':')[0]
            single_code = self.parseConfigItem(self.section,'SINGLE').split(':')[0]
            

            globalVariable.IRK_MAP['System'] = int(sys_code.strip(), 16)
            globalVariable.IRK_MAP['POWER']  = int(power_code.strip(), 16)
            globalVariable.IRK_MAP['1']      = int(code_1.strip(), 16)
            globalVariable.IRK_MAP['2']      = int(code_2.strip(), 16)
            globalVariable.IRK_MAP['3']      = int(code_3.strip(), 16)
            globalVariable.IRK_MAP['4']      = int(code_4.strip(), 16)
            globalVariable.IRK_MAP['5']      = int(code_5.strip(), 16)
            globalVariable.IRK_MAP['6']      = int(code_6.strip(), 16)
            globalVariable.IRK_MAP['7']      = int(code_7.strip(), 16)
            globalVariable.IRK_MAP['8']      = int(code_8.strip(), 16)
            globalVariable.IRK_MAP['9']      = int(code_9.strip(), 16)
            globalVariable.IRK_MAP['0']      = int(code_0.strip(), 16)
            globalVariable.IRK_MAP['PG+']  = int(pgup_code.strip(), 16)
            globalVariable.IRK_MAP['PG-']  = int(pgdn_code.strip(), 16)
            globalVariable.IRK_MAP['MENU']   = int(menu_code.strip(), 16)
            globalVariable.IRK_MAP['EXIT']   = int(exit_code.strip(), 16)
            globalVariable.IRK_MAP['UP']     = int(up_code.strip(), 16)
            globalVariable.IRK_MAP['DOWN']   = int(dn_code.strip(), 16)
            globalVariable.IRK_MAP['LEFT']   = int(left_code.strip(), 16)
            globalVariable.IRK_MAP['RIGHT']  = int(right_code.strip(), 16)
            globalVariable.IRK_MAP['OK']     = int(ok_code.strip(), 16)
            globalVariable.IRK_MAP['INFO']   = int(info_code.strip(), 16)
            #globalVariable.IRK_MAP['DVR']    = int(dvr_code.strip(), 16)
            #globalVariable.IRK_MAP['VOL+']   = int(vol_plus_code.strip(), 16)
            #globalVariable.IRK_MAP['VOL-']   = int(vol_minus_code.strip(), 16)
            #globalVariable.IRK_MAP['LIST']   = int(list_code.strip(), 16)
            #globalVariable.IRK_MAP['BACK']   = int(back_code.strip(), 16)
            globalVariable.IRK_MAP['RED']    = int(red_code.strip(), 16)
            globalVariable.IRK_MAP['GREEN']  = int(green_code.strip(), 16)
            globalVariable.IRK_MAP['YELLOW'] = int(yellow_code.strip(), 16)
            globalVariable.IRK_MAP['BLUE']   = int(blue_code.strip(), 16)
            #globalVariable.IRK_MAP['CH+']    = int(ch_plus_code.strip(), 16)
            #globalVariable.IRK_MAP['CH-']    = int(ch_minus_code.strip(), 16)
            globalVariable.IRK_MAP['EPG']    = int(epg_code.strip(), 16)
            #globalVariable.IRK_MAP['TIMER']  = int(time_code.strip(), 16)
            #globalVariable.IRK_MAP['MEDIA']  = int(media_code.strip(), 16)
            #globalVariable.IRK_MAP['RECLIST']        = int(reclist_code.strip(), 16)
            globalVariable.IRK_MAP['AUDIO']  = int(audio_code.strip(), 16)
            globalVariable.IRK_MAP['TV/R']       = int(tv_radio_code.strip(), 16)
            globalVariable.IRK_MAP['MUTE']   = int(mute_code.strip(), 16)
            #globalVariable.IRK_MAP['SUBT']   = int(subt_code.strip(), 16)
            #globalVariable.IRK_MAP['V.Format']  = int(vformat_code.strip(), 16)
            globalVariable.IRK_MAP['ZOOM']   = int(zoom_code.strip(), 16)
            globalVariable.IRK_MAP['TTX']    = int(ttx_code.strip(), 16)
            globalVariable.IRK_MAP['FAV']    = int(pav_code.strip(), 16)
            globalVariable.IRK_MAP['FIND']   = int(find_code.strip(), 16)
            globalVariable.IRK_MAP['REPLAY&START']   = int(play_code.strip(), 16)
            globalVariable.IRK_MAP['PAUSE']  = int(pause_code.strip(), 16)
            globalVariable.IRK_MAP['STOP']   = int(stop_code.strip(), 16)
            globalVariable.IRK_MAP['IGNORE']  = int(sleep_code.strip(), 16)
            globalVariable.IRK_MAP['SWITCH']  = int(switch_code.strip(), 16)
            globalVariable.IRK_MAP['START']  = int(start_code.strip(), 16)
            globalVariable.IRK_MAP['SINGLE']  = int(single_code.strip(), 16)
            #print globalVariable.IRK_MAP['System']
        elif section=='Libra2':
            sys_code = self.parseConfigItem(self.section,'System').split(':')[0]

            power_code = self.parseConfigItem(self.section,'POWER').split(':')[0]
        
            code_1 = self.parseConfigItem(self.section,'1').split(':')[0]
            code_2 = self.parseConfigItem(self.section,'2').split(':')[0]
            code_3 = self.parseConfigItem(self.section,'3').split(':')[0]
            code_4 = self.parseConfigItem(self.section,'4').split(':')[0]
            code_5 = self.parseConfigItem(self.section,'5').split(':')[0]
            code_6 = self.parseConfigItem(self.section,'6').split(':')[0]
            code_7 = self.parseConfigItem(self.section,'7').split(':')[0]
            code_8 = self.parseConfigItem(self.section,'8').split(':')[0]
            code_9 = self.parseConfigItem(self.section,'9').split(':')[0]
            code_0 = self.parseConfigItem(self.section,'0').split(':')[0]
        
            pgup_code = self.parseConfigItem(self.section,'PgUp+').split(':')[0]
            pgdn_code = self.parseConfigItem(self.section,'PgDn-').split(':')[0]
        
            menu_code = self.parseConfigItem(self.section,'MENU').split(':')[0]
            exit_code = self.parseConfigItem(self.section,'EXIT').split(':')[0]
        
            up_code = self.parseConfigItem(self.section,'UP').split(':')[0]
            dn_code = self.parseConfigItem(self.section,'DOWN').split(':')[0]
            left_code = self.parseConfigItem(self.section,'LEFT').split(':')[0]
            right_code = self.parseConfigItem(self.section,'RIGHT').split(':')[0]
        
            ok_code = self.parseConfigItem(self.section,'OK').split(':')[0]
            info_code = self.parseConfigItem(self.section,'Info').split(':')[0]
            dvr_code = self.parseConfigItem(self.section,'DVR').split(':')[0]

            vol_plus_code = self.parseConfigItem(self.section,'VOL+').split(':')[0]
            vol_minus_code = self.parseConfigItem(self.section,'VOL-').split(':')[0]
        
            list_code = self.parseConfigItem(self.section,'LIST').split(':')[0]
            back_code = self.parseConfigItem(self.section,'BACK').split(':')[0]
        
            red_code = self.parseConfigItem(self.section,'RED').split(':')[0]
            green_code = self.parseConfigItem(self.section,'GREEN').split(':')[0]
            yellow_code = self.parseConfigItem(self.section,'YELLOW').split(':')[0]
            blue_code = self.parseConfigItem(self.section,'BLUE').split(':')[0]
        
            ch_plus_code = self.parseConfigItem(self.section,'CH+').split(':')[0]
            ch_minus_code = self.parseConfigItem(self.section,'CH-').split(':')[0]
        
            epg_code = self.parseConfigItem(self.section,'EPG').split(':')[0]
            time_code = self.parseConfigItem(self.section,'TIMER').split(':')[0]
            media_code = self.parseConfigItem(self.section,'MEDIA').split(':')[0]
            reclist_code = self.parseConfigItem(self.section,'RECLIST').split(':')[0]
            audio_code = self.parseConfigItem(self.section,'AUDIO').split(':')[0]
            tv_radio_code = self.parseConfigItem(self.section,'TV/RADIO').split(':')[0]
            mute_code = self.parseConfigItem(self.section,'MUTE').split(':')[0]
            subt_code = self.parseConfigItem(self.section,'SUBT').split(':')[0]
            vformat_code = self.parseConfigItem(self.section,'V.Format').split(':')[0]
        
            zoom_code = self.parseConfigItem(self.section,'ZOOM').split(':')[0]
            ttx_code = self.parseConfigItem(self.section,'TTX').split(':')[0]
            pav_code = self.parseConfigItem(self.section,'FAV').split(':')[0]
            find_code = self.parseConfigItem(self.section,'FIND').split(':')[0]
        
            play_code = self.parseConfigItem(self.section,'PLAY').split(':')[0]
            pause_code = self.parseConfigItem(self.section,'PAUSE').split(':')[0]
            stop_code = self.parseConfigItem(self.section,'STOP').split(':')[0]
        
            qback_code = self.parseConfigItem(self.section,'QBACK').split(':')[0]
            qplay_code = self.parseConfigItem(self.section,'QPLAY').split(':')[0]
        
            rpoint_code = self.parseConfigItem(self.section,'RPoint').split(':')[0]
            bstart_code = self.parseConfigItem(self.section,'BSTART').split(':')[0]
        
            toend_code = self.parseConfigItem(self.section,'ToEND').split(':')[0]
            opt_code = self.parseConfigItem(self.section,'OPT').split(':')[0]

            sleep_code = self.parseConfigItem(self.section,'SLEEP').split(':')[0]
            dely_code = self.parseConfigItem(self.section,'DELAY').split(':')[0]


            globalVariable.IRK_MAP['System'] = int(sys_code.strip(), 16)
            globalVariable.IRK_MAP['POWER']  = int(power_code.strip(), 16)
            globalVariable.IRK_MAP['1']      = int(code_1.strip(), 16)
            globalVariable.IRK_MAP['2']      = int(code_2.strip(), 16)
            globalVariable.IRK_MAP['3']      = int(code_3.strip(), 16)
            globalVariable.IRK_MAP['4']      = int(code_4.strip(), 16)
            globalVariable.IRK_MAP['5']      = int(code_5.strip(), 16)
            globalVariable.IRK_MAP['6']      = int(code_6.strip(), 16)
            globalVariable.IRK_MAP['7']      = int(code_7.strip(), 16)
            globalVariable.IRK_MAP['8']      = int(code_8.strip(), 16)
            globalVariable.IRK_MAP['9']      = int(code_9.strip(), 16)
            globalVariable.IRK_MAP['0']      = int(code_0.strip(), 16)
            globalVariable.IRK_MAP['PgUp+']  = int(pgup_code.strip(), 16)
            globalVariable.IRK_MAP['PgDn-']  = int(pgdn_code.strip(), 16)
            globalVariable.IRK_MAP['MENU']   = int(menu_code.strip(), 16)
            globalVariable.IRK_MAP['EXIT']   = int(exit_code.strip(), 16)
            globalVariable.IRK_MAP['UP']     = int(up_code.strip(), 16)
            globalVariable.IRK_MAP['DOWN']   = int(dn_code.strip(), 16)
            globalVariable.IRK_MAP['LEFT']   = int(left_code.strip(), 16)
            globalVariable.IRK_MAP['RIGHT']  = int(right_code.strip(), 16)
            globalVariable.IRK_MAP['OK']     = int(ok_code.strip(), 16)
            globalVariable.IRK_MAP['Info']   = int(info_code.strip(), 16)
            globalVariable.IRK_MAP['DVR']    = int(dvr_code.strip(), 16)
            globalVariable.IRK_MAP['VOL+']   = int(vol_plus_code.strip(), 16)
            globalVariable.IRK_MAP['VOL-']   = int(vol_minus_code.strip(), 16)
            globalVariable.IRK_MAP['LIST']   = int(list_code.strip(), 16)
            globalVariable.IRK_MAP['BACK']   = int(back_code.strip(), 16)
            globalVariable.IRK_MAP['RED']    = int(red_code.strip(), 16)
            globalVariable.IRK_MAP['GREEN']  = int(green_code.strip(), 16)
            globalVariable.IRK_MAP['YELLOW'] = int(yellow_code.strip(), 16)
            globalVariable.IRK_MAP['BLUE']   = int(blue_code.strip(), 16)
            globalVariable.IRK_MAP['CH+']    = int(ch_plus_code.strip(), 16)
            globalVariable.IRK_MAP['CH-']    = int(ch_minus_code.strip(), 16)
            globalVariable.IRK_MAP['EPG']    = int(epg_code.strip(), 16)
            globalVariable.IRK_MAP['TIMER']  = int(time_code.strip(), 16)
            globalVariable.IRK_MAP['MEDIA']  = int(media_code.strip(), 16)
            globalVariable.IRK_MAP['RECLIST']= int(reclist_code.strip(), 16)
            globalVariable.IRK_MAP['AUDIO']  = int(audio_code.strip(), 16)
            globalVariable.IRK_MAP['TV/RADIO']= int(tv_radio_code.strip(), 16)
            globalVariable.IRK_MAP['MUTE']   = int(mute_code.strip(), 16)
            globalVariable.IRK_MAP['SUBT']   = int(subt_code.strip(), 16)
            globalVariable.IRK_MAP['V.Format']  = int(vformat_code.strip(), 16)
            globalVariable.IRK_MAP['ZOOM']   = int(zoom_code.strip(), 16)
            globalVariable.IRK_MAP['TTX']    = int(ttx_code.strip(), 16)
            globalVariable.IRK_MAP['FAV']    = int(pav_code.strip(), 16)
            globalVariable.IRK_MAP['FIND']   = int(find_code.strip(), 16)
            globalVariable.IRK_MAP['PLAY']   = int(play_code.strip(), 16)
            globalVariable.IRK_MAP['PAUSE']  = int(pause_code.strip(), 16)
            globalVariable.IRK_MAP['STOP']   = int(stop_code.strip(), 16)
            globalVariable.IRK_MAP['QBACK']  = int(qback_code.strip(), 16)
            globalVariable.IRK_MAP['QPLAY']  = int(qplay_code.strip(), 16)
            globalVariable.IRK_MAP['RPoint'] = int(rpoint_code.strip(), 16)
            globalVariable.IRK_MAP['BSTART'] = int(bstart_code.strip(), 16)
            globalVariable.IRK_MAP['ToEND']  = int(toend_code.strip(), 16)
            globalVariable.IRK_MAP['OPT']    = int(opt_code.strip(), 16)
            globalVariable.IRK_MAP['SLEEP']  = int(sleep_code.strip(), 16)
            globalVariable.IRK_MAP['DELAY']  = int(dely_code.strip(), 16)

            #print globalVariable.IRK_MAP['System']
        elif section=='Sunplus':
            sys_code = self.parseConfigItem(self.section,'System').split(':')[0]
            power_code = self.parseConfigItem(self.section,'POWER').split(':')[0]
        
            code_1 = self.parseConfigItem(self.section,'1').split(':')[0]
            code_2 = self.parseConfigItem(self.section,'2').split(':')[0]
            code_3 = self.parseConfigItem(self.section,'3').split(':')[0]
            code_4 = self.parseConfigItem(self.section,'4').split(':')[0]
            code_5 = self.parseConfigItem(self.section,'5').split(':')[0]
            code_6 = self.parseConfigItem(self.section,'6').split(':')[0]
            code_7 = self.parseConfigItem(self.section,'7').split(':')[0]
            code_8 = self.parseConfigItem(self.section,'8').split(':')[0]
            code_9 = self.parseConfigItem(self.section,'9').split(':')[0]
            code_0 = self.parseConfigItem(self.section,'0').split(':')[0]
        
            pgup_code = self.parseConfigItem(self.section,'>>|').split(':')[0]
            pgdn_code = self.parseConfigItem(self.section,'|<<').split(':')[0]
        
            menu_code = self.parseConfigItem(self.section,'MENU').split(':')[0]
            exit_code = self.parseConfigItem(self.section,'EXIT').split(':')[0]
        
            up_code = self.parseConfigItem(self.section,'UP').split(':')[0]
            dn_code = self.parseConfigItem(self.section,'DOWN').split(':')[0]
            left_code = self.parseConfigItem(self.section,'LEFT').split(':')[0]
            right_code = self.parseConfigItem(self.section,'RIGHT').split(':')[0]
        
            ok_code = self.parseConfigItem(self.section,'OK').split(':')[0]
            info_code = self.parseConfigItem(self.section,'INFO').split(':')[0]
            dvr_code = self.parseConfigItem(self.section,'SAT').split(':')[0]
            
            #vol_plus_code = self.parseConfigItem(self.section,'VOL+').split(':')[0]
            #vol_minus_code = self.parseConfigItem(self.section,'VOL-').split(':')[0]
        
            #list_code = self.parseConfigItem(self.section,'LIST').split(':')[0]
            back_code = self.parseConfigItem(self.section,'RECALL').split(':')[0]
        
            red_code = self.parseConfigItem(self.section,'RED').split(':')[0]
            green_code = self.parseConfigItem(self.section,'GREEN').split(':')[0]
            yellow_code = self.parseConfigItem(self.section,'YELLOW').split(':')[0]
            blue_code = self.parseConfigItem(self.section,'BLUE').split(':')[0]
        
            #ch_plus_code = self.parseConfigItem(self.section,'CH+').split(':')[0]
            #ch_minus_code = self.parseConfigItem(self.section,'CH-').split(':')[0]
        
            epg_code = self.parseConfigItem(self.section,'EPG').split(':')[0]
            time_code = self.parseConfigItem(self.section,'TIMER').split(':')[0]
            media_code = self.parseConfigItem(self.section,'SOURCE').split(':')[0]
            reclist_code = self.parseConfigItem(self.section,'FILELIST').split(':')[0]
            audio_code = self.parseConfigItem(self.section,'AUDIO').split(':')[0]
            tv_radio_code = self.parseConfigItem(self.section,'TV/R').split(':')[0]
            mute_code = self.parseConfigItem(self.section,'MUTE').split(':')[0]
            subt_code = self.parseConfigItem(self.section,'SUB').split(':')[0]
            #vformat_code = self.parseConfigItem(self.section,'V.Format').split(':')[0]
        
            zoom_code = self.parseConfigItem(self.section,'ZOOM').split(':')[0]
            ttx_code = self.parseConfigItem(self.section,'TTX/CC').split(':')[0]
            pav_code = self.parseConfigItem(self.section,'FAV').split(':')[0]
            #find_code = self.parseConfigItem(self.section,'FIND').split(':')[0]
        
            play_code = self.parseConfigItem(self.section,'Play').split(':')[0]
            pause_code = self.parseConfigItem(self.section,'Pause').split(':')[0]
            stop_code = self.parseConfigItem(self.section,'Stop').split(':')[0]
        
            qback_code = self.parseConfigItem(self.section,'<<').split(':')[0]
            qplay_code = self.parseConfigItem(self.section,'>>').split(':')[0]
        
            rpoint_code = self.parseConfigItem(self.section,'Rec').split(':')[0]
            #bstart_code = self.parseConfigItem(self.section,'BSTART').split(':')[0]
        
            
            globalVariable.IRK_MAP['System'] = int(sys_code.strip(), 16)
            globalVariable.IRK_MAP['POWER']  = int(power_code.strip(), 16)
            globalVariable.IRK_MAP['1']      = int(code_1.strip(), 16)
            globalVariable.IRK_MAP['2']      = int(code_2.strip(), 16)
            globalVariable.IRK_MAP['3']      = int(code_3.strip(), 16)
            globalVariable.IRK_MAP['4']      = int(code_4.strip(), 16)
            globalVariable.IRK_MAP['5']      = int(code_5.strip(), 16)
            globalVariable.IRK_MAP['6']      = int(code_6.strip(), 16)
            globalVariable.IRK_MAP['7']      = int(code_7.strip(), 16)
            globalVariable.IRK_MAP['8']      = int(code_8.strip(), 16)
            globalVariable.IRK_MAP['9']      = int(code_9.strip(), 16)
            globalVariable.IRK_MAP['0']      = int(code_0.strip(), 16)
            globalVariable.IRK_MAP['>>|']  = int(pgup_code.strip(), 16)
            globalVariable.IRK_MAP['|<<']  = int(pgdn_code.strip(), 16)
            globalVariable.IRK_MAP['MENU']   = int(menu_code.strip(), 16)
            globalVariable.IRK_MAP['EXIT']   = int(exit_code.strip(), 16)
            globalVariable.IRK_MAP['UP']     = int(up_code.strip(), 16)
            globalVariable.IRK_MAP['DOWN']   = int(dn_code.strip(), 16)
            globalVariable.IRK_MAP['LEFT']   = int(left_code.strip(), 16)
            globalVariable.IRK_MAP['RIGHT']  = int(right_code.strip(), 16)
            globalVariable.IRK_MAP['OK']     = int(ok_code.strip(), 16)
            globalVariable.IRK_MAP['INFO']   = int(info_code.strip(), 16)
            globalVariable.IRK_MAP['SAT']    = int(dvr_code.strip(), 16)
            #globalVariable.IRK_MAP['VOL+']   = int(vol_plus_code.strip(), 16)
            #globalVariable.IRK_MAP['VOL-']   = int(vol_minus_code.strip(), 16)
            #globalVariable.IRK_MAP['LIST']   = int(list_code.strip(), 16)
            globalVariable.IRK_MAP['RECALL']   = int(back_code.strip(), 16)
            globalVariable.IRK_MAP['RED']    = int(red_code.strip(), 16)
            globalVariable.IRK_MAP['GREEN']  = int(green_code.strip(), 16)
            globalVariable.IRK_MAP['YELLOW'] = int(yellow_code.strip(), 16)
            globalVariable.IRK_MAP['BLUE']   = int(blue_code.strip(), 16)
            #globalVariable.IRK_MAP['CH+']    = int(ch_plus_code.strip(), 16)
            #globalVariable.IRK_MAP['CH-']    = int(ch_minus_code.strip(), 16)
            globalVariable.IRK_MAP['EPG']    = int(epg_code.strip(), 16)
            globalVariable.IRK_MAP['TIMER']  = int(time_code.strip(), 16)
            globalVariable.IRK_MAP['SOURCE']  = int(media_code.strip(), 16)
            globalVariable.IRK_MAP['FILELIST']= int(reclist_code.strip(), 16)
            globalVariable.IRK_MAP['AUDIO']  = int(audio_code.strip(), 16)
            globalVariable.IRK_MAP['TV/R']= int(tv_radio_code.strip(), 16)
            globalVariable.IRK_MAP['MUTE']   = int(mute_code.strip(), 16)
            globalVariable.IRK_MAP['SUB']   = int(subt_code.strip(), 16)
            #globalVariable.IRK_MAP['V.Format']  = int(vformat_code.strip(), 16)
            globalVariable.IRK_MAP['ZOOM']   = int(zoom_code.strip(), 16)
            globalVariable.IRK_MAP['TTX/CC']    = int(ttx_code.strip(), 16)
            globalVariable.IRK_MAP['FAV']    = int(pav_code.strip(), 16)
            #globalVariable.IRK_MAP['FIND']   = int(find_code.strip(), 16)
            globalVariable.IRK_MAP['Play']   = int(play_code.strip(), 16)
            globalVariable.IRK_MAP['Pause']  = int(pause_code.strip(), 16)
            globalVariable.IRK_MAP['Stop']   = int(stop_code.strip(), 16)
            globalVariable.IRK_MAP['<<']  = int(qback_code.strip(), 16)
            globalVariable.IRK_MAP['>>']  = int(qplay_code.strip(), 16)
            globalVariable.IRK_MAP['Rec'] = int(rpoint_code.strip(), 16)
            #globalVariable.IRK_MAP['BSTART'] = int(bstart_code.strip(), 16)
        elif section=='SaiKeDa':
            sys_code = self.parseConfigItem(self.section,'System').split(':')[0]
            mute_code = self.parseConfigItem(self.section,'MUTE').split(':')[0]
            power_code = self.parseConfigItem(self.section,'POWER').split(':')[0]
            code_1 = self.parseConfigItem(self.section,'1').split(':')[0]
            code_2 = self.parseConfigItem(self.section,'2').split(':')[0]
            code_3 = self.parseConfigItem(self.section,'3').split(':')[0]
            code_4 = self.parseConfigItem(self.section,'4').split(':')[0]
            code_5 = self.parseConfigItem(self.section,'5').split(':')[0]
            code_6 = self.parseConfigItem(self.section,'6').split(':')[0]
            code_7 = self.parseConfigItem(self.section,'7').split(':')[0]
            code_8 = self.parseConfigItem(self.section,'8').split(':')[0]
            code_9 = self.parseConfigItem(self.section,'9').split(':')[0]
            code_0 = self.parseConfigItem(self.section,'0').split(':')[0]
            
            audchl_code = self.parseConfigItem(self.section,'AUDCHL').split(':')[0]
            vod_code = self.parseConfigItem(self.section,'VOD').split(':')[0]
            up_code = self.parseConfigItem(self.section,'UP').split(':')[0]
            dn_code = self.parseConfigItem(self.section,'DOWN').split(':')[0]
            left_code = self.parseConfigItem(self.section,'LEFT').split(':')[0]
            right_code = self.parseConfigItem(self.section,'RIGHT').split(':')[0]
            ok_code = self.parseConfigItem(self.section,'OK').split(':')[0]
            zhixun_code = self.parseConfigItem(self.section,'ZhiXun').split(':')[0]
            back_code = self.parseConfigItem(self.section,'BACK').split(':')[0]
            menu_code = self.parseConfigItem(self.section,'MENU').split(':')[0]
            exit_code = self.parseConfigItem(self.section,'EXIT').split(':')[0]
            red_code = self.parseConfigItem(self.section,'RED').split(':')[0]
            green_code = self.parseConfigItem(self.section,'GREEN').split(':')[0]
            yellow_code = self.parseConfigItem(self.section,'YELLOW').split(':')[0]
            blue_code = self.parseConfigItem(self.section,'BLUE').split(':')[0]
            mail_code = self.parseConfigItem(self.section,'MAIL').split(':')[0]
            stock_code = self.parseConfigItem(self.section,'STOCK').split(':')[0]
            fav_code = self.parseConfigItem(self.section,'FAV').split(':')[0]       
            pgup_code = self.parseConfigItem(self.section,'PgUP').split(':')[0]
            pgdn_code = self.parseConfigItem(self.section,'PgDN').split(':')[0]
            radio_code = self.parseConfigItem(self.section,'RADIO').split(':')[0]
            vol_plus_code = self.parseConfigItem(self.section,'Vol+').split(':')[0]
            vol_minus_code = self.parseConfigItem(self.section,'Vol-').split(':')[0]
            tv_code = self.parseConfigItem(self.section,'TV').split(':')[0]
            epg_code = self.parseConfigItem(self.section,'EPG').split(':')[0]
            book_code = self.parseConfigItem(self.section,'BOOK').split(':')[0]
            info_code = self.parseConfigItem(self.section,'Info').split(':')[0]

            
            globalVariable.IRK_MAP['System'] = int(sys_code.strip(), 16)
            globalVariable.IRK_MAP['POWER']  = int(power_code.strip(), 16)
            globalVariable.IRK_MAP['1']      = int(code_1.strip(), 16)
            globalVariable.IRK_MAP['2']      = int(code_2.strip(), 16)
            globalVariable.IRK_MAP['3']      = int(code_3.strip(), 16)
            globalVariable.IRK_MAP['4']      = int(code_4.strip(), 16)
            globalVariable.IRK_MAP['5']      = int(code_5.strip(), 16)
            globalVariable.IRK_MAP['6']      = int(code_6.strip(), 16)
            globalVariable.IRK_MAP['7']      = int(code_7.strip(), 16)
            globalVariable.IRK_MAP['8']      = int(code_8.strip(), 16)
            globalVariable.IRK_MAP['9']      = int(code_9.strip(), 16)
            globalVariable.IRK_MAP['0']      = int(code_0.strip(), 16)
            globalVariable.IRK_MAP['AUDCHL'] = int(audchl_code.strip(), 16)
            globalVariable.IRK_MAP['VOD']     = int(vod_code.strip(), 16)
            globalVariable.IRK_MAP['UP']     = int(up_code.strip(), 16)
            globalVariable.IRK_MAP['DOWN']   = int(dn_code.strip(), 16)
            globalVariable.IRK_MAP['LEFT']   = int(left_code.strip(), 16)
            globalVariable.IRK_MAP['RIGHT']  = int(right_code.strip(), 16)
            globalVariable.IRK_MAP['OK']     = int(ok_code.strip(), 16)
            globalVariable.IRK_MAP['ZhiXun']     = int(zhixun_code.strip(), 16)
            globalVariable.IRK_MAP['BACK']   = int(back_code.strip(), 16)
            globalVariable.IRK_MAP['MENU']   = int(menu_code.strip(), 16)
            globalVariable.IRK_MAP['EXIT']   = int(exit_code.strip(), 16)
            globalVariable.IRK_MAP['RED']    = int(red_code.strip(), 16)
            globalVariable.IRK_MAP['GREEN']  = int(green_code.strip(), 16)
            globalVariable.IRK_MAP['YELLOW'] = int(yellow_code.strip(), 16)
            globalVariable.IRK_MAP['BLUE']   = int(blue_code.strip(), 16)
            globalVariable.IRK_MAP['MAIL']   = int(mail_code.strip(), 16)
            globalVariable.IRK_MAP['STOCK']   = int(stock_code.strip(), 16)
            globalVariable.IRK_MAP['FAV']   = int(fav_code.strip(), 16)
            globalVariable.IRK_MAP['PgUP']  = int(pgup_code.strip(), 16)
            globalVariable.IRK_MAP['PgDN']  = int(pgdn_code.strip(), 16)
            globalVariable.IRK_MAP['RADIO']  = int(radio_code.strip(), 16)
            globalVariable.IRK_MAP['VOL+']   = int(vol_plus_code.strip(), 16)
            globalVariable.IRK_MAP['VOL-']   = int(vol_minus_code.strip(), 16)
            globalVariable.IRK_MAP['TV']   = int(tv_code.strip(), 16)
            globalVariable.IRK_MAP['BOOK']   = int(book_code.strip(), 16)
            globalVariable.IRK_MAP['Info']   = int(info_code.strip(), 16)
            globalVariable.IRK_MAP['EPG']   = int(epg_code.strip(), 16)

