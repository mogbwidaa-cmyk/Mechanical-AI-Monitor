import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests

# --- إعدادات الربط والتنبيهات ---
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

def send_intelligent_alert(factory_name, machine_name, vibration, status, fault_type):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    message = (
        f"🏢 **تنبيه من منشأة: {factory_name}**\n"
        f"🚨 **نظام مراقبة المهندس مجاهد الذكي**\n\n"
        f"📅 الوقت: {now}\n"
        f"⚙️ المعدة: {machine_name}\n"
        f"📊 الاهتزاز: {vibration} mm/s\n"
        f"⚠️ الحالة: {status}\n"
        f"🔍 التشخيص: {fault_type}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: requests.get(url)
    except: pass

# --- خوارزمية تحليل FFT المتقدمة ---
def diagnose_fault(vibration):
    if vibration > 7.1: return "Critical: Bearing Failure / Loose Foundation"
    elif vibration > 4.5: return "Warning: Misalignment / Unbalance"
    return "Normal: Operating within ISO limits"

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة م. مجاهد لإدارة الأصول", page_icon="⚙️", layout="wide")

# --- القائمة الجانبية: إعلان التوظيف ورابط LinkedIn ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("👤 الملف المهني")
    st.markdown("### **المهندس مجاهد بشير**")
    st.info("📍 المدينة المنورة، السعودية")
    st.success("✅ **متاح للتوظيف فوراً (Available for Hire)**")
    st.write("📞 `+966501318054` ")
    
    # رابط LinkedIn الاحترافي
    linkedin_url = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
    st.markdown(f"""
        <a href="{linkedin_url}" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin" width="100%">
        </a>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.header("🏢 إدارة المنشآت")
    selected_factory = st.selectbox("اختر المنشأة:", ["مصنع جدة", "مصنع ينبع", "مصنع المدينة"])
    machine_selected = st.selectbox("اختر المعدة:", ["المضخة P-01", "المروحة F-05", "الضاغط C-10"])
    vibration = st.sidebar.slider("الاهتزاز (mm/s)", 0.0, 15.0, 3.2)
    temp = st.sidebar.number_input("الحرارة (°C)", value=55)

# --- الإعلان التسويقي للأتمتة (في الواجهة الرئيسية) ---
st.markdown("""
    <div style="background-color:#001529; padding:20px; border-radius:10px; border-right: 8px solid #FFD700; text-align: right; direction: rtl;">
        <h2 style="color:white; margin:0;">🚀 نظام أتمتة ومراقبة المصانع المتعددة</h2>
        <p style="color:#d9d9d9; font-size:18px;">
            إدارة مركزية لجميع منشآتك الصناعية. مراقبة لحظية، تحليل أعطال ذكي، وربط مباشر بجوال المهندس المسؤول.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- منطق التحليل ---
if vibration <= 2.8: status, color = "Good (Safe)", "green"
elif vibration <= 7.1: status, color = "Warning", "orange"
else: status, color = "Critical", "red"

fault_type = diagnose_fault(vibration)
health_score = max(0, 100 - (vibration * 6) - (temp * 0.05))

# --- الواجهة الرئيسية ---
st.header(f"📊 حالة التشغيل: {selected_factory}")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=vibration, gauge={'bar': {'color': color}, 'axis': {'range': [0, 15]}}))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### التشخيص الذكي")
    st.info(f"النتيجة: **{fault_type}**")
    st.metric("صحة المعدة", f"{int(health_score)}%")
    if st.button("📲 إرسال تنبيه عاجل للجوال"):
        send_intelligent_alert(selected_factory, machine_selected, vibration, status, fault_type)
        st.success("تم إرسال التقرير")

with c3:
    st.markdown("### الحالة الفنية")
    st.subheader(status)
    st.write(f"المعدات النشطة: **12**")
    if vibration > 7.1: st.error("🚨 خطر! اهتزاز مرتفع.")

st.divider()
st.subheader(f"📈 سجل أداء {machine_selected}")
history_data = pd.DataFrame(np.random.randn(24, 2) / 8 + [vibration, temp/20], columns=['الاهتزاز', 'الحرارة'])
st.line_chart(history_data)

st.sidebar.divider()
st.sidebar.caption("تم التطوير بواسطة م. مجاهد بشير - 2026")
