# -*- coding: UTF-8 -*-
'''
发送文本和带附件的邮件
'''
import smtplib  
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import globalVariable


class SendMail(object):
    def __init__(self,to_list = globalVariable.USER_MAIL_LIST,
                 cc_list = globalVariable.USER_CC_LIST,
                 host = "10.209.152.54",
                 user = "Automation",
                 passwd = "Avl1108"):
        self.mailto_list = to_list
        self.mailcc_list = cc_list
        self.mail_host = host
        self.mail_user= user
        self.mail_pass= passwd
        self.me = "Automation@availink.com"
    def send_mail(self,sub,content,attachment = ''):  
        if attachment:  
            body = MIMEText(content,_subtype='plain',_charset='utf-8')  
            msg = MIMEMultipart()        
            msg.attach(body)
            att = MIMEText(open(attachment, 'rb').read(), 'base64', 'gb2312')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename= %s' % attachment
            msg.attach(att)
        else:
            msg = MIMEText(content,_subtype='plain',_charset='utf-8')    
        msg['Subject'] = sub  
        msg['From'] = self.me  
        msg['To'] = ";".join(self.mailto_list)
        msg['Cc'] = ";".join(self.mailcc_list)
            
        try:  
            server = smtplib.SMTP()
            server.set_debuglevel(True)  
            server.connect(self.mail_host,25)  
            server.login(self.mail_user,self.mail_pass)  
            server.sendmail(self.me, self.mailto_list+self.mailcc_list, msg.as_string())  
            server.close()  
            return True  
        except Exception, e:  
            print str(e)  
            return False
    def send_html_mail(self,sub,content):
        msg = MIMEText(content,_subtype='html',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = self.me  
        msg['To'] = ";".join(self.mailto_list)
        msg['Cc'] = ";".join(self.mailcc_list)  
        try:  
            s = smtplib.SMTP()  
            s.connect(self.mail_host)
            s.login(self.mail_user,self.mail_pass)
            s.sendmail(self.me, self.mailto_list+self.mailcc_list, msg.as_string())
            s.close()  
            return True  
        except Exception, e:  
            print str(e)  
            return False

if __name__ == '__main__':
    inst = SendMail()
    if inst.send_html_mail("hello","<a href='http://www.baidu.com'>test</a>"):  
        print "发送成功"  
    else:  
        print "发送失败"
