import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات المنصة (ثوابت لا تتغير) ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="🛡️", layout="wide")

MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
PLATFORM_NAME = "منصة مراقبة المصانع والمعدات الميكانيكية"
RESEARCH_TITLE = "Bio Gas Production from Municipal Solid Waste"
RESEARCH_URL = "https://ijsrset.com/paper/1468.pdf"
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. نظام التنبيهات الذكي ---
def send_technical_alert(category, details):
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    header = "🚨 **تنبيه فني: مراقبة الأصول**" if category == "ASSET" else "🤖 **تنبيه: وكيل الأتمتة والتوظيف**"
    msg = (f"{header}\n\n"
           f"📅 التاريخ: {now}\n"
           f"👤 المهندس: مجاهد بشير\n"
           f"--------------------------\n"
           f"{details}\n"
           f"--------------------------\n"
           f"📞 للتواصل: {MY_PHONE}")
    try:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown")
        return True
    except: return False

# --- 3. القائمة الجانبية (الهوية المهنية) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.markdown("🎓 **باحث دراسات عليا - طاقة متجددة**")
    
    st.divider()
    st.markdown(f"📞 **للتواصل:** `{MY_PHONE}`")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'''<a href="https://wa.me/{MY_PHONE.replace('+', '')}"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<a href="{LINKEDIN_URL}"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    
    st.divider()
    st.header("⚙️ مدخلات المراقبة")
    machine = st.selectbox("المعدة المستهدفة:", ["P-101 Centrifugal Pump", "C-202 Compressor", "Bio-Gas Generator"])
    vib_val = st.slider("Vibration (mm/s RMS):", 0.0, 15.0, 3.2)
    rpm_val = st.number_input("Operating Speed (RPM):", value=1450)

# --- 4. الواجهة الرئيسية ---
st.markdown(f"""
    <div style="background-color:#001529; padding:25px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0; font-size:26px;">🛡️ {PLATFORM_NAME}</h1>
        <p style="color:#FFD700; font-size:18px; margin-top:10px;">نظام هندسي متكامل للصيانة التنبؤية وتحولات الطاقة</p>
    </div>
    """, unsafe_allow_html=True)

# تفعيل الروبوت (Expander)
with st.expander("🤖 تفعيل وكيل الأتمتة والتقديم الذكي (نظام 2026)"):
    st.markdown("### 🚀 مركز تحكم الروبوت الاستراتيجي")
    col_bot1, col_bot2 = st.columns([1, 1])
    with col_bot1:
        mode = st.radio("وضع التشغيل:", ["التقديم التلقائي (Auto-Apply)", "أتمتة العمليات الصناعية"])
        if st.button("تفعيل الوكيل الآن ⚡"):
            send_technical_alert("ROBOT", f"تم تفعيل وضع {mode} بنجاح.")
            st.balloons()
            st.success("الروبوت باشر العمل وسيوافيك بالنتائج على تليجرام.")
    with col_bot2:
        st.markdown("**تحليل مطابقة المهارات مع السوق**")
        match_fig = go.Figure(go.Bar(x=['الهيدروجين', 'الغاز الحيوي', 'الصيانة'], y=[85, 100, 90], marker_color='#FFD700'))
        match_fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(match_fig, use_container_width=True)

# تحليل الاهتزاز (Vibration Analysis)
st.write("")
col_g, col_t = st.columns([1, 2])

# معايير ISO 10816
if vib_val <= 2.8: status, color, recom = "آمن (Safe)", "green", "استمرار التشغيل العادي."
elif vib_val <= 7.1: status, color, recom = "تحذير (Caution)", "orange", "فحص التزييت وضبط المحاذاة."
else: status, color, recom = "حرج (Critical)", "red", "إيقاف فوري للمعدة (RCA Required)."

with col_g:
    st.subheader("📊 مؤشر الحالة الفنية")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=vib_val,
        title={'text': f"الحالة: {status}"},
        gauge={'bar': {'color': color}, 'axis': {'range': [0, 15]},
               'steps': [{'range': [0, 2.8], 'color': "#a3cfbb"}, {'range': [2.8, 7.1], 'color': "#ffeeba"}, {'range': [7.1, 15], 'color': "#f8d7da"}]}))
    st.plotly_chart(fig_gauge, use_container_width=True)
    if st.button("📤 إرسال تقرير التشخيص"):
        send_technical_alert("ASSET", f"المعدة: {machine}\nالاهتزاز: {vib_val}\nالحالة: {status}\nالتوصية: {recom}")
        st.success("تم الإرسال!")

with col_t:
    st.subheader("🔬 التحليل الترددي الرقمي (FFT)")
    
    freq = np.linspace(0, 500, 250)
    base_f = rpm_val / 60
    amp = (np.exp(-((freq - base_f)**2) / 10) * vib_val) + (np.exp(-((freq - 2*base_f)**2) / 15) * (vib_val/3)) + np.random.normal(0, 0.05, 250)
    fig_fft = go.Figure(go.Scatter(x=freq, y=amp, fill='tozeroy', line=dict(color='#FFD700')))
    fig_fft.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Amplitude", height=300, margin=dict(t=10, b=10))
    st.plotly_chart(fig_fft, use_container_width=True)

# كفاءة الطاقة الشمسية (القسم الجديد)
st.divider()
st.subheader("🌱 مراقبة كفاءة الخلايا الضوئية (PV Efficiency)")

c1, c2, c3, c4 = st.columns(4)
temp = c1.slider("حرارة (C°)", 10, 60, 30)
dust = c2.slider("غبار (%)", 0, 100, 15)
wind = c3.slider("رياح (m/s)", 0, 20, 5)
eff = max(0, 20.0 - (temp-25)*0.07 - dust*0.12 + wind*0.04)
c4.metric("الكفاءة الفعلية", f"{eff:.2f}%", delta=f"{eff-20:.1f}%")

# قسم الأبحاث
st.divider()
st.subheader("🔬 السجل البحثي (Bio-Gas Research)")
st.markdown(f"""
**عنوان البحث:** {RESEARCH_TITLE} (2016)  
يتناول البحث تحويل النفايات الصلبة إلى طاقة حيوية مستدامة، وهو مدمج حالياً في خوارزميات الأتمتة الخاصة بالمنصة.  
[📄 عرض البحث بالكامل]({RESEARCH_URL})
""")

st.sidebar.caption(f"تطوير م. مجاهد بشير © 2026 | {MY_PHONE}")
