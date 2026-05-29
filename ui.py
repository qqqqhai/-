import streamlit as st
import pandas as pd
from datetime import datetime

from demo import city_lookup, get_realtime_weather, get_today_weather, get_weather_warning


def get_city_info(city_name):
    """调用 API 获取城市编码和经纬度"""
    result = city_lookup(city_name)
    if result and len(result) > 0:
        return result[0]
    return None


def fetch_realtime(city_id):
    """获取实时天气"""
    data = get_realtime_weather(city_id)
    if data and len(data) > 0:
        return data[0]
    return None


def fetch_forecast(city_id):
    """获取多日天气预报"""
    data = get_today_weather(city_id)
    if data:
        return data
    return []


def fetch_warnings(lat, lon):
    """获取天气预警"""
    data = get_weather_warning(lat, lon)
    if data and isinstance(data, list):
        return data
    return []


#页面配置
st.set_page_config(page_title="天气预报", page_icon="🌤️", layout="wide")
st.title("🌤️ 天气预报仪表板")
st.markdown("---")

# 侧边栏
st.sidebar.header("位置选择")

# 省市数据
CITIES_DATA = {
    "北京市": ["北京"], "天津市": ["天津"], "上海市": ["上海"], "重庆市": ["重庆"],
    "河北": ["石家庄", "唐山", "秦皇岛", "邯郸", "邢台", "保定", "张家口", "承德", "沧州", "廊坊", "衡水"],
    "山西": ["太原", "大同", "朔州", "忻州", "阳泉", "吕梁", "晋中", "长治", "晋城", "临汾", "运城"],
    "辽宁": ["沈阳", "大连", "鞍山", "抚顺", "本溪", "丹东", "锦州", "营口", "阜新", "辽阳", "盘锦", "铁岭", "朝阳", "葫芦岛"],
    "吉林": ["长春", "吉林", "四平", "辽源", "通化", "白山", "松原", "白城"],
    "黑龙江": ["哈尔滨", "齐齐哈尔", "鸡西", "鹤岗", "双鸭山", "大庆", "伊春", "佳木斯", "七台河", "牡丹江", "黑河", "绥化"],
    "江苏": ["南京", "苏州", "无锡", "常州", "镇江", "南通", "连云港", "淮安", "盐城", "扬州", "泰州", "宿迁"],
    "浙江": ["杭州", "宁波", "温州", "嘉兴", "湖州", "绍兴", "金华", "衢州", "舟山", "台州", "丽水"],
    "安徽": ["合肥", "芜湖", "蚌埠", "淮南", "马鞍山", "淮北", "铜陵", "安庆", "黄山", "滁州", "阜阳", "宿州", "六安", "亳州", "池州", "宣城"],
    "福建": ["福州", "厦门", "莆田", "三明", "泉州", "漳州", "南平", "龙岩", "宁德"],
    "江西": ["南昌", "景德镇", "萍乡", "九江", "新余", "鹰潭", "赣州", "吉安", "宜春", "抚州", "上饶"],
    "山东": ["济南", "青岛", "淄博", "枣庄", "东营", "烟台", "潍坊", "济宁", "泰安", "威海", "日照", "临沂", "德州", "聊城", "滨州", "菏泽"],
    "河南": ["郑州", "开封", "洛阳", "平顶山", "安阳", "鹤壁", "新乡", "焦作", "濮阳", "许昌", "漯河", "三门峡", "南阳", "商丘", "信阳", "周口", "驻马店"],
    "湖北": ["武汉", "黄石", "十堰", "宜昌", "襄阳", "鄂州", "荆门", "孝感", "荆州", "黄冈", "咸宁", "随州"],
    "湖南": ["长沙", "株洲", "湘潭", "衡阳", "邵阳", "岳阳", "常德", "张家界", "益阳", "郴州", "永州", "怀化", "娄底"],
    "广东": ["广州", "深圳", "珠海", "佛山", "韶关", "汕头", "湛江", "肇庆", "江门", "茂名", "惠州", "梅州", "汕尾", "河源", "阳江", "清远", "东莞", "中山", "潮州", "揭阳", "云浮"],
    "海南": ["海口", "三亚", "三沙", "儋州"],
    "四川": ["成都", "自贡", "攀枝花", "泸州", "德阳", "绵阳", "广元", "遂宁", "内江", "乐山", "南充", "眉山", "宜宾", "广安", "达州", "雅安", "巴中", "资阳"],
    "贵州": ["贵阳", "六盘水", "遵义", "安顺", "毕节", "铜仁"],
    "云南": ["昆明", "曲靖", "玉溪", "保山", "昭通", "丽江", "普洱", "临沧"],
    "陕西": ["西安", "铜川", "宝鸡", "咸阳", "渭南", "延安", "汉中", "榆林", "安康", "商洛"],
    "甘肃": ["兰州", "嘉峪关", "金昌", "白银", "天水", "武威", "张掖", "平凉", "酒泉", "庆阳", "定西", "陇南"],
    "青海": ["西宁"],
    "台湾": ["台北", "新北", "桃园", "台中", "台南", "高雄"],
    "内蒙古": ["呼和浩特", "包头", "乌海", "赤峰", "通辽", "鄂尔多斯", "呼伦贝尔", "巴彦淖尔", "乌兰察布"],
    "广西": ["南宁", "柳州", "桂林", "梧州", "北海", "防城港", "钦州", "贵港", "玉林", "百色", "贺州", "河池", "来宾", "崇左"],
    "西藏": ["拉萨"],
    "宁夏": ["银川", "石嘴山", "吴忠", "固原", "中卫"],
    "新疆": ["乌鲁木齐", "克拉玛依"],
    "香港": ["香港"], "澳门": ["澳门"]
}

provinces = list(CITIES_DATA.keys())
selected_province = st.sidebar.selectbox("省份", provinces, key="province")
cities_in_province = CITIES_DATA.get(selected_province, [])
selected_city = st.sidebar.selectbox("城市", cities_in_province, key="city")

st.sidebar.markdown("---")
st.sidebar.header(" 功能选择")
selected_tab = st.sidebar.radio(
    "选择板块",
    ["🌡️ 实时天气", "📅 天气预报", "⚠️ 天气预警"],
    label_visibility="collapsed"
)

if st.sidebar.button("🔍 查询天气", use_container_width=True, type="primary"):
    st.session_state.city_selected = selected_city
    st.session_state.query_triggered = True

if "city_selected" not in st.session_state:
    st.session_state.city_selected = None
if "query_triggered" not in st.session_state:
    st.session_state.query_triggered = False

city_to_query = st.session_state.city_selected if st.session_state.query_triggered else selected_city

if not city_to_query:
    st.info("请在左侧选择一个城市并点击「查询天气」")
    st.stop()

with st.spinner(f"正在查询 {city_to_query} 的天气信息..."):
    city_info = get_city_info(city_to_query)

if city_info is None:
    st.error(f"未找到城市「{city_to_query}」的信息")
    st.stop()

city_id = city_info["id"]
city_lat = city_info.get("城市纬度", "")
city_lon = city_info.get("城市经度", "")

st.success(f" 当前城市：{city_info['city']}（{city_info['province']}）")

#实时天气
if selected_tab == "🌡️ 实时天气":
    st.subheader(f"🌡️ 实时天气 - {city_to_query}")
    realtime = fetch_realtime(city_id)
    if realtime:
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("🌡️ 温度", f"{realtime.get('当天温度','--')}°C")
        with col2: st.metric("💧 湿度", f"{realtime.get('相对湿度','--')}%")
        with col3: st.metric("🌬️ 风向", realtime.get('风速','--'))
        with col4: st.metric("🍃 风力", f"{realtime.get('风级','--')}级")
        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        with col_a: st.metric("🤗 体感", f"{realtime.get('体感温度','--')}°C")
        with col_b: st.metric("🌤️ 天气", realtime.get('天气状况的文字描述','--'))
        with col_c: st.metric("☁️ 云量", f"{realtime.get('云量','--')}%")
        if realtime.get("预报日期",""): st.caption(f"更新：{realtime['预报日期']}")
    else:
        st.warning("⚠️ 未获取到实时天气数据")

# 天气预报
elif selected_tab == "📅 天气预报":
    st.subheader(f"📅 天气预报 - {city_to_query}")
    forecast = fetch_forecast(city_id)
    if forecast:
        st.markdown("### 🌟 未来3天")
        cols = st.columns(min(3, len(forecast)))
        for i in range(min(3, len(forecast))):
            d = forecast[i]
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"#### {d.get('预报日期','--')}")
                    st.markdown(f"**☀️ 白天：** {d.get('白天天气状况的文字描述','--')}")
                    st.markdown(f"**🌙 夜间：** {d.get('晚上天气状况的文字描述','--')}")
                    st.markdown(f"**🌡️ 温度：** {d.get('预报当天最低温度','--')}~{d.get('预报当天最高温度','--')}°C")
                    st.markdown(f"**🌬️ 风：** {d.get('白天风向','--')} {d.get('白天风力等级','--')}级")
                    st.markdown(f"**💧 湿度：** {d.get('相对湿度','--')}% | **🌧️ 降水：** {d.get('当天总降水量','--')}mm")
        st.markdown("---")
        st.markdown("### 全部数据")
        df = pd.DataFrame(forecast)
        cols_map = {"预报日期":"日期","白天天气状况的文字描述":"天气","预报当天最高温度":"最高温(℃)","预报当天最低温度":"最低温(℃)","白天风向":"风向","白天风力等级":"风力(级)","相对湿度":"湿度(%)","当天总降水量":"降水量(mm)"}
        cols_exist = [c for c in cols_map if c in df.columns]
        df_display = df[cols_exist].rename(columns={c: cols_map[c] for c in cols_exist})
        st.dataframe(df_display, use_container_width=True)
    else:
        st.warning("⚠️ 未获取到天气预报数据")

# 天气预警
elif selected_tab == "⚠️ 天气预警":
    st.subheader(f"⚠️ 天气预警 - {city_to_query}")
    if not city_lat or not city_lon:
        st.info("ℹ️ 无经纬度信息，无法查询预警")
    else:
        warnings = fetch_warnings(city_lat, city_lon)
        if warnings:
            for alert in warnings:
                with st.expander(f"🚨 {alert.get('headline','预警')}", expanded=True):
                    st.markdown(f"**📝 描述：** {alert.get('description','无')}")
                    st.markdown(f"**📊 标准：** {alert.get('criteria','无')}")
                    st.markdown(f"**🛡️ 防御：** {alert.get('instruction','无')}")
            st.caption(f"共 {len(warnings)} 条预警")
        else:
            st.success("当前无天气预警")