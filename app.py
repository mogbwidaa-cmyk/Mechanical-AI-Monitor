import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="منصة م. مجاهد الصناعية المتكاملة",
    page_icon="⚙️",
    layout="wide"
)

# --- 2. إدارة سجل العمليات (Session State) ---
if 'event_log' not in st.session_state:
    st.session_state.event_log = []

# --- 3. إعدادات الربط مع تليجرام ---
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

def send_intelligent_alert(source, asset, value, status, diagnostic):
    """دالة إرسال التنبيهات وتوثيقها في السجل"""
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    message = (
        f"🚨 **تنبيه من نظام المهندس مجاهد**\n\n"
        f"📍 المصدر: {source}\n"
        f"⚙️ المعدة/الهدف: {asset}\n"
        f"📊 القيمة: {value}\n"
        f"⚠️ الحالة: {status}\n"
        f"🔍 التشخيص: {diagnostic}\n"
        f"⏰ الوقت: {now}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: 
        requests.get(url)
        # توثيق العملية في سجل الأحداث داخل التطبيق
        st.session_state.event_log.insert(0, {
            "الوقت": now,
            "المصدر": source,
            "المعدة/الهدف": asset,
            "الحالة": status,
            "التشخيص": diagnostic
        })
    except:
        pass

# --- 4. فحص ملف السيرة الذاتية ---
current_dir = os.getcwd()
pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
cv_exists = len(pdf_files) > 0

# --- 5. القائمة الجانبية (الشخصية والتحكم) ---
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
            st.download_button(
                label="📄 تحميل السيرة الذاتية (CV)",
                data=f,
                file_name=pdf_files[0],
                mime="application/pdf",
                use_container_width=True
            )
    
    st.divider()
    
    # قسم روبوت التوظيف
    st.header("🤖 روبوت التوظيف الذكي")
    target_city = st.multiselect("مدن استهداف الوظائف:", ["المدينة", "جدة", "نيوم", "ينبع", "الرياض"], default=["المدينة", "جدة"])
    if st.button("🚀 إطلاق حملة التقديم الآلي"):
        send_intelligent_alert("روبوت التوظيف", f"بحث في {target_city}", "Active", "جاري البحث", "استهداف وظائف الطاقة والصيانة")
        st.write("✅ بدأ الروبوت بمسح الفرص المتاحة...")

    st.divider()
    
    # قسم التحكم في المصانع
    st.header("🏢 إدارة المنشآت التجارية")
    selected_factory = st.selectbox("اختر المنشأة:", ["Madinah Plant", "Jeddah Industrial", "Yanbu Petrochemical"])
    machine_selected = st.selectbox("المعدة تحت المراقبة:", ["Pump P-01", "Fan F-05", "Compressor C-10"])
    vibration_val = st.slider("قراءة الاهتزاز (mm/s)", 0.0, 15.0, 3.2)
    temp_val = st.number_input("درجة حرارة المحامل (°C)", value=55)

# --- 6. الواجهة الترويجية الرئيسية ---
st.markdown("""
    <div style="background-color:#001529; padding:30px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0;">🛡️ منصة م. مجاهد للتحول الرقمي الصناعي</h1>
        <p style="color:#FFD700; font-size:20px; font-weight:bold; margin-top:10px;">نحو صيانة ذكية.. صفر توقف مفاجئ!</p>
        <p style="color:#d9d9d9; font-size:16px;">
            نظام متطور لكشف الأعطال قبل وقوعها وتقليل نفقات الصيانة الطارئة بنسبة 30% عبر تقنيات الصيانة التنبؤية المعتمدة على الذكاء الاصطناعي.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 7. معالجة البيانات والتحليل ---
if vibration_val <= 2.8:
    status, color = "Good (Safe Zone)", "green"
    diagnostic = "Operating within ISO 10816 limits"
elif vibration_val <= 7.1:
    status, color = "Warning (Check Needed)", "orange"
    diagnostic = "Potential Unbalance or Misalignment"
else:
    status, color = "Critical (Immediate Action)", "red"
    diagnostic = "Severe Bearing Damage or Looseness"

days_left = max(1, int(150 / (vibration_val + 0.1)))
fail_date = datetime.date.today() + datetime.timedelta(days=days_left)

st.header(f"📊 مراقبة الأصول: {selected_factory}")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### مؤشر الاهتزاز")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vibration_val,
        gauge = {'axis
