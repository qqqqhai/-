import requests
from GenerateJWT import get_token

#获得省份名，城市名，Location ID
def city_lookup(location):
    TOKEN = get_token()
    API_HOST = "nm3h2rumfr.re.qweatherapi.com"
    url = f"https://{API_HOST}/geo/v2/city/lookup"

    params = {
        "location": location,      # 支持拼音、汉字、经纬度、LocationID
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()          # 检查HTTP状态码
        data = resp.json()               # 解析JSON
        # 假设 data 是从 resp.json() 得到的字典
        locations = data.get("location", [])  # 获取地点列表，默认为空列表
        result_list = []
        for loc in locations:
            result_list.append({
                "province": loc.get("adm1", ""),
                "city": loc.get("name", ""),
                "id": loc.get("id", ""),
                "城市纬度": loc.get("lat", ""),
                "城市经度": loc.get("lon", "")
            })
        return result_list
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")

#获得days天的天气信息
def get_today_weather(location_id):
    TOKEN = get_token()
    API_HOST = "nm3h2rumfr.re.qweatherapi.com"
    days = "15d"
    url = f"https://{API_HOST}//v7/weather/{days}"
    params = {
        "location": location_id,
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        daily = data.get("daily", [])  # 获取地点列表，默认为空列表
        result_list = []
        for loc in daily:
            result_list.append({
                "预报日期": loc.get("fxDate", ""),
                "预报当天最高温度": loc.get("tempMax", ""),
                "预报当天最低温度": loc.get("tempMin", ""),
                "白天天气状况的图标代码": loc.get("iconDay", ""),
                "白天天气状况的文字描述": loc.get("textDay", ""),
                "白天风向": loc.get("windDirDay", ""),
                "晚上天气状况的文字描述": loc.get("textNight", ""),
                "白天风力等级": loc.get("windScaleDay", ""),
                "当天总降水量": loc.get("precip", ""),
                "相对湿度": loc.get("humidity", ""),
                "云量": loc.get("cloud", ""),
            })
        return result_list
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")

#获得实时天气预报
def get_realtime_weather(location_id):
    TOKEN = get_token()
    API_HOST = "nm3h2rumfr.re.qweatherapi.com"
    url = f"https://{API_HOST}/v7/weather/now"
    params = {
        "location": location_id,
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        now = data.get("now", [])  # 获取地点列表，默认为空列表
        now_list = [{
            "预报日期": now.get("obsTime", ""),
            "当天温度": now.get("temp", ""),
            "体感温度": now.get("feelsLike", ""),
            "天气状况的图标代码": now.get("icon", ""),
            "天气状况的文字描述": now.get("text", ""),
            "风向": now.get("windDir", ""),
            "风速": now.get("windSpeed", ""),
            "风级": now.get("windScale", ""),
            "过去1小时降水量": now.get("precip", ""),
            "相对湿度": now.get("humidity", ""),
            "云量": now.get("cloud", "")
        }]

        return now_list
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")

#获得天气预警:
def get_weather_warning(latitude,longitude):
    TOKEN = get_token()
    API_HOST = "nm3h2rumfr.re.qweatherapi.com"
    url = f"https://{API_HOST}/weatheralert/v1/current/{latitude}/{longitude}"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        response = requests.get(url,  headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        alerts = data.get("alerts", [])

        extracted = []
        for alert in alerts:
            extracted.append({
                "headline": alert.get("headline"),
                "description": alert.get("description"),
                "criteria": alert.get("criteria"),
                "instruction": alert.get("instruction")
            })
        if extracted:
            return extracted
        else:
            return "没有天气预警"
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")


if __name__=="__main__":
    location1 = input("请输入城市名：")
    result_list1 = city_lookup(location1)
    for item in result_list1:
        city_name = item["city"]
        city_id = item["id"]
        lat=item["城市纬度"]
        lon=item["城市经度"]
        today_weather = get_realtime_weather(city_id)
        #print(f"城市：{city_name}，ID：{city_id},当日天气信息:{today_weather}")
        #weather_warning = get_weather_warning(lat,lon)
        #print(f"城市：{city_name}，ID：{city_id},天气预警信息:{weather_warning}")
        weather=get_today_weather(city_id)
        print(weather[1])
        """for i in range(1,3):
            print(f"城市：{city_name}，ID：{city_id},当日天气信息:{weather[i]}")"""