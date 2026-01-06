import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="منصة م. مجاهد - تحليل FFT المتقدم", page_icon="⚙️", layout="wide")

# --- 2. إدارة السجل وتتبع الزوار ---
if 'event_log' not in st.session_state:
    st.session_state.event_log = []

# --- 3. إعدادات التنبيهات ---
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

def notify_visitor_with_location():
    if 'notified' not in st.session_state:
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5).json()
            city = response.get('city', 'غير معروف')
            region = response.get('regionName', 'غير معروف')
            now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
            msg = f"👤 **زائر جديد للمنصة!**\n📍 الموقع: {city}, {region}\n⏰ الوقت: {now}"
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"
            requests.get(url)
            st.session_state.notified = True
        except: pass

notify_visitor_with_location()

def send_intelligent_alert(source, asset, value, status, diagnostic):
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    message = f"🚨 **تنبيه فني**\n📍 المصدر: {source}\n⚙️ المعدة: {asset}\n📊 القيمة: {value}\n⚠️ الحالة: {status}\n🔍 التشخيص: {diagnostic}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: 
        requests.get(url)
        st.session_state.event_log.insert(0, {"الوقت": now, "المصدر": source, "المعدة": asset, "الحالة": status, "التشخيص": diagnostic})
    except: pass

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.title("👤 المهندس مجاهد بشير")
    st.success("✅ متاح للتوظيف فوراً")
    # التأكد من وجود ملف CV
    if os.path.exists("cv.pdf"):
        with open("cv.pdf", "rb") as f:
            st.download_button("📄 تحميل السيرة الذاتية (CV)", f, "cv.pdf", mime="application/pdf", use_container_width=True)
    
    st.divider()
    st.header("🏢 تحكم المنشأة")
    selected_factory = st.selectbox("المصنع:", ["Madinah Plant", "Jeddah Industrial"])
    machine_selected = st.selectbox("المعدة:", ["Pump P-01", "Motor M-02", "Compressor C-10"])
    vibration_val = st.slider("مستوى الاهتزاز (mm/s)", 0.0, 15.0, 3.2)
    rpm_val = st.number_input("سرعة الدوران (RPM)", value=1450)

# --- 5. الواجهة الترويجية ---
st.markdown("""
    <div style="background-color:#001529; padding:25px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0;">🔬 نظام تحليل FFT والتشخيص الترددي</h1>
        <p style="color:#FFD700; font-size:18px;">تحليل الاهتزاز الميكانيكي المتقدم لاكتشاف جذور الأعطال (Root Cause Analysis).</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. منطق التشخيص ---
if vibration_val <= 2.8: status, color = "Good", "green"
elif vibration_val <= 7.1: status, color = "Warning", "orange"
else: status, color = "Critical", "red"

# --- 7. قسم العرض الرئيسي ---
col1, col2 = st.columns([1, 2])
with col1:
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=vibration_val, gauge={'bar': {'color': color}, 'axis': {'range': [0, 15]}}))
    st.plotly_chart(fig_gauge, use_container_width=True)
    if st.button("📲 إرسال تقرير التشخيص"):
        send_intelligent_alert(selected_factory, machine_selected, f"{vibration_val} mm/s", status, "FFT Analysis Completed")
        st.success("تم الإرسال")

with col2:
    st.subheader(f"🔍 تحليل الطيف الترددي (FFT Spectrum) - {machine_selected}")
    
    # محاكاة بيانات FFT حقيقية
    freq = np.linspace(0, 500, 200) # التردد من 0 إلى 500 هرتز
    base_rpm_freq = rpm_val / 60
    
    # إنشاء قمم ترددية (Peaks) بناءً على مستوى الاهتزاز
    amplitude = (np.exp(-((freq - base_rpm_freq)**2) / 10) * vibration_val) + \
                (np.exp(-((freq - 2*base_rpm_freq)**2) / 10) * (vibration_val/3)) + \
                np.random.normal(0, 0.1, 200) # إضافة ضوضاء
    
    fig_fft = go.Figure()
    fig_fft.add_trace(go.Scatter(x=freq, y=amplitude, mode='lines', line=dict(color='#FFD700', width=2), fill='tozeroy'))
    fig_fft.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Amplitude (mm/s)", height=300, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_fft, use_container_width=True)
    
    st.info(f"💡 الذروة الأساسية (1X) عند {base_rpm_freq:.1f} Hz تتناسب مع سرعة الدوران.")

# --- 8. سجل الأحداث ---
st.divider()
st.subheader("📝 سجل عمليات النظام")
if st.session_state.event_log:
    st.table(pd.DataFrame(st.session_state.event_log))

st.sidebar.caption("تم التطوير بواسطة م. مجاهد بشير - 2026")
