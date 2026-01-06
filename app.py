import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="⚙️", layout="wide")

# --- 2. بيانات التواصل الأساسية ---
MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 3. القائمة الجانبية (هوية المهندس وأدوات التواصل) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.info("خبير صيانة ميكانيكية وأتمتة صناعية")
    
    # عرض رقم الجوال بوضوح
    st.markdown(f"📞 **للتواصل المباشر:**\n`{MY_PHONE}`")
    
    # أزرار التواصل الاجتماعي (واتساب ولينكد إن) بجانب بعضهما
    col_ws, col_li = st.columns(2)
    with col_ws:
        whatsapp_api = f"https://wa.me/{MY_PHONE.replace('+', '')}"
        st.markdown(f"""<a href="{whatsapp_api}" target="_blank"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" width="100%"></a>""", unsafe_allow_html=True)
    with col_li:
        st.markdown(f"""<a href="{LINKEDIN_URL}" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>""", unsafe_allow_html=True)
    
    st.divider()
    
    # زر تحميل السيرة الذاتية (CV)
    if os.path.exists("cv.pdf"):
        with open("cv.pdf", "rb") as f:
            st.download_button("📄 تحميل السيرة الذاتية (CV)", f, "cv.pdf", mime="application/pdf", use_container_width=True)
    
    st.divider()
    st.header("⚙️ مدخلات النظام")
    factory = st.selectbox("الوحدة الصناعية:", ["مجمع الصناعات بجدة", "مصفاة ينبع", "مدينة نيوم الصناعية"])
    machine = st.selectbox("المعدة:", ["مضخة P-101", "ضاغط C-202", "محرك F-305"])
    vib_input = st.slider("الاهتزاز (mm/s RMS):", 0.0, 15.0, 3.2)
    rpm_input = st.number_input("سرعة الدوران (RPM):", value=1450)

# --- 4. الواجهة الرئيسية وتحليل البيانات ---
st.markdown(f"""
    <div style="background-color:#001529; padding:25px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0; font-size:26px;">⚙️ منصة مراقبة المصانع والمعدات الميكانيكية</h1>
        <p style="color:#FFD700; font-size:18px; font-weight:bold; margin-top:10px;">تحليل متقدم للأصول الميكانيكية والصيانة التنبؤية</p>
    </div>
    """, unsafe_allow_html=True)

# معايير التقييم وتوليد التقرير
if vib_input <= 2.8: status, color = "آمن", "green"
elif vib_input <= 7.1: status, color = "تحذير", "orange"
else: status, color = "حرج", "red"

st.write("")
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("📊 مؤشر الحالة")
    fig_g = go.Figure(go.Indicator(mode="gauge+number", value=vib_input, gauge={'bar': {'color': color}, 'axis': {'range': [0, 15]}}))
    st.plotly_chart(fig_g, use_container_width=True)
    
    if st.button("📤 إرسال التقرير للمهندس مجاهد"):
        msg = f"🚨 تنبيه فني جديد\nالمعدة: {machine}\nالحالة: {status}\nالاهتزاز: {vib_input}\n📞 للتواصل: {MY_PHONE}"
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
        st.success("تم الإرسال والتوثيق بنجاح")

with c2:
    st.subheader("🔬 تحليل الطيف الترددي FFT")
    freq = np.linspace(0, 500, 200)
    base_f = rpm_input / 60
    amp = (np.exp(-((freq - base_f)**2) / 10) * vib_input) + np.random.normal(0, 0.05, 200)
    fig_f = go.Figure(go.Scatter(x=freq, y=amp, fill='tozeroy', line=dict(color='#FFD700')))
    st.plotly_chart(fig_f, use_container_width=True)

st.sidebar.caption(f"تم التطوير بواسطة م. مجاهد بشير | {MY_PHONE}")
