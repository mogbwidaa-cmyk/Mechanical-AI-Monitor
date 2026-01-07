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

# --- 2. التصميم البصري الجديد (Industrial Neon CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
    .main {{ background-color: #050a12; color: #ffffff; font-family: 'Tajawal', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: #0a111e; border-left: 1px solid #1f2937; }}
    
    .header-box {{
        background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%);
        padding: 30px;
        border-radius: 20px;
        border-right: 8px solid #38bdf8;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        text-align: right;
        margin-bottom: 30px;
    }}
    
    .stat-card {{
        background: #0f172a;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #1e293b;
        text-align: center;
        transition: 0.3s;
    }}
    .stat-card:hover {{ border-color: #38bdf8; transform: translateY(-5px); }}
    
    .stButton>button {{
        background: #38bdf8;
        color: #050a12;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        width: 100%;
    }}
    .stButton>button:hover {{ background: #7dd3fc; box-shadow: 0 0 15px #38bdf8; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. القائمة الجانبية (الثوابت المتفق عليها) ---
with st.sidebar:
    st.markdown(f"<div style='text-align: center;'><h2 style='color:#38bdf8; font-family:\"Orbitron\"'>ENGINEER</h2><h3 style='color:white;'>مجاهد بشير</h3></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.selectbox("📌 القائمة الفنية", ["🚀 مركز العمليات", "📉 تحليل الاهتزازات", "🔋 كفاءة الطاقة", "🤖 حلول الأتمتة"])
    
    st.markdown("---")
    st.markdown(f"📞 التواصل: `{MY_PHONE}`")
    
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/{MY_PHONE.replace('+', '')})")
    with c2: st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN_URL})")

# --- 4. محتوى الصفحات ---

if page == "🚀 مركز العمليات":
    st.markdown(f"""
        <div class="header-box">
            <h1 style="color:white; margin:0;">🛡️ {PLATFORM_NAME}</h1>
            <p style="color:#cbd5e1; font-size:18px;">نظام المراقبة الذكي والتحليل التنبؤي - إصدار 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown("<div class='stat-card'><h2 style='color:#38bdf8;'>98%</h2><p>الموثوقية التشغيلية</p></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='stat-card'><h2 style='color:#10b981;'>Active</h2><p>حالة الرصد الذكي</p></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='stat-card'><h2 style='color:#f59e0b;'>2016</h2><p>بداية التوثيق البحثي</p></div>", unsafe_allow_html=True)

elif page == "📉 تحليل الاهتزازات":
    st.header("📉 نظام تحليل الاهتزاز الرقمي (FFT)")
    
    c_in, c_ch = st.columns([1, 2])
    with c_in:
        v = st.slider("مستوى الاهتزاز (mm/s RMS):", 0.0, 15.0, 3.5)
        rpm = st.number_input("سرعة الدوران (RPM):", 500, 5000, 1500)
        if st.button("📤 إرسال تقرير التشخيص"):
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚨 تنبيه اهتزاز: {v} mm/s")
            st.toast("تم إرسال التقرير بنجاح")
    with c_ch:
        x = np.linspace(0, 500, 400)
        y = (np.exp(-((x - (rpm/60))**2)/20) * v) + (np.exp(-((x - 2*(rpm/60))**2)/40) * (v/2))
        fig = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy', line_color='#38bdf8'))
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🔋 كفاءة الطاقة":
    st.header("🔋 مراقبة ومعايرة الخلايا الضوئية")
    
    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        t = st.slider("الحرارة (C°)", 10, 65, 30)
        d = st.slider("الغبار (%)", 0, 100, 20)
        w = st.slider("الرياح (m/s)", 0, 25, 5)
    with col_s2:
        eff = max(0, 22.0 - (t-25)*0.08 - d*0.15 + w*0.05)
        st.markdown(f"<div style='text-align:center; padding:50px;'><h1>{eff:.2f}%</h1><p>الكفاءة الحالية</p></div>", unsafe_allow_html=True)
        st.progress(eff/25)

elif page == "🤖 حلول الأتمتة":
    st.markdown(f"""
        <div style="background:#1e293b; padding:40px; border-radius:20px; border-right:10px solid #10b981; direction:rtl;">
            <h2 style="color:#10b981;">🤖 أتمتة الأعمال مع المهندس مجاهد</h2>
            <p style="font-size:18px; line-height:1.6;">
            يمتلك المهندس <b>مجاهد بشير</b> القدرة على تحويل الأنظمة الصناعية التقليدية إلى أنظمة <b>مؤتمتة بالكامل</b> تعمل بالذكاء الاصطناعي.
            <br><br>
            <b>💎 لماذا تختار حلولنا للأتمتة؟</b><br>
            • <b>توفير التكاليف:</b> تقليل استهلاك الطاقة والهدر بنسبة تصل إلى 25%.<br>
            • <b>التنبؤ الذكي:</b> نظام لا يكتفي بالرصد، بل يتنبأ بالعطل قبل وقوعه.<br>
            • <b>التحكم عن بعد:</b> إدارة كاملة للمصنع عبر منصة رقمية موحدة وآمنة.<br>
            • <b>الاستدامة:</b> حلول متوافقة مع معايير البيئة العالمية ورؤية المملكة 2030.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 تفعيل نظام الاستجابة الذكي"):
        st.balloons()
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🤖 طلب استشارة أتمتة من المهندس مجاهد")

st.sidebar.caption(f"© 2026 {PLATFORM_NAME}")
