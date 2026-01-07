import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests

# --- 1. الثوابت (قواعد ثابتة لا تتغير) ---
st.set_page_config(page_title="منصة مراقبة المصانع والمعدات الميكانيكية", page_icon="🏗️", layout="wide")

MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
PLATFORM_NAME = "منصة مراقبة المصانع والمعدات الميكانيكية"
TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. دوال خفيفة الوزن (Cached Functions) ---
@st.cache_data
def get_fft_data(vib_level, freq_input):
    x = np.linspace(0, 500, 300) # تقليل النقاط لسرعة الرسم
    y = (np.exp(-((x - freq_input)**2)/50) * vib_level) + np.random.normal(0, 0.05, 300)
    return x, y

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try: requests.get(url, timeout=1) # تايم أوت قصير لعدم تعليق الموقع
    except: pass

# --- 3. القائمة الجانبية (الثوابت) ---
with st.sidebar:
    st.title("المهندس مجاهد بشير")
    st.write("🎓 باحث طاقة متجددة")
    st.divider()
    st.markdown(f"📞 `{MY_PHONE}`")
    
    # أزرار تواصل خفيفة
    st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat&logo=whatsapp&logoColor=white)](https://wa.me/{MY_PHONE.replace('+', '')})")
    st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)]({LINKEDIN_URL})")
    
    st.divider()
    page = st.radio("القائمة الرئيسية:", ["🏠 الرئيسية", "🛠️ الصيانة", "🌱 الطاقة", "🤖 الذكاء الاصطناعي"])

# --- 4. الواجهة الرئيسية ---
if page == "🏠 الرئيسية":
    st.markdown(f"<h1 style='text-align: center; color: #1E3A8A;'>🛡️ {PLATFORM_NAME}</h1>", unsafe_allow_html=True)
    st.write("---")
    st.columns(3)[1].image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=150)
    st.info("مرحباً بك في المنصة الموحدة. استخدم القائمة الجانبية للتنقل السريع بين الأقسام.")

# --- 5. الأقسام المحدثة ---

elif page == "🛠️ الصيانة":
    st.subheader("تحليل الاهتزاز الرقمي و FFT")
    v_col, f_col = st.columns(2)
    vib = v_col.slider("الاهتزاز (mm/s):", 0.0, 15.0, 3.5)
    freq = f_col.number_input("التردد (Hz):", 10, 500, 50)
    
    x, y = get_fft_data(vib, freq)
    fig = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy', line_color='#1E3A8A'))
    fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

elif page == "🌱 الطاقة":
    st.subheader("مراقبة كفاءة الخلايا الضوئية")
    c1, c2, c3 = st.columns(3)
    t, w, d = c1.slider("حرارة", 10, 60, 30), c2.slider("رياح", 0, 20, 5), c3.slider("غبار", 0, 100, 10)
    
    eff = max(0, 20.0 - (t-25)*0.05 - d*0.1 + w*0.02)
    st.metric("الكفاءة الحالية", f"{eff:.2f} %", delta=f"{eff-20:.1f} %")
    
    

elif page == "🤖 الذكاء الاصطناعي":
    st.success("### 🚀 أتمتة الأعمال مع المهندس مجاهد")
    st.write("""
    **لماذا تختار حلولنا الذكية؟**
    * أتمتة كاملة للعمليات الصناعية لتقليل الخطأ البشري.
    * نظام تنبيهات استباقي يحمي الأصول من التلف المفاجئ.
    * دمج بيانات الحساسات مع تقارير إدارية ذكية تدعم رؤية 2030.
    """)
    if st.button("تفعيل روبوت التوظيف والتحليل ⚡"):
        send_alert("🤖 تم تفعيل الروبوت الذكي من المنصة")
        st.toast("تم التفعيل!")

st.sidebar.caption(f"{PLATFORM_NAME}")
