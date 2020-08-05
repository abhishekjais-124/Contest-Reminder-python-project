from bs4 import BeautifulSoup
import requests
import datetime
import re
from twilio.rest import Client
import random
from datetime import timedelta
import math



sid= "ACd1f57b2f44498ee9e39f7426da0607cd"
token = "*****************************"  #not shown due to privacy
client = Client(sid,token)
Name = []
p_title = []
level = ['school','easy']

for i in level:
    URL2 = "https://www.codechef.com/problems/" + i
    parsed_html = requests.get(URL2)
    soup2 = BeautifulSoup(parsed_html.content,"html.parser")
    data2 = str(soup2.findAll("tr", class_ = "problemrow"))
    Name += re.findall(r'<b>(.*?)</b>',data2)
    p_title += re.findall(r'Submit a solution to this problem.">(.*?)</a>',data2)
#print(Name)
#print(p_title)
total = len(Name)
choose = random.randint(0,total-1)

x1 = Name[choose] + " ("  + p_title[choose] + ")"
x3 = "https://www.codechef.com/problems/" + p_title[choose]
#print(x1,x3)

Month = ['January','February','March','April','May','June','July',"August",'September','October','November','December']
Mainloc = ['spoj','code','hacker','google','facebook','codingame']
Neg = ['developer','fullstack','hackathon','frontend','backend','machine','deep','devops']

URL = "https://clist.by/"

def fun(l):
    for i in Mainloc:
        if l.find(i) != -1:
            return True
    return False

parsed_html = requests.get(URL)
soup = BeautifulSoup(parsed_html.content,"html.parser")
data = str(soup.findAll("a", class_ = "data-ace"))
#print(data)

contest_title = re.findall(r'title"(.*?)",',data)
location = re.findall(r'location"(.*?)",',data)
start = re.findall(r'start"(.*?)",',data)
end = re.findall(r'end"(.*?)",',data)
url_list = re.findall(r'url: (.*?)",',data)
#print(contest_title)
#print(location)
#print(start)
#print(end)
#print(url_list)
A = []
events = len(start)
for i in range(events):
    s = start[i].strip().split(" ")
    s_month =Month.index(s[0][2:]) + 1
    s_date = int(s[1][:-1])
    s_year = int(s[2])
    s_time = s[3].strip().split(':')
    #print(s_month,s_date,s_year,s_time)
    e = end[i].strip().split(" ")
    e_month = Month.index(e[0][2:]) + 1
    e_date = int(e[1][:-1])
    e_year = int(e[2])
    e_time = e[3].strip().split(':')
    #print(e_month, e_date, e_year, e_time)
    a = datetime.datetime(s_year,s_month,s_date,int(s_time[0]) , int(s_time[1]),int(s_time[2]))
    b = datetime.datetime(e_year, e_month, e_date, int(e_time[0]), int(e_time[1]), int(e_time[2]))
    a += timedelta(hours= 5,minutes= 30)
    b += timedelta(hours=5, minutes=30)
    c = b - a
    d = a - datetime.datetime.today()
    #print(a,b,c.days)
    loc = location[i][2:]
    zz = contest_title[i][2:].lower()
    if c.days <= 10 and fun(loc) and d.days < 2:
        if 'hacker' in loc:
            ff = 0
            for m in Neg:
                if zz.find(m) != -1:
                    ff = 1
                    break
            if ff:  continue
        temp = []
        t1 = loc.split('.')[0].capitalize() + ": " + contest_title[i][2:]
        #print(t1)
        print(a,b,loc)
        t2 = a.strftime("%d %b %Y %I:%M %p")
        t3 = b.strftime("%d %b %Y %I:%M %p")
        if c.days == 0:
            tt =divmod(c.seconds,3600)
            t4 = str(tt[0]) + " hours " + str(tt[1]//60) + " minutes"
        else:
            tt = divmod(c.seconds,60)
            t4 = str(c.days) + " days"
        temp.append(t1);temp.append(t2);temp.append(t3);temp.append(t4);temp.append(url_list[i])
        A.append(temp.copy())
#print(A)

Numbers = ["7615815667"]

msg  = "Contest Reminder" + '\n\n'
c = 0
n = len(A)
print("Working...")
for i in A:
    msg += '*' + str(c+1) +'*'+ ". " +'*'+ i[0] + '*'+ '\n' + 'Start: ' + i[1] + '\n' + 'End: ' + i[2] + '\n' + 'Duration: ' + i[3] + '\n' + 'link: ' + i[4] + '\n\n'
    c += 1
    print(c)
    if c % 6 == 0 or c == n:
        if c == n:
            msg += '_Problem of the day_' + '\n\n' + '*' +x1 +'*\n' + x3 + '\n\n' + "By AJ"
        for j in Numbers:
            message = client.messages.create(body = msg, from_ = "whatsapp:+14155238886",to = "whatsapp:+91" + j)
        msg = ""
