import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime
import requests
import os

# --- 1. إعدادات المنصة (نظام إدارة الأصول والطاقة) ---
st.set_page_config(page_title="منصة م. مجاهد | مراقبة المصانع والطاقة", page_icon="🛡️", layout="wide")

# --- 2. البيانات المرجعية والتواصل ---
MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
RESEARCH_URL = "https://ijsrset.com/paper/1468.pdf"
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 3. نظام التنبيهات الذكي ---
def send_technical_alert(asset, value, status, recommendation):
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = (f"🚨 **تقرير فني عاجل**\n\n"
           f"⚙️ المعدة: {asset}\n"
           f"📊 الاهتزاز: {value} mm/s\n"
           f"⚠️ الحالة: {status}\n"
           f"💡 التوصية: {recommendation}\n"
           f"👤 المهندس المسؤول: م. مجاهد بشير\n"
           f"📞 للتواصل: {MY_PHONE}")
    try:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown")
        return True
    except: return False

# --- 4. القائمة الجانبية (الهوية المهنية والأكاديمية) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.markdown("🎓 **باحث دراسات عليا - طاقة متجددة**")
    st.success("📝 **مؤلف بحث علمي منشور دولياً (2016)**")
    st.caption("Bio Gas Production from Municipal Solid Waste")
    
    # أزرار التواصل السريع
    st.markdown(f"📞 **للتواصل المباشر:** `{MY_PHONE}`")
    c1, c2 = st.columns(2)
    with c1:
        whatsapp_url = f"https://wa.me/{MY_PHONE.replace('+', '')}"
        st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<a href="{LINKEDIN_URL}" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    
    st.divider()
    # قسم الأبحاث والتحميلات
    st.markdown("📄 **الوثائق المهنية:**")
    if os.path.exists("cv.pdf"):
        with open("cv.pdf", "rb") as f:
            st.download_button("📂 تحميل السيرة الذاتية (CV)", f, "cv.pdf", use_container_width=True)
    
    st.markdown(f'''<a href="{RESEARCH_URL}" target="_blank"><button style="width:100%; height:40px; background-color:#1B5E20; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">🔬 عرض الورقة البحثية</button></a>''', unsafe_allow_html=True)

    st.divider()
    st.header("⚙️ مدخلات مراقبة الأصول")
    factory = st.selectbox("المرفق الصناعي:", ["مجمع الغاز والزيت", "محطة الطاقة المتجددة", "وحدة إدارة النفايات"])
    machine = st.selectbox("المعدة المستهدفة:", ["P-101 Centrifugal Pump", "C-202 Compressor", "Bio-Gas Generator"])
    vib_val = st.slider("Overall Vibration (mm/s RMS):", 0.0, 15.0, 3.2)
    rpm_val = st.number_input("Operating Speed (RPM):", value=1450)
# --- إضافة قسم الروبوت الذكي داخل المنصة ---
with st.expander("🤖 تفعيل وكيل التوظيف الذكي (نظام 2026)"):
    st.markdown("### 🚀 مركز تحكم الروبوت الاستراتيجي")
    col_bot1, col_bot2 = st.columns([1, 1])
    
    with col_bot1:
        mode = st.radio("وضع تشغيل الروبوت:", 
                        ["التقديم التلقائي المخصص (Auto-Apply)", "تحليل فجوة المهارات في السوق"])
        
        if st.button("تفعيل الوكيل الذكي الآن ⚡"):
            # دالة إرسال التنبيه لتليجرام
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            msg = f"🤖 **تنبيه الروبوت:** تم تفعيل وضع {mode}\n👤 المهندس: مجاهد بشير\n📅 {timestamp}"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
            
            st.balloons()
            st.success("الروبوت باشر العمل وسيوافيك بالنتائج على تليجرام.")

    with col_bot2:
        # محاكاة خريطة الفرص بناءً على بحثك
        market_data = pd.DataFrame({
            'التخصص': ['الهيدروجين', 'تحويل النفايات (بحثك)', 'صيانة التوربينات'],
            'المطابقة': [85, 100, 75]
        })
        fig_bot = go.Figure(go.Bar(
            x=market_data['التخصص'], y=market_data['المطابقة'],
            marker_color=['#00d2ff', '#00ff88', '#FFD700']
        ))
        fig_bot.update_layout(title="نسبة مطابقة بروفايلك مع السوق", height=200, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_bot, use_container_width=True)

    st.info(f"🔗 **الروبوت مرتبط ببحثك:** {RESEARCH_TITLE}")
    
# --- 5. الواجهة الرئيسية (Dashboard) ---
st.markdown(f"""
    <div style="background-color:#001529; padding:25px; border-radius:15px; border-right: 10px solid #FFD700; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0; font-size:26px;">🛡️ منصة مراقبة المصانع والمعدات الميكانيكية</h1>
        <p style="color:#FFD700; font-size:18px; font-weight:bold; margin-top:10px;">نظام هندسي متقدم للصيانة التنبؤية وتحولات الطاقة</p>
    </div>
    """, unsafe_allow_html=True)

# معايير التقييم ISO 10816
if vib_val <= 2.8: 
    status, color = "آمن (Safe)", "green"
    recom = "استمرار التشغيل العادي ومراقبة الدورية."
elif vib_val <= 7.1: 
    status, color = "تحذير (Caution)", "orange"
    recom = "فحص التزييت وضبط المحاذاة في نافذة الصيانة القادمة."
else: 
    status, color = "حرج (Critical)", "red"
    recom = "إيقاف فوري للمعدة وإجراء تحليل الأسباب الجذرية (RCA)."

# عرض البيانات الفنية
st.write("")
col_g, col_t = st.columns([1, 2])

with col_g:
    st.subheader("📊 مؤشر الحالة الفنية")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=vib_val,
        title={'text': f"الحالة: {status}"},
        gauge={'bar': {'color': color}, 'axis': {'range': [0, 15]},
               'steps': [{'range': [0, 2.8], 'color': "#a3cfbb"}, 
                        {'range': [2.8, 7.1], 'color': "#ffeeba"}, 
                        {'range': [7.1, 15], 'color': "#f8d7da"}]}))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    if st.button("📤 توليد وإرسال تقرير التشخيص"):
        if send_technical_alert(machine, vib_val, status, recom):
            st.success("تم إرسال التقرير المعتمد للهاتف")

with col_t:
    st.subheader("🔬 التحليل الترددي اللحظي (FFT Analysis)")
    # محاكاة FFT بناءً على سرعة المعدة المكتوبة
    freq = np.linspace(0, 500, 250)
    base_f = rpm_val / 60
    amp = (np.exp(-((freq - base_f)**2) / 10) * vib_val) + (np.exp(-((freq - 2*base_f)**2) / 15) * (vib_val/3)) + np.random.normal(0, 0.05, 250)
    fig_fft = go.Figure(go.Scatter(x=freq, y=amp, fill='tozeroy', line=dict(color='#FFD700'), name="Spectrum"))
    fig_fft.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Amplitude (mm/s)", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_fft, use_container_width=True)

# --- 6. قسم الأبحاث العلمية (تحويل النفايات إلى طاقة) ---
st.divider()
st.subheader("🌱 السجل البحثي والأكاديمي (International Research)")
c_res1, c_res2 = st.columns([2, 1])

with c_res1:
    st.markdown(f"""
    ### **اسم البحث:** Bio Gas Production from Municipal Solid Waste
    **تاريخ النشر:** يونيو 2016  
    **المجلة:** IJSRSET | **الاعتماد:** ISSN: 2394-4099  
    **الملخص الفني:** تناول البحث دراسة تجريبية ونظرية لتحويل النفايات الصلبة إلى طاقة حيوية مستدامة، مع تحليل العوامل الميكانيكية والكيميائية المؤثرة على كفاءة الإنتاج.
    
    [🔗 رابط الوصول المباشر للبحث]({RESEARCH_URL})
    """)

with c_res2:
    st.info("""
    **مجالات التخصص:**
    - الصيانة التنبؤية (Vibration Analysis)
    - الطاقة المتجددة (Bio-Energy)
    - إدارة الأصول الصناعية (Asset Integrity)
    """)

st.sidebar.caption(f"تطوير م. مجاهد بشير © 2026 | {MY_PHONE}")


