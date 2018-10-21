
#time converter
# def time_converter(time):
#     import datetime
#     from datetime import timezone
#     d=datetime.datetime.strptime( str(time), "%Y-%m-%dT%H:%M:%S" )
# #     d=datetime.datetime.strptime( "2007-03-04T21:08:12", "%Y-%m-%dT%H:%M:%S" )
#     timestamp = d.replace(tzinfo=timezone.utc).timestamp()
#     return timestamp
#
#
# # In[3]:
#
#
# #create csv file
# import csv
# with open('hack.csv', 'w',encoding='utf-8') as csvfile:
#     fieldnames = ['userID','Interest','Availibility_from','Availibility_to']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#
#
#
# #writing records
# def writeRecord(userID,Interest,Availibility_f,Availibility_t):
#     u = str(userID)
#     af = time_converter(str(Availibility_f))
#     at = time_converter(str(Availibility_t))
#     i = str(Interest)
#
#     with open('hack.csv','a',encoding='utf-8') as fd:
#         fieldnames = ['userID','Interest','Availibility_from','Availibility_to']
#         writer = csv.DictWriter(fd, fieldnames=fieldnames)
#
#         writing_dic={'userID':u, 'Interest':i, 'Availibility_from':af, 'Availibility_to':at}
#         writer.writerow(writing_dic)
#
#
# #Write Recodes
# # writeRecord('001','cats',"2007-03-04T21:08:13","2007-03-04T21:09:11")
# # writeRecord('002','dogs',"2007-03-04T21:06:12","2007-03-04T21:07:12")
# # writeRecord('003','cats',"2007-03-04T21:08:12","2007-03-04T21:20:12")
# # writeRecord('004','cats',"2007-03-04T21:08:12","2007-03-04T21:20:12")
# #
def timer(time):
    from apscheduler.schedulers.background import BackgroundScheduler

    count = 0

    def job_function():
        print ("job executing")
        global count, scheduler

        # Execute the job till the count of 5
        count = count + 1
        if count == 5:
            scheduler.remove_job('my_job_id')


    scheduler = BackgroundScheduler()
    scheduler.add_job(job_function, 'interval', seconds=int(time), id='my_job_id')


    scheduler.start()


# In[12]:


#filtering CSV
# import pandas as pd
# df=pd.read_csv('hack.csv',encoding='utf-8')


# def interestSelect(interest,Availibility_from,Availibility_to):
#     time_af=(time_converter(Availibility_from))
#     time_at=(time_converter(Availibility_to))

#     new_df=df.loc[(df['Interest'] == str(interest)) & (time_af<=(df['Availibility_from']))& (time_at>=(df['Availibility_to'])) ]
#     new_df.to_csv('Filtered_hack.csv', encoding='utf-8')
#     return new_df

#filtering CSV
# import pandas as pd
# df=pd.read_csv('hack.csv',encoding='utf-8')
#
# #para= >,<,==,!=
#
#
# def interestSelect(certain_column,para,standard):
#
#     if (type(df.iloc[:,int(certain_column)][0]) is str):
#         if para == "=":
#             new_df=df.loc[(df.iloc[:,int(certain_column)] == str(standard))]
#
#
# #             new_df.to_csv('Filtered_hack.csv', encoding='utf-8')
#             return new_df
#         else:
#             new_df=df.loc[(df.iloc[:,int(certain_column)] != str(standard))]
# #             new_df.to_csv('Filtered_hack.csv', encoding='utf-8')
#             return new_df
#     else:
#
#         if para == "=":
#             new_df=df.loc[(df.iloc[:,int(certain_column)] == str(standard))]
# #             new_df.to_csv('Filtered_hack.csv', encoding='utf-8')
#             return new_df
#         elif para == ">":
#             new_df=df.loc[(df.iloc[:,int(certain_column)]) > float(standard)]
# #             new_df.to_csv('Filtered_hack.csv', encoding='utf-8')
#             return new_df
#         elif para == "<":
#             new_df=df.loc[float((df.iloc[:,int(certain_column)]) < float(standard))]
# #             new_df.to_csv('Filtered_hack.csv', encoding='utf-8')
#             return new_df
#         elif para == "!=":
#             new_df=df.loc[(df.iloc[:,int(certain_column)] != str(standard))]
# #             new_df.to_csv('Filtered_hack.csv', encoding='utf-8')
#             return new_df
#

# print(interestSelect(1,"=","cats"))

# #
# def fn():
#     print("Hello, world")
#
#     from apscheduler.schedulers.background import BackgroundScheduler
#
#     scheduler = BackgroundScheduler()
#     scheduler.start()
#     scheduler.add_job(fn, trigger='cron', second='*/5')



#timer
def timer_SMS(days_,body,to_number):
    from apscheduler.schedulers.background import BackgroundScheduler


    count=0
    def SMS1(body,to_number,count):

        to_number=4802552099
        from twilio.rest import Client

        # Your Account SID from twilio.com/console
        account_sid = "AC3d0e45500fdd987d07b4cd6f594b7ee5"
        # Your Auth Token from twilio.com/console
        auth_token  = "91a8726ff72cf2708643a513724d2997"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to='+1'+str(to_number),
            from_="+14803780697",
            body=str(body))
        global count, scheduler

        # Execute the job till the count of 5
        count += 1
        if count == 5:
            scheduler.remove_job('my_job_id')


    scheduler = BackgroundScheduler()
    scheduler.add_job(SMS1(body,to_number), 'interval', seconds=int(days_)*86400, id='my_job_id')
    scheduler.start()



#
# #json to dataframe
# import json
# import pandas as pd
# with open('test.json', 'r') as f:
#     data = json.load(f)
# pd = pd.DataFrame.from_dict(data, orient='index')
# # train.reset_index(level=0, inplace=True)


# In[350]:



# In[334]:



def select_group(list_,mode,number):
    import random
#     list_=
    if mode=="random":
        random.shuffle(list_)
        return (list_[:number])
    else:
        return (list_[:number])



#find cell
import re
def find_cell(json):
    import re
    cell_list=(re.findall(r'\d{10,13}' , json ,re.I|re.M))

    return cell_list
# print(find_cell(json))

#find email
def find_email(json):
    import re
    email_list=(re.findall(r'\w*\@\w+\.\w+' , json ,re.I|re.M))

    return email_list
# print(find_email(json))


def SMS1(body,to_number0):
    to_number0=[]

    to_number=4802552099
    from twilio.rest import Client

    # Your Account SID from twilio.com/console
    account_sid = "AC3d0e45500fdd987d07b4cd6f594b7ee5"
    # Your Auth Token from twilio.com/console
    auth_token  = "91a8726ff72cf2708643a513724d2997"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to='+1'+str(to_number),
        from_="+14803780697",
        body=str(body))

    # print(message.sid)

def phone1(to_number0):
    to_number0=[]
    to_number=4802552099
    from twilio.rest import Client
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = "AC3d0e45500fdd987d07b4cd6f594b7ee5"
    # Your Auth Token from twilio.com/console
    auth_token  = "91a8726ff72cf2708643a513724d2997"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            url='http://demo.twilio.com/docs/voice.xml',
                            to='+1'+str(to_number),
                            from_="+14803780697"
                        )


# In[6]:

def SMS2(body,to_number0):
    to_number0[]
    to_number=4252406185
    from twilio.rest import Client

    # Your Account SID from twilio.com/console
    account_sid = "AC7ce8816749a9678e91f9b3b63b245db1"
    # Your Auth Token from twilio.com/console
    auth_token  = "6cca0278886c131a1e4b9c460513a30b"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to='+1'+str(to_number),
        from_="+12155443131",
        body=str(body))

    print(message.sid)


# In[248]:

def phone2(to_number0):
    to_number0=[]
    to_number=4252406185
    from twilio.rest import Client

    # Your Account SID from twilio.com/console
    account_sid = "AC7ce8816749a9678e91f9b3b63b245db1"
    # Your Auth Token from twilio.com/console
    auth_token  = "6cca0278886c131a1e4b9c460513a30b"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            url='http://demo.twilio.com/docs/voice.xml',
                            to='+1'+str(to_number),
                            from_="+12155443131"
                        )
