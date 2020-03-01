import requests

class Weather_API:

    def __init__(self, appid, units="metric"):
        self.key = appid
        self.unit = units

    def Get_Data_By_id(self, id=1258847, lang="en"):
        url = "http://api.openweathermap.org/data/2.5/weather?id={}&units={}&lang={}&appid={}".format(id, self.unit, lang, self.key)
        return requests.get(url).json()

    def Get_Data_By_cityname(self,name="Rajkot", lang="en"):
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units={}&lang={}&appid={}".format(name, self.unit, lang, self.key)
        return requests.get(url).json()
    
    def Get_Data_By_geoCor(self, lon=70.783333, lat=22.299999, lang="en"):
        url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&lang={}&appid={}".format(lat, lon, self.unit, lang, self.key)
        return requests.get(url).json()
    
    def Get_Data_By_zip(self, zip=360004, country="IN", lang="en"):
        url = "http://api.openweathermap.org/data/2.5/weather?zip={},{}&units={}&lang={}&appid={}".format(zip, country, self.unit, lang, self.key)
        return requests.get(url).json()
