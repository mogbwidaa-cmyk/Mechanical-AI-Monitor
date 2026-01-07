import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests

# --- 1. إعدادات المنصة والثوابت (قواعد ثابتة لا تتغير) ---
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

# --- 3. القائمة الجانبية (الثوابت المتفق عليها) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.write("🎓 باحث دراسات عليا - طاقة متجددة")
    st.divider()
    
    st.markdown(f"📞 التواصل: `{MY_PHONE}`")
    col_links = st.columns(2)
    with col_links[0]:
        st.markdown(f'''<a href="https://wa.me/{MY_PHONE.replace('+', '')}"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    with col_links[1]:
        st.markdown(f'''<a href="{LINKEDIN_URL}"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    
    st.divider()
    if st.button("🏠 العودة للرئيسية", use_container_width=True):
        set_page('Home')

# --- 4. الواجهة الرئيسية ---
if st.session_state.page == 'Home':
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 15px; border-bottom: 5px solid #1E3A8A;">
            <h1 style="color: #1E3A8A; margin: 0;">🛡️ {PLATFORM_NAME}</h1>
            <p style="font-size: 18px; color: #555; margin-top: 10px;">نظام هندسي متكامل بإدارة المهندس مجاهد بشير</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🛠️ قسم الصيانة\nتحليل الاهتزاز الرقمي و FFT.")
        if st.button("دخول قسم الصيانة", use_container_width=True): set_page('Maintenance')
    with col2:
        st.success("### 🌱 الطاقة المتجددة\nمراقبة كفاءة الخلايا الضوئية.")
        if st.button("دخول قسم الطاقة", use_container_width=True): set_page('Renewable')
    with col3:
        st.warning("### 🤖 الذكاء الاصطناعي\nأتمتة الأعمال والترويج الذكي.")
        if st.button("دخول مشروع الـ AI", use_container_width=True): set_page('AI_Bot')

# --- 5. محتوى الأقسام (التطوير الجديد) ---

# 5.1 صفحة الصيانة (نظام الاهتزاز الرقمي و FFT)
elif st.session_state.page == 'Maintenance':
    st.header("🛠️ النظام الرقمي لتحليل الاهتزازات")
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        vib_level = st.slider("مستوى الاهتزاز (mm/s):", 0.0, 20.0, 4.2)
        freq_input = st.number_input("تردد التشغيل (Hz):", 10, 1000, 50)
        st.metric("حالة المعدة", "تحذير" if vib_level > 7.1 else "آمن")
    with col_m2:
        st.subheader("تحليل FFT (Fast Fourier Transform)")
        x = np.linspace(0, 500, 500)
        # محاكاة طيف ترددي حقيقي
        y = (np.exp(-((x - freq_input)**2)/50) * vib_level) + (np.exp(-((x - 2*freq_input)**2)/100) * (vib_level/2)) + np.random.normal(0, 0.1, 500)
        fig_fft = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy', line=dict(color='#1E3A8A')))
        fig_fft.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Amplitude", height=300)
        st.plotly_chart(fig_fft, use_container_width=True)

# 5.2 صفحة الطاقة المتجددة (مراقبة الخلايا الضوئية مع المعايرة)
elif st.session_state.page == 'Renewable':
    st.header("🌱 مراقبة كفاءة الخلايا الضوئية (PV Efficiency)")
    c1, c2, c3 = st.columns(3)
    temp = c1.slider("درجة الحرارة (C°):", 10, 60, 35)
    wind = c2.slider("سرعة الرياح (m/s):", 0, 20, 5)
    dust = c3.slider("نسبة الغبار (%):", 0, 100, 10)
    
    # معادلة معايرة الكفاءة (محاكاة هندسية)
    base_eff = 20.0
    loss_temp = (temp - 25) * 0.05 if temp > 25 else 0
    loss_dust = dust * 0.15
    gain_wind = wind * 0.02 # الرياح تساعد في التبريد
    current_eff = max(0, base_eff - loss_temp - loss_dust + gain_wind)
    
    st.divider()
    st.subheader(f"الكفاءة الفعلية الحالية: {current_eff:.2f}%")
    fig_eff = go.Figure(go.Indicator(mode="gauge+number", value=current_eff, gauge={'axis': {'range': [0, 25]}, 'bar': {'color': "green"}}))
    st.plotly_chart(fig_eff, use_container_width=True)

# 5.3 صفحة الذكاء الاصطناعي (النص الترويجي وتحفيز الأتمتة)
elif st.session_state.page == 'AI_Bot':
    st.header("🤖 أتمتة الأعمال الصناعية بالذكاء الاصطناعي")
    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 30px; border-radius: 15px; border-right: 10px solid #1E3A8A; direction: rtl; text-align: right;">
        <h2 style="color: #1E3A8A;">🚀 رؤية المهندس مجاهد في الأتمتة الصناعية</h2>
        <p style="font-size: 18px; line-height: 1.8;">
        يستطيع <b>المهندس مجاهد بشير</b> تحويل منشأتك التقليدية إلى منشأة ذكية من خلال <b>أتمتة الأعمال الصناعية المختلفة</b>. 
        نحن لا نصمم أنظمة فحسب، بل نبني حلولاً تفكر وتتوقع الأعطال قبل وقوعها.
        </p>
        <h4 style="color: #1E3A8A;">💎 مميزات تجعلنا خيارك الأول:</h4>
        <ul style="font-size: 16px;">
            <li><b>تقليل الهدر:</b> أتمتة العمليات تضمن تقليل الأخطاء البشرية بنسبة تصل إلى 95%.</li>
            <li><b>التوفير الذكي:</b> خوارزمياتنا تساهم في تقليل استهلاك الطاقة وتكاليف الصيانة الطارئة.</li>
            <li><b>دقة القرار:</b> تقارير ذكاء اصطناعي لحظية تدعم اتخاذ قراراتك الإدارية بناءً على أرقام حقيقية.</li>
            <li><b>الاستدامة:</b> ربط كامل بين الأداء الميكانيكي ومعايير البيئة (رؤية 2030).</li>
        </ul>
        <p style="font-weight: bold; color: #1E3A8A;">مستعد لنقل مصنعك للمستقبل؟ تواصل معي الآن عبر الواتساب في القائمة الجانبية.</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.caption(f"{PLATFORM_NAME} | 2026")
