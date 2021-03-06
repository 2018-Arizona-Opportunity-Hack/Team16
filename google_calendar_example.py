from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import json
from pprint import pprint

# If modifying these scopes, delete the file token.json.
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'

# name, experience, age, email, phone, 
def jsonToList(json_file):
    #import ast
    #d = ast.literal_eval("{'code1':1,'code2':1}")
    with open(json_file) as f:
        data = json.load(f)
    #print(data)
    return data

def listToJson(list_table,json_name):
        #json.dumps(list_table, outfile)
    json_string = json.dumps(list_table)
    #print(json_string)
    with open(json_name, 'a+') as outfile:
        outfile.write(json_string)

def send_email_notify(html_str,date_str_0,date_str_1,loc_str,email_list,require_num):
    me = "alpaca5566zzz@gmail.com"

    ## Deal with email list based on history recored
    ## input require_num

    filename = "history.txt"
    try:
        fs = open(filename, "r+")
    except:
        fs = open(filename, "a+")
    history = fs.readlines()
    fs.close()
    index = 0
    history_list = []
    for i,ival in enumerate(history):
        #print(ival)
        if ival.replace('\n', '') == html_str:
            history_list = history[i+1].replace("\n","").replace(" ","")[1:-1].split(",")
            history[i+1] = [k[1:-1] for k in history_list]
            index = i+1
            break
  
    history_dict = {}
    for i in history[index]:
        if i not in history_dict:
            history_dict[i] = 1

    #print(history_dict)
    real_email_list = []
    for i in email_list:
        if len(real_email_list) == require_num: 
            print("enough emails")
            break
        if i not in history_dict:
            real_email_list.append(i)
    #print(history[index],real_email_list)
    #print(email_list)
    history[index] = str(history[index] + real_email_list)+"\n"
    with open(filename, "w") as fs:
        fs.writelines(history)

    you = ", ".join(real_email_list)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Invoice for Volunteers"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    pwd = "alpaca5566%%%"
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi Volunteer:<br>
           Hope you are doing great today,<br>
           We will have an event with following informations and please check with the button below if you are willing to join :) <br>
           Time: {calendar_time_start} to {calendar_time_end}
           Location: {calendar_location}
        </p>
        <table width="100%" cellspacing="0" cellpadding="0">
          <tr>
            <td>
              <table cellspacing="0" cellpadding="0">
                <tr>
                  <td style="border-radius: 2px;" bgcolor="#ED2939">
                    <a href="{calendar_url}" target="_blank" style="padding: 8px 12px; border: 1px solid #ED2939;border-radius: 2px;font-family: Helvetica, Arial, sans-serif;font-size: 14px; color: #ffffff;text-decoration: none;font-weight:bold;display: inline-block;">
                          YES!!! I AM IN!!!             
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
       </table>
      </body>
    </html>
    """.format(calendar_url=html_str,calendar_time_start=date_str_0,calendar_time_end=date_str_1,calendar_location=loc_str,subtype='html')
    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    fp = open("kitten.jpeg", 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<0>'.format("kitten.jpeg"))
    img.add_header('Content-Disposition', 'attachment',filename="kitten.jpeg")
    img.add_header('X-Attachment-Id', '0')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)
    #msg.attach(img)

        ##<h2>HTML Image</h2>
        ##<img src="kitten.jpeg" alt="Kitten Look" width="500" height="600">
    #msgText = MIMEText('<b>%s</b><br><img src="cid:%s" width="500" height="600"><br>' %(part2,"kitten.jpeg"), 'html')
    #msg.attach(msgText)

    #fp = open("kitten.jpeg", 'rb')
    #img = MIMEImage(fp.read())
    #fp.close()
    ###img.add_header('Content-ID', '<{}>'.format("kitten.jpeg"))
    #msg.attach(img)
    
    #print(msg)    
    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(me, pwd)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #server.sendmail(me, you, msg.as_string())
    server.sendmail(me, real_email_list, msg.as_string())
    server.quit()

def poll_attend(event_id,service,html_val):

    ##page_token = None
    ##while True:
    ##    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    ##    for calendar_list_entry in calendar_list['items']:
    ##        print(calendar_list_entry)
    ##    page_token = calendar_list.get('nextPageToken')
    ##    if not page_token:
    ##        break

    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    #print("\n") 
    #print(event) 

    accept = reject = not_decide = 0
    email_list = []
    for attendee in event['attendees']:
        #if attendee not in history_dict:
            attendees = (attendee['email'],attendee['responseStatus'])
            #print(attendee['responseStatus'])
            if attendee['responseStatus'] == "accepted":
                email_list.append(attendee['email'])
                accept += 1
            elif attendee['responseStatus'] == "declined":
                reject += 1
            else:
                not_decide += 1

    return email_list,accept,reject,not_decide

##def GE_main(create,html_val,email_list,date_str,loc_str,text_str,require_num):
def GE_main(create,html_val,email_list,require_num):
    filename = "event.txt" ##Name for local file to save for google calendar event URL and event ID

    #json_data = jsonToList(json_file_name)
    #email_list = [ list(json_data.values())[0][i]["Email"] for i in list(json_data.values())[0]]

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        #flow = client.flow_from_clientsecrets('OpportunityHack.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    event = {
      'summary': 'Test for invitation',
      'location': '1216 E Vista Del Cerro Dr,. APT 2103N, Tempe, AZ 85281',
      'description': 'Opportunity Hack 2018',
      'start': {
        'dateTime': '2018-10-22T11:00:00-07:00',
        'timeZone': 'America/Phoenix',
      },
      'end': {
        'dateTime': '2018-10-22T11:00:00-07:00',
        'timeZone': 'America/Phoenix',
      },
      'attendees': [],
      'sendUpdates': 'all',
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 30},
        ],
      },
    }

    for i in email_list:
        event['attendees'].append({'email': i})
    #print(event)

    if not create:
        fs  = open(filename, "r+")
        event_txt = fs.readlines()
        fs.close()
        for i,ival in enumerate(event_txt):
            #print(ival)
            if ival.replace('\n', '') == html_val:
                event = service.events().get(calendarId='primary', eventId=event_txt[i+1].replace('\n','')).execute()
                result_list,accept,reject,not_decide = poll_attend(event_txt[i+1].replace('\n',''),service,html_val)

                ##old_email_list = []
                ##for k in event['attendees']:
                ##    old_email_list.append(k['email'])

                send_email_notify(event['htmlLink'],event['start']['dateTime'][:10]+" "+event['start']['dateTime'][11:17],event['end']['dateTime'][:10]+" "+event['end']['dateTime'][11:17],event['location'],email_list,require_num-accept-reject-not_decide)
                return result_list
        print("Event Not Found")
        return []
    else:    
        fs  = open(filename, "a+")
        new_event = service.events().insert(calendarId='primary', body=event).execute()
        #print(new_event)
        fs.write(new_event["htmlLink"])
        fs.write("\n")
        fs.write(new_event["id"])
        fs.write("\n")
        send_email_notify(new_event['htmlLink'],new_event['start']['dateTime'][:10]+" "+new_event['start']['dateTime'][11:17],new_event['end']['dateTime'][:10]+" "+new_event['end']['dateTime'][11:17],new_event['location'],email_list,require_num);
        print("Event Built")
        return [new_event["htmlLink"]]


##json_name = "real.json"
##simple_list = jsonToList(json_name)
##new_json_name = "real_new.json"
##listToJson(simple_list,new_json_name)

#ge_create = True
ge_create = False
#ge_html="https://www.google.com/calendar/event?eid=ajM1OGhrcGhrbTVzOGxtb2FmY3F0bnIxNDhfMjAxODEwMjFUMTgwMDAwWiBhbHBhY2E1NTY2enp6QG0"
ge_html="https://www.google.com/calendar/event?eid=Y2szNzlzdXA5ZDU2b2lodnYyMXZtdGFodGsgYWxwYWNhNTU2Nnp6ekBt"
vol_list = ['ocasiychuang@gmail.com','david9yieh@gmail.com']
result_list = GE_main(ge_create,ge_html,vol_list,4)
print(result_list)
