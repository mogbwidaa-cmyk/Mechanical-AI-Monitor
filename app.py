import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests

# --- 1. الثوابت المتفق عليها (لا تتغير) ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="🏗️", layout="wide")

MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
PLATFORM_NAME = "منصة مراقبة المصانع والمعدات الميكانيكية"
TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. تحسين مظهر CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #1E3A8A; color: white; border: none; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #3b82f6; border: none; }
    .card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-right: 5px solid #1E3A8A; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. القائمة الجانبية المنسقة ---
with st.sidebar:
    st.markdown(f"<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/6840/6840478.png' width='80'><br><h3>م. مجاهد بشير</h3></div>", unsafe_allow_html=True)
    st.write("---")
    
    # اختيار الأقسام بأيقونات
    page = st.selectbox("انتقل إلى القسم:", ["🏠 الرئيسية", "🛠️ الصيانة التنبؤية", "🌱 كفاءة الخلايا الضوئية", "🤖 أتمتة الذكاء الاصطناعي"])
    
    st.write("---")
    st.markdown(f"📱 **تواصل مباشر:**")
    st.markdown(f"[`{MY_PHONE}`](tel:{MY_PHONE})")
    
    # أزرار التواصل بشكل أنيق
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/{MY_PHONE.replace('+', '')})")
    with c2: st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN_URL})")

# --- 4. محتوى الصفحات بتنسيق محسّن ---

if page == "🏠 الرئيسية":
    st.markdown(f"<h1 style='text-align: center;'>🛡️ {PLATFORM_NAME}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #666;'>بوابة هندسية متطورة لإدارة الأصول والطاقة المستدامة</p>", unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>🎯 رؤية المنصة</h3>
            <p>تهدف المنصة لدمج الخبرات الميكانيكية الميدانية مع الحلول البرمجية الذكية لرفع كفاءة الإنتاج وتقليل تكاليف الصيانة.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card">
            <h3>🔬 الخبرة البحثية</h3>
            <p>أنظمة مبنية على أسس أكاديمية موثقة دولياً في مجال الطاقة الحيوية واستدامة الأصول منذ عام 2016.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "🛠️ الصيانة التنبؤية":
    st.markdown("<h2>🛠️ تحليل الاهتزازات الرقمي (FFT)</h2>", unsafe_allow_html=True)
    with st.container():
        col_in, col_gr = st.columns([1, 2])
        with col_in:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            vib = st.slider("مستوى الاهتزاز (mm/s):", 0.0, 15.0, 3.5)
            freq = st.number_input("التردد الأساسي (Hz):", 10, 500, 60)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_gr:
            x = np.linspace(0, 500, 300)
            y = (np.exp(-((x - freq)**2)/40) * vib) + (np.exp(-((x - 2*freq)**2)/80) * (vib/2))
            fig = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy', line_color='#1E3A8A', name="FFT Spectrum"))
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

elif page == "🌱 كفاءة الخلايا الضوئية":
    st.markdown("<h2>🌱 مراقبة ومعايرة الكفاءة الشمسية</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    temp = c1.select_slider("الحرارة (C°)", options=list(range(10, 61)), value=30)
    wind = c2.select_slider("الرياح (m/s)", options=list(range(0, 21)), value=5)
    dust = c3.select_slider("الغبار (%)", options=list(range(0, 101)), value=15)
    
    eff = max(0, 20.0 - (temp-25)*0.06 - dust*0.12 + wind*0.03)
    st.markdown(f"<h3 style='text-align: center;'>الكفاءة اللحظية: {eff:.2f}%</h3>", unsafe_allow_html=True)
    st.progress(eff/25)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🤖 أتمتة الذكاء الاصطناعي":
    st.markdown("<div class='card' style='border-right: 5px solid #FFD700;'>", unsafe_allow_html=True)
    st.markdown("<h2>🤖 م. مجاهد بشير: خبير الأتمتة الصناعية</h2>", unsafe_allow_html=True)
    st.write("""
    **الذكاء الاصطناعي في خدمتك:**
    * **أتمتة العمليات:** تقليل التدخل البشري في المهام المتكررة.
    * **الرصد الذكي:** ربط الحساسات الميدانية بنظام تنبيهات فوري.
    * **تحليل البيانات:** تحويل الأرقام الخام إلى قرارات استراتيجية.
    """)
    if st.button("🚀 تفعيل نظام الاستجابة الذكي"):
        st.toast("جاري الاتصال بروبوت التوظيف...")
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🤖 طلب جديد لتجربة الأتمتة من المنصة")
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.caption(f"© 2026 {PLATFORM_NAME}")
