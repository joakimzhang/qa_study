#!coding:utf-8
import jinja2
import os
import socket

import globalVariable
import sendMail

template = jinja2.Template("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang='en'>
<head xmlns="http://www.w3.org/1999/xhtml">
  <meta charset='utf-8' />
  <title>Test results</title>
    <style>
        .title
        {
        text-align:center;
        }
        
        .report
          {
          font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
          width:100%;
          border-collapse:collapse;
          }
        
        .report td, #report th 
          {
          font-size:1em;
          border:1px solid #98bf21;
          padding:3px 7px 2px 7px;
          }
        
        .report th 
          {
          font-size:1.1em;
          text-align:left;
          padding-top:5px;
          padding-bottom:4px;
          background-color:#97CBFF;
          color:#ffffff;
          }
        
        .report tr.alt td 
          {
          color:#000000;
          background-color:#EAF2D3;
          }
        
        caption
            {
                font-size:25px;
                font-weight: bold
            }
    </style>
</head>

<body>

  <h3 class='title'>
  App Automation Report
  </h3>
    <table id="testruns" class="report">
      <thead>
      <tr>
        <th style="width:10em">Timestamp</th>
        <th style="width:30%">Test</th>
        <th>Exit status</th>
        <th>Notes</th>
        <th style="width:5em">Duration</th>
      </tr>
      </thead>
      <tbody>
      {% for run in runs %}
      <tr bgcolor="{{run.bg_color()}}">
        <td>{{run.timestamp}}</td>
        <td>{{run.test_name}}</td>
        <td>
          {% if run.exit_status == 'PASS(memory check)' %}
              <a href = {{run.img_url()}}>{{run.exit_status}}</a>
          {% else %}
              {{run.exit_status}}
              {% if run.exit_status not in ("", "PASS", "PASS(memory check)") %}
                  - <span>{{run.failure_reason|e}}</span>
              {% endif %}
           {% endif %}
        </td>
        <td>{{run.notes|e}}</td>
        <td>{{run.duration}}</td>
      </tr>
      {% endfor %}
      </tbody>
    </table>

</body>
</html>
""")

class CaseInfo():
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        
    def bg_color(self):
        if self.exit_status == 'PASS' or self.exit_status == 'PASS(memory check)':
            return "#edffe6"
        elif self.exit_status == 'FAIL':
            return "#ff9797"  # Red: Possible system-under-test failure
    def img_url(self):
        if socket.gethostbyname(socket.gethostname()) != globalVariable.APACHE_SERVER:
            img_url = 'http://%s/not_exist.jpg'%globalVariable.APACHE_SERVER
        else:
            img_url = os.path.join('http://%s'%globalVariable.APACHE_SERVER, globalVariable.IMAGE_DICT[self.test_name])
            img_url = img_url.replace('\\', '/')
        return img_url
        
class CaseFactory(object):
    cases = []
    
    def __init__(self, *args, **kwargs):
        self.cases.append(CaseInfo(*args, **kwargs))
    
    @classmethod
    def create_html(cls, html = 'report.html'):
        with open(html, "w+") as f:
            f.write(template.render(name = 'app', runs = cls.cases))
    
    @classmethod
    def send_report(cls, report_time):
        cls.create_html()
        with open('report.html', 'r') as f:
            content = f.read()
        inst = sendMail.SendMail()
        inst.send_html_mail('App Automation Report at %s'%report_time, content)
        
if __name__ == '__main__':
    CaseFactory(timestamp = 1, test_name = 'test1', exit_status = 'PASS', failure_reason = 'success', duration = '30', note = '')
    CaseFactory(timestamp = 2, test_name = 'test2', exit_status = 'FAIL', failure_reason = 'not match', duration = '28', note = '')
    CaseFactory.create_html()

