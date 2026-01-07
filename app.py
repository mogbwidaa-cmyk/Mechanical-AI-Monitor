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

# --- 2. التصميم البصري (Professional CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; text-align: right; }
    .main { background-color: #0b111a; color: #e1e1e1; }
    .info-card { background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); padding: 25px; border-radius: 15px; color: white; margin-bottom: 25px; }
    .feature-box { background-color: #161b22; padding: 20px; border-radius: 12px; border-right: 5px solid #3b82f6; margin-bottom: 15px; }
    .stButton>button { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. القائمة الجانبية (الثوابت) ---
with st.sidebar:
    st.markdown(f"<div style='text-align: center;'><h2 style='color:white;'>م. مجاهد بشير</h2></div>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("القائمة الرئيسية", ["🏠 مركز التحكم", "🛠️ الصيانة التنبؤية (Vibration)", "🌱 هندسة الطاقة (PV System)", "🤖 حلول الأتمتة (AI)"])
    st.markdown("---")
    st.markdown(f"📱 التواصل: `{MY_PHONE}`")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/{MY_PHONE.replace('+', '')})")
    with c2: st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN_URL})")

# --- 4. محتوى المنصة ---

if menu == "🏠 مركز التحكم":
    st.markdown(f"<div class='info-card'><h1>🛡️ {PLATFORM_NAME}</h1><p>تكامل الذكاء الاصطناعي مع الخبرة الميكانيكية الميدانية.</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: st.markdown("<div class='feature-box'><h4>🔬 البحث العلمي</h4><p>حلول مبنية على أبحاث منشورة دولياً (Bio-Gas 2016).</p></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='feature-box'><h4>⚙️ أتمتة العمليات</h4><p>تحويل البيانات الميدانية إلى قرارات ذكية.</p></div>", unsafe_allow_html=True)

elif menu == "🛠️ الصيانة التنبؤية (Vibration)":
    st.subheader("🛠️ تحليل الاهتزازات الرقمي (FFT Diagnostic)")
    
    col_in, col_ch = st.columns([1, 2])
    with col_in:
        vibration = st.slider("مستوى الاهتزاز (mm/s RMS):", 0.0, 15.0, 3.2)
        rpm = st.number_input("سرعة الدوران (RPM):", 500, 5000, 1500)
        if st.button("إرسال تقرير التشخيص"):
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚨 تنبيه اهتزاز: {vibration} mm/s")
            st.toast("تم إرسال التقرير")
    with col_ch:
        freq_base = rpm / 60
        x = np.linspace(0, 500, 300)
        y = (np.exp(-((x - freq_base)**2)/30) * vibration) + (np.exp(-((x - 2*freq_base)**2)/60) * (vibration/3))
        fig = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy', line_color='#3b82f6'))
        fig.update_layout(height=350, template="plotly_dark", margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

elif menu == "🌱 هندسة الطاقة (PV System)":
    st.subheader("🌱 مراقبة كفاءة الأنظمة الضوئية")
    
    c1, c2, c3 = st.columns(3)
    temp = c1.slider("درجة الحرارة (C°)", 15, 65, 30)
    dust = c2.slider("تراكم الغبار (%)", 0, 100, 10)
    wind = c3.slider("سرعة الرياح (m/s)", 0, 25, 5)
    eff = max(0, 22.5 - (temp-25)*0.07 - dust*0.14 + wind*0.04)
    st.markdown(f"<div style='text-align: center;'><h2>الكفاءة المعايرة: {eff:.2f}%</h2></div>", unsafe_allow_html=True)
    st.progress(eff/25)

elif menu == "🤖 حلول الأتمتة (AI)":
    st.markdown(f"""
    <div class='feature-box'>
        <h2 style='color: #3b82f6;'>🤖 أتمتة الأعمال الصناعية مع م. مجاهد</h2>
        <p>يستطيع المهندس مجاهد بشير أتمتة العمليات الصناعية المختلفة لضمان أقصى كفاءة:</p>
        <ul>
            <li><b>الأتمتة الشاملة:</b> تقليل الخطأ البشري وزيادة سرعة الإنتاج.</li>
            <li><b>التوفير الذكي:</b> خوارزميات لتقليل استهلاك الطاقة وتكاليف الصيانة.</li>
            <li><b>دعم القرار:</b> تحويل الحساسات الميدانية إلى تقارير ذكاء اصطناعي لحظية.</li>
        </ul>
        <p><b>مميزات تحفيزية:</b> موثوقية تشغيلية 24/7، توافق مع رؤية 2030، وسهولة في التحكم عن بُعد.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 تفعيل روبوت الأتمتة"):
        st.balloons()
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🤖 طلب استشارة أتمتة من المنصة")

st.sidebar.caption(f"© 2026 {PLATFORM_NAME}")
