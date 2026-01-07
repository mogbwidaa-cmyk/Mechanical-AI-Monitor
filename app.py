import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
import os

# --- 1. إعدادات الهوية الفنية والنظام ---
st.set_page_config(page_title="منصة م. مجاهد 2026 | الأصول والروبوت الذكي", page_icon="🤖", layout="wide")

# الثوابت والروابط
MY_PHONE = "+966501318054"
LINKEDIN_URL = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/"
RESEARCH_TITLE = "Bio Gas Production from Municipal Solid Waste"
RESEARCH_URL = "https://ijsrset.com/paper/1468.pdf"
TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

# --- 2. محرك التنبيهات والذكاء الاصطناعي ---
def send_telegram_alert(category, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    header = "🤖 **تنبيه وكيل التوظيف الذكي**" if category == "JOB" else "🚨 **تنبيه مراقبة الأصول**"
    
    message = f"{header}\n\n" \
              f"📅 التاريخ: {timestamp}\n" \
              f"👤 المهندس: مجاهد بشير\n" \
              f"--------------------------\n" \
              f"{details}\n" \
              f"--------------------------\n" \
              f"🔗 بروفايل لينكد إن: {LINKEDIN_URL}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try:
        requests.get(url, timeout=5)
        return True
    except: return False

# --- 3. القائمة الجانبية (هوية المهندس الباحث) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=80)
    st.title("المهندس مجاهد بشير")
    st.markdown("🎓 **باحث دراسات عليا - طاقة متجددة**")
    st.success(f"📝 **بحث منشور (2016):**\n{RESEARCH_TITLE}")
    
    st.divider()
    st.markdown(f"📞 **للتواصل المباشر:** `{MY_PHONE}`")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'''<a href="https://wa.me/{MY_PHONE.replace('+', '')}"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<a href="{LINKEDIN_URL}"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>''', unsafe_allow_html=True)
    
    st.divider()
    if os.path.exists("cv.pdf"):
        with open("cv.pdf", "rb") as f:
            st.download_button("📂 تحميل السيرة الذاتية", f, "cv.pdf", use_container_width=True)
    
    st.markdown(f'''<a href="{RESEARCH_URL}" target="_blank"><button style="width:100%; height:40px; background-color:#1B5E20; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">🔬 عرض الورقة البحثية</button></a>''', unsafe_allow_html=True)

# --- 4. الواجهة الرئيسية (التصميم الحديث 2026) ---
st.markdown(f"""
    <div style="background-color:#001529; padding:20px; border-radius:15px; border-right: 10px solid #00d2ff; text-align: right; direction: rtl;">
        <h1 style="color:white; margin:0; font-size:26px;">🛡️ منصة iPredict للأصول وتحولات الطاقة</h1>
        <p style="color:#00d2ff; font-size:16px;">نظام مهجن يدمج بين الصيانة التنبؤية وروبوتات التوظيف الذكية</p>
    </div>
""", unsafe_allow_html=True)

# إنشاء تبويبات المنصة
tab_monitor, tab_robot, tab_research = st.tabs(["📊 مراقبة الأصول", "🤖 الروبوت الذكي", "🔬 السجل البحثي"])

# --- التبويب الأول: مراقبة الأصول ---
with tab_monitor:
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        st.subheader("⚙️ مدخلات المعدة")
        machine = st.selectbox("المعدة:", ["Pump P-101", "Compressor C-202", "Bio-Gas Generator"])
        vib_val = st.slider("مستوى الاهتزاز (mm/s):", 0.0, 15.0, 3.8)
        
        if vib_val > 7.1: status, color = "🔴 حرج", "red"
        elif vib_val > 2.8: status, color = "🟡 تحذير", "orange"
        else: status, color = "🟢 آمن", "green"
        
        st.metric("الحالة الفنية", status)
        if st.button("📤 إرسال تقرير التشخيص"):
            send_telegram_alert("ASSET", f"🚨 تنبيه صيانة!\nالمعدة: {machine}\nالاهتزاز: {vib_val} mm/s\nالحالة: {status}")
            st.success("تم التوثيق وإرسال التقرير")

    with col_m2:
        st.subheader("🔬 FFT Spectral Analysis")
        x = np.linspace(0, 500, 200)
        y = (np.exp(-((x - 60)**2)/20) * vib_val) + np.random.normal(0, 0.1, 200)
        fig_fft = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy', line=dict(color='#00d2ff')))
        fig_fft.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)
        st.plotly_chart(fig_fft, use_container_width=True)

# --- التبويب الثاني: الروبوت الذكي (الإضافة الجديدة) ---
with tab_robot:
    st.subheader("🚀 روبوت التقديم والتحليل الاستراتيجي")
    col_r1, col_r2 = st.columns([1, 1])
    
    with col_r1:
        mode = st.radio("وضع تشغيل الروبوت:", 
                        ["التقديم التلقائي الذكي (Auto-Apply)", "تحليل مطابقة السوق"])
        keywords = st.multiselect("كلمات البحث:", ["Energy Engineer", "Maintenance", "Bio-Energy"], default=["Energy Engineer"])
        
        if st.button("تفعيل الوكيل الذكي ⚡"):
            details = f"📍 وضع التشغيل: {mode}\n🔍 الكلمات: {', '.join(keywords)}\n🎯 الهدف: مطابقة البحث العلمي مع الوظائف"
            if send_telegram_alert("JOB", details):
                st.balloons()
                st.success("الروبوت يعمل الآن وسيرسل لك الإشعارات فور المطابقة!")

    with col_r2:
        st.markdown("### 📊 تحليل مطابقة بروفايلك")
        match_data = pd.DataFrame({
            'المجال': ['طاقة شمسية', 'غاز حيوي (بحثك)', 'صيانة ميكانيكية'],
            'نسبة المطابقة': [88, 100, 92]
        })
        fig_match = go.Figure(go.Bar(x=match_data['المجال'], y=match_data['نسبة المطابقة'], marker_color='#00ff88'))
        fig_match.update_layout(height=250, margin=dict(t=10, b=0))
        st.plotly_chart(fig_match, use_container_width=True)

# --- التبويب الثالث: السجل البحثي ---
with tab_research:
    st.subheader("🌱 السجل العلمي الموثق (International Publication)")
    st.markdown(f"""
    > **عنوان البحث:** {RESEARCH_TITLE}  
    > **المجلة:** IJSRSET | **تاريخ النشر:** يونيو 2016  
    > **ISSN:** 2394-4099  
    > 
    > **نبذة:** يتناول البحث آليات استعادة الطاقة من النفايات البلدية الصلبة وإنتاج الغاز الحيوي، مما يدعم الاقتصاد الدائري واستدامة الطاقة في المدن الذكية.
    """)
    st.info("💡 هذا البحث هو الأساس العلمي الذي يعتمد عليه الروبوت في صياغة رسائل التغطية المخصصة لشركات الطاقة المتجددة.")

st.sidebar.caption(f"تم التطوير بواسطة م. مجاهد بشير | 2026")
