import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests
import datetime

# --- 1. الثوابت والقواعد الراسخة (لا تتغير) ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="🛡️", layout="wide")

MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
PLATFORM_NAME = "منصة مراقبة المصانع والمعدات الميكانيكية"
TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. التصميم البصري المتقدم (Professional CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; text-align: right; }
    .main { background-color: #0b111a; color: #e1e1e1; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .info-card { background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); padding: 25px; border-radius: 15px; color: white; margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .feature-box { background-color: #161b22; padding: 20px; border-radius: 12px; border-right: 5px solid #3b82f6; margin-bottom: 15px; }
    .stButton>button { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); color: white; border: none; border-radius: 8px; font-weight: bold; transition: 0.5s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(59,130,246,0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. القائمة الجانبية (الهوية الثابتة) ---
with st.sidebar:
    st.markdown(f"<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/6840/6840478.png' width='100'><br><h2 style='color:white;'>م. مجاهد بشير</h2></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # قائمة التنقل
    menu = st.radio("القائمة الرئيسية", ["🏠 مركز التحكم", "🛠️ الصيانة التنبؤية (Vibration)", "🌱 هندسة الطاقة (PV System)", "🤖 حلول الأتمتة (AI)"])
    
    st.markdown("---")
    st.markdown(f"📱 **للتواصل المباشر:**")
    st.code(MY_PHONE, language="text")
    
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/{MY_PHONE.replace('+', '')})")
    with c2: st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN_URL})")

# --- 4. محتوى المنصة ---

# --- الصفحة الرئيسية ---
if menu == "🏠 مركز التحكم":
    st.markdown(f"<div class='info-card'><h1>🛡️ {PLATFORM_NAME}</h1><p>تكامل الذكاء الاصطناعي مع الخبرة الهندسية الميدانية لإدارة الأصول وتحولات الطاقة.</p></div>", unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("الموثوقية المستهدفة", "99.8%", "+0.5%")
    col_m2.metric("توفير الطاقة المتوقع", "15%", "AI Optimized")
    col_m3.metric("سرعة الاستجابة", "Real-time", "Active")
    
    st.markdown("### 💠 مجالات التميز الهندسي")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='feature-box'><h4>🔬 البحث والتطوير</h4><p>تطوير حلول مبنية على أبحاث علمية منشورة دولياً (Bio-Gas 2016) لدعم الاقتصاد الدائري.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='feature-box'><h4>⚙️ أتمتة العمليات</h4><p>تحويل البيانات الخام من الحساسات إلى لوحات تحكم ذكية تدعم اتخاذ القرار الاستراتيجي.</p></div>", unsafe_allow_html=True)

# --- صفحة الصيانة ---
elif menu == "🛠️ الصيانة التنبؤية (Vibration)":
    st.subheader("🛠️ نظام تحليل الاهتزازات الرقمي (FFT Diagnostic)")
    
    col_ctrl, col_chart = st.columns([1, 2])
    
    with col_ctrl:
        st.write("🔧 **إعدادات المحاذاة**")
        vibration = st.slider("مستوى الاهتزاز (mm/s RMS):", 0.0,
