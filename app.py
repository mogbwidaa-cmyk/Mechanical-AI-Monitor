import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="منصة م. مجاهد المتكاملة", page_icon="⚙️", layout="wide")

# --- 2. إدارة السجل (Session State) ---
if 'event_log' not in st.session_state:
    st.session_state.event_log = []

# --- 3. إعدادات الربط والتنبيهات ---
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

def send_intelligent_alert(factory_name, machine_name, vibration, status, fault_type):
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    message = (
        f"🏢 **منشأة: {factory_name}**\n"
        f"🚨 **نظام المهندس مجاهد الذكي**\n\n"
        f"📅 الوقت: {now}\n"
        f"⚙️ المعدة: {machine_name}\n"
        f"📊 الاهتزاز: {vibration} mm/s\n"
        f"⚠️ الحالة: {status}\n"
        f"🔍 التشخيص: {fault_type}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: 
        requests.get(url)
        st.session_state.event_log.insert(0, {"الوقت": now, "المنشأة": factory_name, "المعدة": machine_name, "الحالة": status, "التشخيص": fault_type})
    except: pass

# --- 4. فحص ملف السيرة الذاتية ---
current_dir = os.getcwd()
pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
cv_exists = len(pdf_files) > 0

# --- 5. القائمة الجانبية (كل الميزات المحذوفة عادت هنا) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("👤 الملف المهني")
    st.markdown("### **المهندس مجاهد بشير**")
    st.info("📍 المدينة المنورة، السعودية")
    st.success("✅ **متاح للتوظيف فوراً**")
    st.write("📞 `+966501318054` ")
    
    # روابط التواصل والسيرة الذاتية
    linkedin_url = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
    st.markdown(f"""<a href="{linkedin_url}" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin" width="100%"></a>""", unsafe_allow_html=True)
    
    if cv_exists:
        with open(pdf_files[0], "rb") as f:
            st.download_button(label="📄 تحميل السيرة الذاتية (CV)", data=f, file_name=pdf_files[0], mime="application/pdf", use_container_width=True)
    
    st.divider()
    st.header("🤖 روبوت التوظيف الذكي")
    target_city = st.multiselect("مدن الاستهداف:", ["المدينة", "جدة", "نيوم", "ينبع"], default=["المدينة", "جدة"])
    if st.button("إطلاق حملة التقديم الآلي"):
        st.write("🚀 الروبوت يبحث عن فرص في القطاع الصناعي...")
        send_intelligent_alert("نظام التوظيف", "روبوت البحث", 0, "نشط", f"بدء البحث في {target_city}")

    st.divider()
    st.header("🏢 إدارة المنشآت")
    selected_factory = st.selectbox("اختر المنشأة:", ["Madinah Factory", "Jeddah Plant", "Yanbu Industrial"])
    machine_selected = st.selectbox("اختر المعدة:", ["Pump P-01", "Fan F-05", "Compressor C-10"])
    vibration_val = st.slider("الاهتزاز (mm/s)", 0.0, 15.0, 3.2)
    temp_val = st.number_input("الحرارة (°C)", value=55)

# --- 6. الواجهة الترويجية الرئيسية ---
st.markdown("""
    <div style="background-color:#001529; padding:30px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0;">🛡️ منصة م. مجاهد للتحول الرقمي الصناعي</h1>
        <p style="color:#FFD700; font-size:20px; font-weight:bold; margin-top:10px;">نحو صيانة ذكية.. صفر توقف مفاجئ!</p>
        <p style="color:#d9d9d9; font-size:16px;">
            نظام متطور لكشف الأعطال قبل وقوعها وتقليل نفقات الصيانة الطارئة بنسبة 30% عبر تقنيات الصيانة التنبؤية.
        </p>
    </div>
    """, unsafe_allow_html=True)

# تحليل البيانات
if vibration_val <= 2.8: status, color = "Good (Safe)", "green"
elif vibration_val <= 7.1: status, color = "Warning", "orange"
else: status, color = "Critical", "red"

days_left = max(1, int(150 / (vibration_val + 0.1)))
fail_date = datetime.date.today() + datetime.timedelta(days=days_left)

st.header(f"📊 حالة التشغيل: {selected_factory}")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=vibration_val, gauge={'bar': {'color': color}, 'axis': {'range': [0, 15]}}))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🤖 وحدة التنبؤ والتحليل")
    st.metric("تاريخ الصيانة المتوقع", f"{fail_date}")
    st.write(f"الأيام المتبقية: **{days_left} يوم**")
    if st.button("📲 إرسال تنبيه وتوثيق العملية"):
        send_intelligent_alert(selected_factory, machine_selected, vibration_val, status, "Misalignment/Bearing")
        st.success("تم التنبيه والتوثيق")

with c3:
    st.markdown("### 📥 إدارة التقارير")
    report_text = f"Report for {machine_selected}\nStatus: {status}\nVibration: {vibration_val}\nDate: {datetime.date.today()}"
    st.download_button(label="📥 تحميل التقرير الفني", data=report_text, file_name=f"Report_{machine_selected}.txt", use_container_width=True)

# سجل الأحداث
st.divider()
st.subheader("📝 سجل أحداث الصيانة والتوظيف الأخير")
if st.session_state.event_log:
    st.table(pd.DataFrame(st.session_state.event_
