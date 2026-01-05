import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import cv2
from PIL import Image
import datetime

# إعدادات الصفحة
st.set_page_config(page_title="AI Mechanical Monitor", layout="wide")

# --- الهوية المهنية (من سيرتك الذاتية) ---
st.title("🛠️ نظام الفحص الميكانيكي والتشخيص الذكي")
st.sidebar.info(f"المهندس: مجاهد بشير ")
st.sidebar.markdown("---")

# --- القسم الأول: لوحة تحكم الحساسات (Vibration & Temp) ---
st.header("📊 مراقبة حالة المعدة (Real-time Monitoring)")

col1, col2, col3 = st.columns(3)

with col1:
    vibration = st.slider("مستوى الاهتزاز (mm/s)", 0.0, 15.0, 4.5)
    # منطق معايير ISO 10816
    if vibration <= 2.8:
        status = "Good (Zone A)"
        color = "green"
    elif vibration <= 7.1:
        status = "Satisfactory (Zone B)"
        color = "orange"
    else:
        status = "Unacceptable (Zone D)"
        color = "red"

with col2:
    temp = st.number_input("درجة الحرارة (°C)", value=65)
    
with col3:
    # عداد السرعة (Gauge Chart) للاهتزاز
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vibration,
        title = {'text': "Vibration Status"},
        gauge = {'axis': {'range': [0, 15]},
                 'bar': {'color': color},
                 'steps': [
                     {'range': [0, 2.8], 'color': "lightgreen"},
                     {'range': [2.8, 7.1], 'color': "yellow"},
                     {'range': [7.1, 15], 'color': "salmon"}]}))
    st.plotly_chart(fig, use_container_width=True)

st.write(f"**حالة الماكينة الحالية:** :{color}[{status}]")

# --- القسم الثاني: التنبؤ بالعمر الافتراضي (AI Prediction) ---
st.divider()
st.header("🤖 التنبؤ بالأعطال (AI Predictive Maintenance)")

# نموذج رياضي مبسط لمحاكاة الذكاء الاصطناعي
rul_prediction = max(0, 100 - (vibration * 5) - (temp * 0.2))
st.metric("العمر الافتراضي المتبقي (RUL)", f"{int(rul_prediction)} يوم")
st.progress(int(rul_prediction) / 100)

# --- القسم الثالث: الفحص البصري (Computer Vision) ---
st.divider()
st.header("📸 الفحص البصري الآلي (Visual Inspection)")
uploaded_file = st.file_uploader("ارفع صورة للقطعة (تروس، محامل، شروخ)", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # معالجة الصورة باستخدام OpenCV
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    
    c1, c2 = st.columns(2)
    with c1:
        st.image(image, caption="الصورة الأصلية", use_container_width=True)
    with c2:
        st.image(edges, caption="تحليل الشروخ والعيوب السطحية", use_container_width=True)

# --- القسم الرابع: التقارير الإدارية (Management) ---
st.divider()
if st.button("توليد تقرير صيانة"):
    st.success(f"تم تسجيل التقرير بتاريخ {datetime.date.today()}")
    st.info("تنبيه: تم إرسال إشعار لمدير الصيانة بناءً على حالة المنطقة (Zone).")