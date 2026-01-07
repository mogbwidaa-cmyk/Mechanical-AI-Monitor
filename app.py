import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات المنصة والثوابت (قواعد ثابتة) ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="🏗️", layout="wide")

MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
PLATFORM_NAME = "منصة مراقبة المصانع والمعدات الميكانيكية"
RESEARCH_TITLE = "Bio Gas Production from Municipal Solid Waste"
RESEARCH_URL = "https://ijsrset.com/paper/1468.pdf"
TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. إدارة التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

def set_page(page_name):
    st.session_state.page = page_name

# --- 3. القائمة الجانبية (الثوابت: الرقم، واتساب، لينكد إن) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.write("🎓 باحث دراسات عليا - طاقة متجددة")
    st.divider()
    
    # الثوابت المتفق عليها
    st.markdown(f"📞 التواصل: `{MY_PHONE}`")
    
    col_links = st.columns(2)
    with col_links[0]:
        st.markdown(f'''<a href="https://wa.me/{MY_PHONE.replace('+', '')}"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    with col_links[1]:
        st.markdown(f'''<a href="{LINKEDIN_URL}"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    
    st.divider()
    if st.button("🏠 العودة للرئيسية", use_container_width=True):
        set_page('Home')

# --- 4. الواجهة الرئيسية بالاسم الثابت ---
if st.session_state.page == 'Home':
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 15px; border-bottom: 5px solid #1E3A8A;">
            <h1 style="color: #1E3A8A; margin: 0;">🛡️ {PLATFORM_NAME}</h1>
            <p style="font-size: 18px; color: #555; margin-top: 10px;">نظام هندسي متكامل للصيانة التنبؤية، الطاقة المتجددة، والذكاء الاصطناعي</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🛠️ قسم الصيانة\nمراقبة الاهتزاز وتحليل الأصول.")
        if st.button("دخول قسم الصيانة", use_container_width=True): set_page('Maintenance')
            
    with col2:
        st.success("### 🌱 الطاقة المتجددة\nالبحث العلمي واستدامة الطاقة.")
        if st.button("دخول قسم الطاقة", use_container_width=True): set_page('Renewable')
            
    with col3:
        st.warning("### 🤖 الذكاء الاصطناعي\nروبوت التوظيف والتقديم الذكي.")
        if st.button("دخول مشروع الـ AI", use_container_width=True): set_page('AI_Bot')

# --- الأقسام الفرعية (تتبع نفس منطق الكود السابق) ---
elif st.session_state.page == 'Maintenance':
    st.header("🛠️ مراقبة الأصول الميكانيكية")
    # (كود الصيانة يوضع هنا...)
    st.button("إرسال تقرير صيانة")

elif st.session_state.page == 'Renewable':
    st.header("🌱 قسم الطاقة المتجددة")
    # (كود الطاقة يوضع هنا...)

elif st.session_state.page == 'AI_Bot':
    st.header("🤖 مشروع الذكاء الاصطناعي")
    # (كود الروبوت يوضع هنا...)

st.sidebar.caption(f"{PLATFORM_NAME} | 2026")
