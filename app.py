import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات المنصة ---
st.set_page_config(page_title="منصة م. مجاهد المتكاملة", page_icon="🏗️", layout="wide")

# الثوابت
MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
RESEARCH_TITLE = "Bio Gas Production from Municipal Solid Waste"
RESEARCH_URL = "https://ijsrset.com/paper/1468.pdf"
TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. إدارة الحالة (Navigation) ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

def set_page(page_name):
    st.session_state.page = page_name

# --- 3. الهوية البصرية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.write("🎓 باحث دراسات عليا - طاقة متجددة")
    st.divider()
    if st.button("🏠 العودة للرئيسية", use_container_width=True):
        set_page('Home')
    
    st.markdown(f"📞 `{MY_PHONE}`")
    st.markdown(f"[LinkedIn]({LINKEDIN_URL})")

# --- 4. الواجهة الرئيسية (الأزرار الثلاثة) ---
if st.session_state.page == 'Home':
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #1E3A8A;">🛡️ نظام الإدارة الهندسية المتكامل</h1>
            <p style="font-size: 18px; color: #555;">اختر المسار الهندسي المطلوب للبدء في التحليل</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🛠️ قسم الصيانة")
        st.write("مراقبة اهتزاز الأصول الميكانيكية وتحليل FFT.")
        if st.button("دخول قسم الصيانة", use_container_width=True):
            set_page('Maintenance')
            
    with col2:
        st.markdown("### 🌱 الطاقة المتجددة")
        st.write("البحث العلمي (Bio-Gas) ومشاريع استدامة الطاقة.")
        if st.button("دخول قسم الطاقة", use_container_width=True):
            set_page('Renewable')
            
    with col3:
        st.markdown("### 🤖 الذكاء الاصطناعي")
        st.write("روبوت التوظيف والتقديم التلقائي الذكي.")
        if st.button("دخول مشروع الـ AI", use_container_width=True):
            set_page('AI_Bot')

# --- 5. محتوى الصفحات ---

# 5.1 صفحة الصيانة
elif st.session_state.page == 'Maintenance':
    st.header("🛠️ مراقبة الأصول الميكانيكية (ISO 10816)")
    vib = st.slider("مستوى الاهتزاز (mm/s):", 0.0, 15.0, 3.5)
    
    # الرسم البياني للاهتزاز
    fig = go.Figure(go.Indicator(mode="gauge+number", value=vib, gauge={'bar': {'color': "blue"}, 'axis': {'range': [0, 15]}}))
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("📤 إرسال تقرير الصيانة"):
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚨 تنبيه صيانة: الاهتزاز {vib} mm/s")
        st.success("تم إرسال التنبيه!")

# 5.2 صفحة الطاقة المتجددة
elif st.session_state.page == 'Renewable':
    st.header("🌱 الطاقة المتجددة والبحث العلمي")
    st.info(f"📜 البحث المنشور: {RESEARCH_TITLE} (2016)")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.write("هذا القسم مخصص لمحاكاة إنتاج الطاقة الحيوية بناءً على ورقتك البحثية.")
        waste = st.number_input("كمية النفايات (طن):", 1, 100, 10)
        st.metric("إنتاج الغاز المتوقع", f"{waste * 0.45:.2f} m³")
    with col_r2:
        st.markdown(f'''<a href="{RESEARCH_URL}" target="_blank"><button style="width:100%; height:50px; background-color:#1B5E20; color:white; border:none; border-radius:5px; cursor:pointer;">📄 فتح الورقة البحثية</button></a>''', unsafe_allow_html=True)

# 5.3 صفحة الذكاء الاصطناعي
elif st.session_state.page == 'AI_Bot':
    st.header("🤖 مشروع الذكاء الاصطناعي (روبوت التوظيف)")
    st.write("الروبوت يقوم بمطابقة مهاراتك مع وظائف لينكد إن تلقائياً.")
    
    mode = st.radio("اختر وضع الروبوت:", ["التقديم التلقائي", "تحليل فرص السوق"])
    if st.button("تفعيل الروبوت الآن ⚡"):
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🤖 تم تفعيل الروبوت في وضع {mode}")
        st.balloons()
        st.success("الروبوت يعمل الآن في الخلفية!")
    
    # رسم بياني بسيط للمطابقة
    match_data = pd.DataFrame({'Job': ['Aramco', 'SIRC', 'NEOM'], 'Match %': [92, 99, 88]})
    st.bar_chart(match_data.set_index('Job'))

# التذييل
st.sidebar.caption("تم التطوير بواسطة م. مجاهد بشير | 2026")
