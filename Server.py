import imaplib
import smtplib
import email
from email.message import EmailMessage
from bs4 import BeautifulSoup
import json
import datetime
import time
import sys
from WM import Weather_API
from log import Logger

details = "EMAIL OR GMAIL ID($)GENERATED PASSWORD"

key = "OPEN-WEATHER-MAP API KEY"

path = "Weather_Map\\city.list.json"

try:
    Fail = Logger("Fail", logfile="LogFiles\\logReport[server].log")
    Pass = Logger("Pass", logfile="LogFiles\\logReport[server].log", list_=[4,4,4])
    Fail.Set_File = True
    Fail.Set_Stream = True
    Pass.Set_File = True
    Pass.Set_Stream = True
    Pass.D("Logger Successfully Created...")
except:
    pass


def Data_Sorter(data):
    dic = {}
    key_1 = []
    key_2 = ['lon', 'lat', 'id', 'main', 'description', 'icon', 'base', 'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity', 'sea_level', 'grnd_level', 'speed', 'deg', 'all', 'dt', 'country', 'sunrise', 'sunset', 'timezone', 'id', 'name', 'cod']
    for i in list(data.keys()):
        try:
            for j in list(data[i].keys()):
                dic[j] = data[i][j]
                key_1.append(j)
        except:
            try:
                for j in list(data[i][0].keys()):
                    dic[j] = data[i][0][j]
                    key_1.append(j)
            except:
                dic[i] = data[i]
                key_1.append(i)
    for i in key_2:
        if i not in key_1:
            dic[i] = ""
        else:
            pass
    return dic

class Input_Server:

    def __init__(self):

        self.set_server = 0
        self.login = 0
        self.logout = 0
        self.inbox_select = 0
        self.inbox = 0
        self.email = 0
        self.select_all = 0
        self.store_all = 0
        self.select_bin = 0
        self.store_del = 0
        self.exp = 0
        self.cls = 0
        self.mail = 0
        self.dict = 0
        self.set_server_b = False
        self.login_b = False
        self.logout_b = False
        self.inbox_select_b = False
        self.inbox_b = False
        self.email_b = False
        self.select_all_b = False
        self.store_all_b = False
        self.select_bin_b = False
        self.store_del_b = False
        self.exp_b = False
        self.cls_b = False
        self.mail_b = False
        self.dict_b = True
        
        while self.set_server_b == False:
            if self.set_server < 10:
                try:

                    self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
                    self.set_server_b =True
                    Pass.D("Input Server Successfully Refreshed...")
        
                except:
                    self.set_server += 1
                    Fail.E("Error IN PROCESS OF REFRESHING INPUT SERVER")

            elif self.set_server == 10:
                Fail.C("Input Server Not Refreshed : Shutting Down Server")
                exit()
            
            else:
                pass


        self.username = str
        self.password = str

    def Login(self):

        while self.login_b == False:
            if self.login < 10:
                try:
        
                    self.imap.login(self.username,self.password)
                    self.login_b = True
                    Pass.D("Login Via Input Server Successfully Done...")
        
                except:
                    self.login += 1
                    Fail.E("Error IN PROCESS OF LOGIN VIA INPUT SERVER")

            elif self.login == 10:
                Fail.C("Input Login Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

    def Logout(self):
        
        while self.logout_b == False:
            if self.logout < 10:
                try:
        
                    self.imap.logout()
                    self.logout_b = True
                    Pass.D("Logout Via Output Server Successfully Done...")
        
                except:
                    self.logout += 1
                    Fail.E("Error IN PROCESS OF LOGOUT VIA INPUT SERVER")
            
            elif self.logout == 10:
                Fail.C("Input Logout Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

    def Fetch_Inbox(self, Request_Dict = {}):

        self.imap.select("inbox")

        self.inbox_item_list = self.imap.uid("search", None, "ALL")[1][0].split()

        for x in self.inbox_item_list:
            
            City = []
            self.email_data = self.imap.uid("fetch", x, "(RFC822)")[1][0][1]      
            Mail = email.message_from_bytes(self.email_data)

            if Mail["Subject"] == "Send me weather":

                for M in Mail.walk():

                    if M.get_content_maintype() == "multipart":

                        for c in M.get_payload():
                            
                            if c.get_content_subtype() == "plain":
                            
                                string =c.get_payload()
                                City.append(string.strip())
                            
                            elif c.get_content_subtype() == "html":
                            
                                html = c.get_payload()
                                soup = BeautifulSoup(html, "html5lib")
                                text =soup.find("div",dir="auto") 
                                City.append(text.text)
                            
                            else:
                                pass
                    
                    else:
                        
                        if M.get_content_subtype() == "plain":
                        
                            string_ = M.get_payload()
                            City.append(string_.strip())
                        
                        elif M.get_content_subtype() == "html":
                        
                            html_ = M.get_payload()
                            soup_ = BeautifulSoup(html_, "html5lib")
                            text_ = soup_.find("div",dir="auto")
                            City.append(text_.text)
                        else:
                            pass

                City = list(set(City))
            
                if (((("{}".format( Mail["From"])).split("<"))[-1]).split(">"))[0] not in Request_Dict.keys():
            
                    Request_Dict[(((("{}".format( Mail["From"])).split("<"))[-1]).split(">"))[0]] = City
            
                elif (((("{}".format( Mail["From"])).split("<"))[-1]).split(">"))[0] in Request_Dict.keys():
            
                    for z in City:
            
                        Request_Dict[(((("{}".format( Mail["From"])).split("<"))[-1]).split(">"))[0]].append(z)
            
                else:
                    pass

            else:
                pass

        return Request_Dict

    def Clear_Inbox(self):
        
        while self.select_all_b == False:
            if self.select_all < 10:
                try:

                    self.imap.select('"[Gmail]/All Mail"')
                    self.select_all_b = True
                    Pass.D("All_Mail Folder Selection Successfully Done...")

                except:
                    self.select_all += 1
                    Fail.E("Error IN PROCESS OF SELECTING ALL MAIL FOLDER VIA INPUT SERVER")
            
            elif self.select_all == 10:
                Fail.C("All Mail Folder Selection Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

        while self.store_all_b == False:
            if self.store_all < 10:
                try:

                    self.imap.store("1:*", "+X-GM-LABELS", "\\Trash")
                    self.store_all_b = True
                    Pass.D("Trash Store Successfully Done...")

                except:
                    self.store_all += 1
                    Fail.E("Error IN PROCESS OF TRASH STORING VIA INPUT SERVER")

            elif self.store_all == 10:
                Fail.C("Trash Store Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

        while self.select_bin_b == False:
            if self.select_bin < 10:
                try:

                    self.imap.select('"[Gmail]/Bin"')
                    self.select_bin_b = True
                    Pass.D("Bin Folder Selection Successfully Done...")

                except:
                    self.select_bin += 1
                    Fail.E("Error IN PROCESS OF BIN FOLDER SELECTION VIA INPUT SERVER")
            
            elif self.select_bin == 10:
                Fail.C("Bin Folder Selection Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

        while self.store_del_b == False:
            if self.store_del < 10:
                try:

                    self.imap.store("1:*", "+FLAGS", "\\Deleted")
                    self.store_del_b = True
                    Pass.D("Deleted Store Successfully Done...")

                except:
                    self.store_del += 1
                    Fail.E("Error IN PROCESS OF DELETED STORING VIA INPUT SERVER")
            
            elif self.store_del == 10:
                Fail.C("Deleted Sorting Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

        while self.exp_b == False:
            if self.exp < 10:
                try:

                    self.imap.expunge()
                    self.exp_b = True
                    Pass.D("Expunge Successfully Done...")

                except:
                    self.exp += 1
                    Fail.E("Error IN EXPUNGE PROCESS VIA INPUT SERVER")
            
            elif self.exp == 10:
                Fail.C("Expunging Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

        while self.cls_b == False:
            if self.cls < 10:
                try:

                    self.imap.close()
                    self.cls_b = True
                    Pass.D("Closing Successfully Done...")

                except:
                    self.cls += 1
                    Fail.E("Error IN CLOSING PROCESS VIA INPUT SERVER")
            
            elif self.cls == 10:
                Fail.C("Closing Not Done : Shutting Down Server")
                exit()
            
            else:
                pass


    @property
    def Set_Server_Det(self):
        pass

    @Set_Server_Det.setter
    def Set_Server_Det(self, details=str):
        self.username = details.split("($)")[0]
        self.password = details.split("($)")[1]


class Output_Server:

    def __init__(self):

        self.set_server = 0
        self.set_server_b = False
        self.login = 0
        self.login_b = False
        self.logout = 0
        self.logout_b = False
        self.city = 0
        self.city_b = False
        self.weat = 0
        self.weat_b = False
        self.msgs = 0
        self.msgs_b = False
        self.send = 0
        self.send_b = False
        self.jsn = 0
        self.jsn_b = False

        self.Map_path = str

        while self.set_server_b == False:
            if self.set_server < 10:
                try:
                    self.smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    self.set_server_b = True
                    Pass.D("Output Server Successfully Refreshed...")
                
                except:
                    self.set_server +=1
                    Fail.E("Error IN PROCESS OF SERVER REFRESHING VIA OUTPUT SERVER")
            
            elif self.set_server == 10:
                Fail.C("Output Server Not Refreshed : Shutting Down Server")
                exit()
            
            else:
                pass

        self.username = str
        self.password = str
        self.API_key = str

    def Login(self):

        while self.login_b == False:
            if self.login < 10:
                try:
                    self.smtp.login(self.username, self.password)
                    self.login_b = True
                    Pass.D("Login Via Output Server Successfully Done...")
                
                except:
                    self.login += 1
                    Fail.E("Error IN PROCESS OF LOGIN VIA OUTPUT SERVER")
            
            elif self.login == 10:
                Fail.C("Login Via Output Server Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

    def Logout(self):

        while self.logout_b == False:
            if self.logout < 10:
                try:        
                    self.smtp.quit()
                    self.logout_b = True
                    Pass.D("Logout Via Output Server Successfully Done...")
                
                except:
                    self.logout += 1
                    Fail.E("Error IN PROCESS OF LOGOUT VIA OUTPUT SERVER")
            
            elif self.logout == 10:
                Fail.C("Logout Via Output Server Not Done : Shutting Down Server")
                exit()
            
            else:
                pass

    @property
    def Set_Server_Det(self):
        pass

    @Set_Server_Det.setter
    def Set_Server_Det(self, details=str):
        self.username = details.split("($)")[0]
        self.password = details.split("($)")[1]

    @property
    def Set_Server_Key(self):
        pass

    @Set_Server_Key.setter
    def Set_Server_Key(self, key=str):
        self.API_key = key

    @property
    def Set_Map_Path(self):
        pass

    @Set_Map_Path.setter
    def Set_Map_Path(self, path=str):
        self.Map_path = path


    def Send_Output(self,Request_Dict={}):

        for key in Request_Dict.keys():
            RECIEVER_EMAIL = key

            for city in Request_Dict[key]:
                Name_Of_City = city
                id_ = 0

                while self.city_b == False:
                    if self.city < 10:
                        try:
                            with open(self.Map_path, encoding="utf8") as city:
                                self.city_b = True    
                                while self.jsn_b == False:
                                    if self.jsn < 10:
                                        try:
                                            map_ = json.load(city)

                                            for i in map_:
                                                if i["name"] == Name_Of_City:
                                                    id_ = i["id"]
                                                    break
                                                else:
                                                    pass
                                            
                                            self.jsn_b = True
                                     
                                            Pass.D("JSON Loading Via Output Server Successfully Done...")
                                        except:
                                            self.jsn += 1
                                            Fail.E("Error IN PROCESS OF JSON LOADING VIA OUTPUT SERVER")

                                    elif self.jsn == 10:
                                        Fail.C("JSON Loading Via Output Server Not Done : Shutting Down Server")
                                        exit()
                                    
                                    else:
                                        pass
                            Pass.D("MAP Loading Via Output Server Successfully Done...")
                        except:
                            self.city += 1
                            Fail.E("Error IN PROCESS OF MAP LOADING VIA OUTPUT SERVER")
                    
                    elif self.city == 10:
                        Fail.C("MAP Loading Via Output Server Not Done : Shutting Down Server")
                        exit()
                    
                    else:
                        pass

                while self.weat_b == False:
                    if self.weat < 10:
                        try:
                            weather = Weather_API(self.API_key)
                
                            data = weather.Get_Data_By_id(id=id_)

                            Dict_Final = Data_Sorter(data)

                            self.weat_b = True

                            Pass.D("Weather Data Sorting Via Output Server Successfully Done...")
                
                        except:
                            self.weat += 1
                            Fail.E("Error IN PROCESS OF WEATHER DATA SORTING VIA OUTPUT SERVER")
                    
                    elif self.weat == 10:
                        Fail.C("Weather Data Sorting Via Output Server Not Done : Shutting Down Server")
                        exit()
                    
                    else:
                        pass
                
                
                while self.msgs_b == False:
                    if self.msgs < 10:
                        try:
                            msg = EmailMessage()

                            msg["Subject"] = "Weather_Info[{}]".format(Name_Of_City)

                            msg["From"] = self.username

                            msg["To"] = RECIEVER_EMAIL

                            if id_ == 0:
                                msg.set_content("Sorry, We were unable to load your requested data.")
                
                            else:
                                msg.set_content("""
    Weather Report Of {}...

    Longitude : {}
    Latitude  : {}

    Sky Condition : {}
    Sky Information : {}

    Temprature : {}
    Feels Like : {}
    Maximum Temprature : {}
    Minimum Temprature : {}

    Pressure : {}
    Sea Level Pressure : {}
    Ground Level Pressure : {}
    
    Humidity : {}
    Wind Speed : {}
    Wind Direction : {}
    
    Sunrise Time : {}
    Sunset Time : {}
    
    [If some of the parameters are left blank, those info may not be available for particular city.]
    [If there is no info in message(all parameters are blank), there must be some error while importing data, we're sincearly sorry for that.]
    
    Have A Nice Day ...
    """.format(Name_Of_City, Dict_Final["lon"], Dict_Final["lat"], Dict_Final["main"], Dict_Final["description"], "{} C".format(Dict_Final["temp"]), "{} C".format(Dict_Final["feels_like"]), "{} C".format(Dict_Final["temp_max"]), "{} C".format(Dict_Final["temp_min"]), "{} mbar".format(Dict_Final["pressure"]), "{} mbar".format(Dict_Final["sea_level"]), "{} mbar".format(Dict_Final["grnd_level"]), "{} %".format(Dict_Final["humidity"]), "{} meter/sec".format(Dict_Final["speed"]), "{} degree".format(Dict_Final["deg"]), datetime.datetime.fromtimestamp(Dict_Final["sunrise"]).strftime("%I:%M %p"), datetime.datetime.fromtimestamp(Dict_Final["sunset"]).strftime("%I:%M %p")))
                                self.msgs_b = True
                            
                            Pass.D("Message Setting Via Output Server Successfully Done...")
                        
                        except:
                            self.msgs += 1
                            Fail.E("Error IN PROCESS OF MESSAGE SETTING VIA OUTPUT SERVER")
                    
                    elif self.msgs == 10:
                        Fail.C("Message Setting Via Output Server Not Done : Shutting Down Server")
                        exit()
                    
                    else:
                        pass
                
                while self.send_b == False:
                    if self.send < 10:
                        try:
                            self.smtp.send_message(msg)
                            self.send_b = True
                            Pass.D("Message Sending Via Output Server Successfully Done...")
                    
                        except:
                            self.send += 1
                            Fail.E("Error IN PROCESS OF MESSAGE SENDING VIA OUTPUT SERVER")
                    
                    elif self.send == 10:
                        Fail.C("Message Sending Via Output Server Not Done : Shutting Down Server")
                        exit()
                    
                    else:
                        pass

        Request_Dict.clear()


def Server_ON_Air(det, key, path):
    while True:
        Input = Input_Server()
        Output = Output_Server()
        Input.Set_Server_Det = det
        Output.Set_Server_Det = det
        Output.Set_Server_Key = key
        Output.Set_Map_Path = path
        Input.Login()
        dict_ = Input.Fetch_Inbox()
        Input.Clear_Inbox()
        Input.Logout()
        Output.Login()
        Output.Send_Output(dict_)
        Output.Logout()
        time.sleep(5)

Server_ON_Air(details, key, path)
