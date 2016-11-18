# -*- coding=gbk -*-
import re
import sys  
reload(sys)  
sys.setdefaultencoding('gbk')   
import csv
from xml.etree.ElementTree import iterparse
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
class XML_CSV():
    #ȥ��xml�ļ��е�HTML��ǩ
    def strip_tags(self,htmlStr):
        htmlStr = htmlStr.strip()
        htmlStr = htmlStr.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(htmlStr)
        parser.close()
        return  ''.join(result)
     
    def read_xml_to_csv(self,csv_file,xmlfile):  
        csvfile = open(csv_file, 'wb')
        #���������ĵ�ַ���б�txt�ļ���
        link_txt_file = open(xmlfile.replace(".xml",".txt"),'wb')
        #���������ĵ�ַ���б�csv�ļ���
        link_csv_file = open(xmlfile.replace(".xml","_link.csv"),'wb')
        linkwriter = csv.writer(link_csv_file, dialect='excel')
        linkwriter.writerow(['name', 'link'])
        
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(['tag', 'name', 'node_order', 'details', 'internalid','externalid','summary','steps','expectedresults'])
        #���н���XML�ļ�����ÿ�е����ݴ����б�֮������д��CSV�ļ���
        for (event,node) in iterparse(xmlfile,events=['start']):
            if node.tag == "testsuite":
                suite_list = ['','','','','','','','','']
                print node.attrib['name']
                suite_list[0] = node.attrib['name']
                for child in node:
                    if child.tag == "node_order":
                        print child.text
                        suite_list[2] = child.text
                    if child.tag == "details":
                        print child.text
                        suite_list[3] = self.strip_tags(str(child.text))
                spamwriter.writerow(suite_list)
            if node.tag == "testcase":
                case_list = ['testcase','','','','','','','','']
                link_list = ['','']
                print node.attrib['internalid']
                print node.attrib['name']
                case_list[1] = node.attrib['name']
                case_list[4] = node.attrib['internalid']
                for child in node:
                    if child.tag == "node_order":
                        print child.text
                        case_list[2] = child.text
                    if child.tag == "externalid":
                        print child.text
                        case_list[5] = child.text
                    if child.tag == "summary":
                        print self.strip_tags(str(child.text))
                        case_list[6] = self.strip_tags(str(child.text))
                    if child.tag == "steps":
                        print self.strip_tags(str(child.text))
                        case_list[7] = self.strip_tags(str(child.text))
                    if child.tag == "expectedresults":
                        #print child.text
                        print self.strip_tags(str(child.text))
                        case_list[8] = self.strip_tags(str(child.text))
                spamwriter.writerow(case_list)

                link_obj = re.search(r"\\\\.*\.(ts|trp)",case_list[7])
                link_obj_bak = re.search(r"\\\\\S*",case_list[7])
                link_obj2 = re.search(r"\\\\.*\.(ts|trp)",case_list[6])
                link_obj2_bak = re.search(r"\\\\\S*",case_list[6])
                
                if link_obj:
                    link_final = link_obj.group(0)
                elif link_obj2:
                    link_final = link_obj2.group(0)
                elif link_obj_bak:
                    link_final = link_obj_bak.group(0)
                elif link_obj2_bak:
                    link_final = link_obj2_bak.group(0)
                else:
                    link_final = ""
                #link_final = link_final.replace('\\','\\\\')
                temp_txt = r"[Template]    video_templete"
                
                link_content = "YHD-%s:%s\n    %s\n    %s\n"%(case_list[5],case_list[1],temp_txt,link_final)
                link_list[0] = "YHD-%s:%s"%(case_list[5],case_list[1])
                link_list[1] = link_final
                linkwriter.writerow(link_list)
                print link_content
                link_txt_file.write(link_content)
                #link_list.write(case_list[7])
        csvfile.close()
        link_txt_file.close()
    
    def read_csv_to_xml(self,csv_file,xmlfile):
        #���ж�ȡCSV�ļ������ݣ�������д����internalidΪ����name��sumary��steps��expectresultΪֵ���ֵ�
        csv_file = file(csv_file,'rb')
        reader = csv.reader(csv_file)  
        case_dic = {}  
        for line in reader:  
            if reader.line_num == 1:  
                continue  
            if line[0] == "testcase":
                name = str(line[1])
                internalid = str(line[4])
                summary = line[6]
                steps = line[7]
                expectedresults = line[8]
                case_dic[internalid] = (name,summary,steps,expectedresults)
        csv_file.close()
        print case_dic
        #��ElementTree������xml�ļ������н���XML�ļ�������caseΪtag���У��ͽ�name��sumary��steps��expectresult���⼸�����ֵ��ֵ�滻��
        tree = ET.ElementTree()
        tree.parse('usb.xml')
        root = tree.getroot()
        root_suite_name = root.attrib['name']
        
        for node in tree.iter():
            if node.tag == "testsuite":
                print node.attrib['name']
                sub_suite_name = node.attrib['name']
                for child in node:
                    if child.tag == "node_order":
                        #print child.text
                        pass
                    if child.tag == "details":
                        pass
            if node.tag == "testcase":
                new_internalid = node.attrib['internalid']
                #����Ŀ¼����Ŀ¼�����ֶ�д����case�����С��������Ҫ��������������ע�͵����滻��һ��
                node.attrib['name'] = root_suite_name+'_'+sub_suite_name+'_'+case_dic[new_internalid][0]
                #node.attrib['name'] = case_dic[new_internalid][0]
                print node.attrib['name']
                #����tagΪtestcase�Ľڵ���ӽڵ㣬���޸Ľڵ��ֵ
                for child in node:
                    if child.tag == "node_order":
                        pass
                    if child.tag == "externalid":
                        pass
                    if child.tag == "summary":
                        child.text = case_dic[new_internalid][1]
                        child.text = str(child.text.replace('\n',"<p>"))
                    if child.tag == "steps":
                        child.text = str(case_dic[new_internalid][2])
                        child.text = str(child.text.replace('\n',"<p>"))
                    if child.tag == "expectedresults":
                        child.text = case_dic[new_internalid][3]
                        child.text = str(child.text.replace('\n',"<p>"))
        #���޸ĺ��ElementTree����д��xml�ļ��С�
        tree.write('usb.xml',encoding='utf8')   

if __name__ == "__main__":
    test = XML_CSV()
    test.read_xml_to_csv('testsuites5.csv','testsuites.xml')
    #test.read_csv_to_xml('usb2.csv','usb.xml')