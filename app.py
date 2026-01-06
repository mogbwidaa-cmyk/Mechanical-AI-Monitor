import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات الصفحة الفنية ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="⚙️", layout="wide")

# --- 2. إدارة الجلسة والتتبع ---
if 'event_log' not in st.session_state:
    st.session_state.event_log = []

# --- 3. إعدادات التنبيهات والروابط ---
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"
MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"

def notify_visitor_with_location():
    """تتبع موقع الزائر وإرسال تنبيه فوري للهاتف"""
    if 'notified' not in st.session_state:
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5).json()
            city = response.get('city', 'غير معروف')
            region = response.get('regionName', 'غير معروف')
            now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
            msg = f"👤 **زائر جديد للمنصة!**\n📍 الموقع: {city}, {region}\n⏰ الوقت: {now}\n📞 هاتف المطور: {MY_PHONE}"
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"
            requests.get(url)
            st.session_state.notified = True
        except: pass

notify_visitor_with_location()

def send_technical_alert(source, asset, value, status, diagnostic):
    """إرسال تقارير الحالة الفنية"""
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    message = (
        f"🚨 **تقرير حالة فنية - منصة م. مجاهد**\n\n"
        f"📍 المنشأة: {source}\n"
        f"⚙️ المعدة: {asset}\n"
        f"📊 الاهتزاز: {value}\n"
        f"⚠️ التقييم: {status}\n"
        f"🔍 التشخيص: {diagnostic}\n"
        f"📞 هاتف المهندس: {MY_PHONE}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: 
        requests.get(url)
        st.session_state.event_log.insert(0, {"الوقت": now, "المنشأة": source, "المعدة": asset, "التقييم": status, "التشخيص": diagnostic})
    except: pass

# --- 4. القائمة الجانبية (لوحة التحكم والروابط) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.info("خبير صيانة ميكانيكية وأتمتة صناعية")
    
    st.markdown(f"📞 **للتواصل المباشر:**\n`{MY_PHONE}`")
    
    # أزرار التواصل الاجتماعي
    c1, c2 = st.columns(2)
    with c1:
        whatsapp_url = f"https://wa.me/{MY_PHONE.replace('+', '')}"
        st.markdown(f"""<a href="{whatsapp_url}" target="_blank"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" width="100%"></a>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<a href="{LINKEDIN_URL}" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>""", unsafe_allow_html=True)
    
    st.divider()
    
    # التحقق من السيرة الذاتية
    if os.path.exists("cv.pdf"):
        with open("cv.pdf", "rb") as f:
            st.download_button("📄 تحميل السيرة الذاتية (CV)", f, "cv.pdf", mime="application/pdf", use_container_width=True)
    
    st.divider()
    st.header("⚙️ مدخلات النظام الفنية")
    factory = st.selectbox("الوحدة الصناعية:", ["مجمع الصناعات بجدة", "مصفاة ينبع", "مدينة نيوم الصناعية"])
    machine = st.selectbox("المعدة تحت الفحص:", ["مضخة طرد مركزي P-101", "ضاغط هواء C-202", "محرك مروحة تبريد F-305"])
    vib_input = st.slider("قراءة الاهتزاز الكلي (RMS mm/s):", 0.0, 15.0, 3.2)
    rpm_input = st.number_input("سرعة الدوران التشغيلية (RPM):", value=1450)

# --- 5. الواجهة الرئيسية ---
st.markdown(f"""
    <div style="background-color:#001529; padding:25px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0; font-size:28px;">⚙️ منصة مراقبة المصانع والمعدات الميكانيكية</h1>
        <p style="color:#FFD700; font-size:18px; font-weight:bold; margin-top:10px;">نظام هندسي متقدم للصيانة التنبؤية وتحليل الأصول</p>
    </div>
    """, unsafe_allow_html=True)

# معايير التقييم ISO 10816
if vib_input <= 2.8: status, color = "تشغيل آمن (A)", "green"
elif vib_input <= 7.1: status, color = "تحذير - مراقبة (B/C)", "orange"
else: status, color = "حرج - إيقاف فوري (D)", "red"

st.write("")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 مؤشر الحالة اللحظي")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=vib_input,
        gauge={'bar': {'color': color}, 'axis': {'range': [0, 15]},
               'steps': [{'range': [0, 2.8], 'color': "lightgreen"}, {'range': [2.8, 7.1], 'color': "yellow"}, {'range': [7.1, 15], 'color': "salmon"}]}))
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    if st.button("📲 إرسال تقرير الحالة للمشرف"):
        send_technical_alert(factory, machine, f"{vib_input} mm/s", status, "Spectral FFT Analysis Triggered")
        st.success("تم التوثيق وإرسال التنبيه")

with col2:
    st.subheader(f"🔬 تحليل الطيف الترددي FFT Spectrum")
    freq = np.linspace(0, 500, 250)
    base_freq = rpm_input / 60
    amplitude = (np.exp(-((freq - base_freq)**2) / 10) * vib_input) + \
                (np.exp(-((freq - 2*base_freq)**2) / 8) * (vib_input*0.4)) + \
                np.random.normal(0, 0.05, 250)
    
    fig_fft = go.Figure()
    fig_fft.add_trace(go.Scatter(x=freq, y=amplitude, fill='tozeroy', line=dict(color='#FFD700')))
    fig_fft.update_layout(xaxis_title="التردد (Hz)", yaxis_title="السعة (mm/s)", height=300, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_fft, use_container_width=True)
    st.caption(f"القمة الأساسية (1X) عند التردد {base_freq:.2f} هرتز.")

# --- 6. سجل العمليات ---
st.divider()
st.subheader("📝 سجل المراقبة والعمليات الفنية")
if st.session_state.event_log:
    st.dataframe(pd.DataFrame(st.session_state.event_log), use_container_width=True)

st.sidebar.caption(f"تطوير: م. مجاهد بشير | {MY_PHONE}")
