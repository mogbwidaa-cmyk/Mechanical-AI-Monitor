import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="منصة م. مجاهد لمراقبة المعدات", page_icon="⚙️", layout="wide")

# --- 2. إدارة السجل وتتبع الزوار (Session State) ---
if 'event_log' not in st.session_state:
    st.session_state.event_log = []

# --- 3. إعدادات الربط والتنبيهات ---
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

def notify_visitor_with_location():
    """دالة تتبع موقع الزائر وإرسال تنبيه للجوال"""
    if 'notified' not in st.session_state:
        try:
            # جلب بيانات الموقع عبر الـ IP
            response = requests.get('http://ip-api.com/json/', timeout=5).json()
            city = response.get('city', 'غير معروف')
            region = response.get('regionName', 'غير معروف')
            country = response.get('country', 'غير معروف')
            
            now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
            msg = (
                f"👤 **زائر جديد للمنصة!**\n"
                f"📍 الموقع: {city}, {region} - {country}\n"
                f"⏰ الوقت: {now}\n"
                f"📱 ملاحظة: يتم التصفح الآن."
            )
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"
            requests.get(url)
            st.session_state.notified = True
        except:
            pass

# استدعاء التنبيه فور فتح الموقع
notify_visitor_with_location()

def send_intelligent_alert(source, asset, value, status, diagnostic):
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    message = (
        f"🚨 **تنبيه فني - المهندس مجاهد**\n\n"
        f"📍 المصدر: {source}\n"
        f"⚙️ المعدة: {asset}\n"
        f"📊 القيمة: {value}\n"
        f"⚠️ الحالة: {status}\n"
        f"🔍 التشخيص: {diagnostic}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: 
        requests.get(url)
        st.session_state.event_log.insert(0, {"الوقت": now, "المصدر": source, "المعدة": asset, "الحالة": status, "التشخيص": diagnostic})
    except: pass

# --- 4. فحص ملف السيرة الذاتية ---
current_dir = os.getcwd()
pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
cv_exists = len(pdf_files) > 0

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("👤 الملف المهني")
    st.markdown("### **المهندس مجاهد بشير**")
    st.info("📍 المدينة المنورة، السعودية")
    st.success("✅ **متاح للتوظيف فوراً**")
    st.write("📞 `+966501318054` ")
    
    linkedin_url = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
    st.markdown(f"""<a href="{linkedin_url}" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin" width="100%"></a>""", unsafe_allow_html=True)
    
    if cv_exists:
        with open(pdf_files[0], "rb") as f:
            st.download_button(label="📄 تحميل السيرة الذاتية (CV)", data=f, file_name=pdf_files[0], mime="application/pdf", use_container_width=True)
    
    st.divider()
    st.header("🤖 روبوت التوظيف")
    target_city = st.multiselect("مدن الاستهداف:", ["المدينة", "جدة", "نيوم", "ينبع"], default=["المدينة", "جدة"])
    if st.button("🚀 إطلاق حملة التقديم"):
        send_intelligent_alert("روبوت التوظيف", f"بحث في {target_city}", "نشط", "جاري البحث", "استهداف وظائف هندسية")

    st.divider()
    st.header("🏢 إدارة المنشآت")
    selected_factory = st.selectbox("اختر المنشأة:", ["Madinah Plant", "Jeddah Industrial", "Yanbu Plant"])
    machine_selected = st.selectbox("المعدة:", ["Pump P-01", "Fan F-05", "Compressor C-10"])
    vibration_val = st.slider("الاهتزاز (mm/s)", 0.0, 15.0, 3.2)
    temp_val = st.number_input("الحرارة (°C)", value=55)

# --- 6. الواجهة الترويجية الرئيسية ---
st.markdown("""
    <div style="background-color:#001529; padding:30px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0;">🛡️ منصة م. مجاهد للتحول الرقمي الصناعي</h1>
        <p style="color:#FFD700; font-size:20px; font-weight:bold; margin-top:10px;">نحو صيانة ذكية.. صفر توقف مفاجئ!</p>
        <p style="color:#d9d9d9; font-size:16px;">تقنيات الصيانة التنبؤية لخفض التكاليف بنسبة 30% وضمان استمرارية الإنتاج.</p>
    </div>
    """, unsafe_allow_html=True)

# معالجة البيانات
if vibration_val <= 2.8: status, color = "Good", "green"
elif vibration_val <= 7.1: status, color = "Warning", "orange"
else: status, color = "Critical", "red"

days_left = max(1, int(150 / (vibration_val + 0.1)))
fail_date = datetime.date.today() + datetime.timedelta(days=days_left)

st.header(f"📊 حالة التشغيل: {
