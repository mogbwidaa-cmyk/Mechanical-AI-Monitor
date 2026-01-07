import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests

# --- 1. الثوابت والقواعد الراسخة (لا تتغير) ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="🏗️", layout="wide")

MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
PLATFORM_NAME = "منصة مراقبة المصانع والمعدات الميكانيكية"
TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. التصميم الجديد: تباين عالي ووضوح فائق (Engineering Clean UI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
    /* تنسيق عام للمنصة */
    .main {{ background-color: #ffffff; color: #1a1a1a; font-family: 'Tajawal', sans-serif; }}
    
    /* الهيدر الرئيسي */
    .main-header {{
        background-color: #f0f4f8;
        padding: 25px;
        border-radius: 12px;
        border-bottom: 4px solid #1e3a8a;
        text-align: right;
        margin-bottom: 30px;
    }}
    
    /* بطاقات المحتوى */
    .content-card {{
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    
    /* أزرار واضحة */
    .stButton>button {{
        background-color: #1e3a8a;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 12px;
        font-weight: bold;
        width: 100%;
    }}
    .stButton>button:hover {{ background-color: #2563eb; color: white; }}
    
    /* العناوين */
    h1, h2, h3 {{ color: #1e3a8a; font-weight: 700; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. القائمة الجانبية (الثوابت المتفق عليها) ---
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center; color: #1e3a8a;'>م. مجاهد بشير</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # قائمة التنقل بوضوح عالي
    page = st.radio("القائمة الفنية:", 
                    ["🏠 لوحة التحكم الرئيسية", "🛠️ الصيانة وتحليل الاهتزاز", "🌱 كفاءة الطاقة الشمسية", "🤖 حلول الأتمتة والذكاء"])
    
    st.write("---")
    st.markdown(f"📞 **للتواصل:** `{MY_PHONE}`")
    
    # أزرار تواصل احترافية وواضحة
    st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-التواصل%20السريع-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/{MY_PHONE.replace('+', '')})")
    st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-الملف%20الشخصي-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN_URL})")

# --- 4. محتوى الأقسام ---

if page == "🏠 لوحة التحكم الرئيسية":
    st.markdown(f"""
        <div class="main-header">
            <h1>🛡️ {PLATFORM_NAME}</h1>
            <p style="font-size: 1.1em; color: #4a5568;">النظام الموحد لمراقبة أداء الأصول وتطوير حلول الطاقة المستدامة</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='content-card'><h3>🎯 أهداف المنصة</h3><p>دمج أنظمة الرصد اللحظي مع التحليلات المتقدمة لتقليل فترات التوقف وتحسين استغلال الموارد الطاقية.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='content-card'><h3>📝 التوثيق الهندسي</h3><p>كافة العمليات والتحليلات مبنية على معايير الجودة الميكانيكية (ISO) والأبحاث العلمية الموثقة.</p></div>", unsafe_allow_html=True)

elif page == "🛠️ الصيانة وتحليل الاهتزاز":
    st.header("🛠️ نظام تحليل الاهتزاز الرقمي (FFT)")
    
    col_input, col_plot = st.columns([1, 2])
    
    with col_input:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        v = st.slider("مستوى الاهتزاز (mm/s RMS):", 0.0, 15.0, 3.5)
        rpm = st.number_input("سرعة الدوران (RPM):", 500, 5000, 1500)
        if st.button("إرسال تقرير التشخيص"):
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚨 تقرير من {PLATFORM_NAME}: الاهتزاز {v} mm/s")
            st.success("تم إرسال التقرير بنجاح")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_plot:
        x = np.linspace(0, 500, 400)
        y = (np.exp(-((x - (rpm/60))**2)/20) * v) + (np.exp(-((x - 2*(rpm/60))**2)/40) * (v/2))
        fig = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy', line_color='#1e3a8a'))
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=350, margin=dict(l=0,r=0,t=10,b=0))
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        st.plotly_chart(fig, use_container_width=True)

elif page == "🌱 كفاءة الطاقة الشمسية":
    st.header("🌱 مراقبة ومعايرة الكفاءة (PV System)")
    
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    temp = c1.slider("الحرارة المحيطة (C°)", 10, 65, 30)
    dust = c2.slider("نسبة تراكم الغبار (%)", 0, 100, 20)
    wind = c3.slider("سرعة الرياح (m/s)", 0, 25, 5)
    
    eff = max(0, 22.0 - (temp-25)*0.08 - dust*0.15 + wind*0.05)
    st.markdown(f"<div style='text-align: center;'><h3>كفاءة النظام الحالية: <span style='color: #1e3a8a;'>{eff:.2f}%</span></h3></div>", unsafe_allow_html=True)
    st.progress(eff/25)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🤖 حلول الأتمتة والذكاء":
    st.markdown(f"""
        <div class="content-card" style="border-right: 8px solid #10b981;">
            <h2 style="color: #10b981;">🤖 أتمتة الأعمال مع المهندس مجاهد</h2>
            <p style="font-size: 1.1em; line-height: 1.6;">
            يتمتع المهندس <b>مجاهد بشير</b> بخبرة واسعة في <b>أتمتة الأعمال الصناعية المختلفة</b>، محولاً التحديات التشغيلية إلى حلول رقمية ذكية.
            <br><br>
            <b>💎 مميزات حلولنا للأتمتة:</b><br>
            • <b>تحسين التكاليف:</b> تقليل الهدر الطاقي والميكانيكي عبر المراقبة الذكية.<br>
            • <b>نظم الاستجابة اللحظية:</b> أتمتة التقارير والتنبيهات لضمان التدخل السريع.<br>
            • <b>تحليل البيانات الضخمة:</b> معالجة بيانات الحساسات لاتخاذ قرارات دقيقة.<br>
            • <b>التوافق مع رؤية 2030:</b> حلول تدعم التحول الرقمي والاستدامة الصناعية.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 تفعيل نظام التواصل الذكي للأتمتة"):
        st.balloons()
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🤖 طلب استشارة أتمتة من المهندس مجاهد")

st.sidebar.caption(f"© 2026 {PLATFORM_NAME}")
