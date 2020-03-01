try:
    import json
    import requests
    from email.message import EmailMessage
    import imghdr
    import smtplib
    import sys
    from WM import Weather_API
    import datetime
    from log import Logger
    print("Modules Successfully Imported...")        
except:
    print("Error IN PROCESS OF MODULE IMPORTING")
    print("next part of script will not be executed...")
    exit()

try:
    Fail = Logger("Fail", logfile="LogFiles\\logReport[main].log")
    Pass = Logger("Pass", logfile="LogFiles\\logReport[main].log")
    Fail.Set_File = True
    Fail.Set_Stream = True
    Pass.Set_File = True
    Pass.Set_Stream = True
    Pass.D("Logger Successfully Created...")
except:
    print("Error IN CREATING LOGGER")
    print("next part of script will not be executed...")
    exit()

try:
    email_add = "EMAIL OR GMAIL ACCOUNT"
    email_pass = "YOUR GENERATED PASSWORD"
    RECIEVER_EMAIL = ""
    key_1 = "YOUR OPEN-WEATHER-MAP API KEY"
    id_ = 0
    Name_Of_City = ""
    Input = ["Fail"]
    I = [0]
    Check_Point = True
    Check_List = 0
    Pass.D("Common Variables Successfully Created...")
except:
    Fail.C("Error IN PROCESS OF COMMON SETTING VARIABLES")
    print("next part of script will not be executed...")
    Pass.I("Script Written By Akshay Pandya...\n")
    exit()

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

print("""
How Do You Want To Continue The Script...
1] With Data Of Input File
2] With New Inputs
""")

while Input[0] == "Fail":
    I[0] = int(input("Enter Answer> "))
    if I[0] == 1:
        try:
            with open("Name_Of_City.txt") as n:
                cont = n.read()
                Scont = cont.split(">")
                RECIEVER_EMAIL = Scont[2]
                Name_Of_City = Scont[4]
                Pass.D("Name_Of_City.txt Successfully Read...")
            try:
                with open("Weather_Map\\city.list.json", encoding="utf8") as city:
                    try:
                        map_ = json.load(city)
                        for i in map_:
                            if i["name"] == Name_Of_City:
                                id_ = i["id"]
                                Pass.D("City Found!!!")
                                break
                            else:
                                pass
                    except:
                        Fail.E("Error IN PROCESS OF CITY_MAP JSON PARSING")
                        pass        
            except:
                Fail.E("Error IN PROCESS OF CITY_MAP LOADING")
                pass
        except:
            Fail.E("Error IN PROCESS OF READING Name_Of_City.txt")
            pass
        if id_ == 0:
            Fail.E("Error IN PROCESS OF FINDING CITY FROM CITY_MAP")
            id_ = 1258847
            Name_Of_City = "Rajkot"
            RECIEVER_EMAIL = "akkypan99@gmail.com"
            pass
        else:
            pass
        Input[0] = "Done"
    elif I[0] == 2:
        print()
        print("Check That First Character Is CAPITAL")
        print()
        Name_Of_City = str(input("Name_Of_City> "))
        RECIEVER_EMAIL = str(input("Reciever_Email> "))
        Pass.D("User Input Recieved...")
        try:
            with open("Weather_Map\\city.list.json", encoding="utf8") as city:
                try:
                    map_ = json.load(city)
                    for i in map_:
                        if i["name"] == Name_Of_City:
                            id_ = i["id"]
                            Pass.D("City Found!!!")
                            break
                        else:
                            pass
                except:
                    Fail.E("Error IN PROCESS OF CITY_MAP JSON PARSING")
                    pass        
        except:
            Fail.E("Error IN PROCESS OF CITY_MAP LOADING")
            pass
        if id_ == 0:
            Fail.E("Error IN PROCESS OF FINDING CITY FROM CITY_MAP")
            id_ = 1258847
            Name_Of_City = "Rajkot"
            RECIEVER_EMAIL = "akkypan99@gmail.com"
            pass
        else:
            pass
        Input[0] = "Done"
    else:
        print("""Invalid Input...
        Please Try Again""")

try:
    weather = Weather_API(key_1)
    Pass.D("Weather_API Class Successfully Called...")
except:
    Fail.E("Error IN PROCESS OF CALLING Weather_API CLASS")
    Check_Point = False
    pass

print("Importing Data From Api...")

try:
    data = weather.Get_Data_By_id(id=id_)
    Pass.D("Data Successfully Imported From Api...")
except:
    Fail.E("Error IN PROCESS OF DATA IMPORTING")
    Check_Point = False
    pass

if Check_Point == True:
    Dict_Final = Data_Sorter(data)
    Pass.D("Data Successfully Sorted...")
else:
    Fail.E("Error IN PROCESS OF DATA SORTING")
    pass

try:
    msg = EmailMessage()
    Pass.D("EmailMessage Function Successfully Called...")
except: 
    Fail.C("Error IN PROCESS OF CALLING EmailMessage FUNCTION")
    print("next part of script will not be executed...")
    Pass.I("Script Written By Akshay Pandya...\n")
    exit()

try:
    msg["Subject"] = "Weather_Info[{}]".format(Name_Of_City)
    Pass.D("Subject Successfully Created...")
except:
    Fail.E("Error IN PROCESS OF SUBJECT CREATION")
    msg["Subject"] = "[Automation_Weather]"
    pass

try:
    msg["From"] = email_add
    Pass.D("Sender Email Successfully Set...")
except:
    Fail.C("Error IN PROCESS OF SETTING SENDER EMAIL")
    print("next part of script will not be executed...")
    Pass.I("Script Written By Akshay Pandya...\n")
    exit()

try:
    msg["To"] = RECIEVER_EMAIL
    Pass.D("Reciever Email Successfully Set...")
except:
    Fail.C("Error IN PROCESS OF SETTING RECIEVER EMAIL")
    print("next part of script will not be executed...")
    Pass.I("Script Written By Akshay Pandya...\n")
    exit()

try:
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
    Pass.D("Message Successfully Created...")
except:
    Fail.E("Error IN PROCESS OF SETTING CONTENT OF MESSAGE")
    msg.set_content("Sorry, We were unable to load your requested data.")

try:
    while Check_List <= 10: 
        if Check_List < 10:
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    Pass.D("Server Connection Is Successfull...")
                    try:
                        smtp.login(email_add, email_pass)
                        Pass.D("Account Login Is Successfull...")
                    except:
                        Fail.C("Error IN PROCESS OF LOGIN")
                        pass
                    try:
                        smtp.send_message(msg)
                        Pass.D("Message Is Successfully Sent...")
                        Pass.I("Script Written By Akshay Pandya...\n")
                        Check_List = 99
                    except:
                        Fail.C("Error IN PROCESS OF SENDING EMAIL")
                        pass
            except:
                Fail.E("Retrying...[{}]".format(Check_List + 1))
                Check_List += 1
                pass
        elif Check_List == 10:
            Fail.C("FAILED TO CONNECT TO SERVER")
            print()
            print("Please Try Again Later.")
            print()
            Pass.I("Script Written By Akshay Pandya...\n")
            exit()
except:
    exit()