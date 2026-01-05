import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import cv2
from PIL import Image
import datetime
from fpdf import FPDF
import base64

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام التشخيص الميكانيكي الذكي", layout="wide")

# --- دالة توليد تقرير PDF ---
def create_pdf(vibration, status, temp, rul):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # عنوان التقرير
    pdf.cell(200, 10, txt="Mechanical Inspection Report", ln=True, align='C')
    pdf.ln(10)
    
    # تفاصيل المهندس والبيانات (مستمدة من سيرتك الذاتية)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True)
    pdf.cell(200, 10, txt=f"Lead Engineer: Mogahed Bashir Ahmed", ln=True)
    pdf.cell(200, 10, txt=f"Location: Dammam, KSA", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="--------------------------------------------------", ln=True)
    
    # النتائج التقنية
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Technical Analysis Results:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"- Vibration Level: {vibration} mm/s", ln=True)
    pdf.cell(200, 10, txt=f"- Machine Status (ISO 10816): {status}", ln=True)
    pdf.cell(200, 10, txt=f"- Operating Temperature: {temp} C", ln=True)
    pdf.cell(200, 10, txt=f"- Predicted Remaining Useful Life (RUL): {int(rul)} Days", ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="This report was generated automatically by the AI Maintenance System.", ln=True, align='C')
    
    # تحويل الـ PDF إلى بايتات للتحميل
    return pdf.output(dest='S').encode('latin-1')

# --- واجهة المستخدم الرئيسية ---
st.title("🛠️ المنصة الذكية لمراقبة وتشخيص المعدات الميكانيكية")
st.markdown(f"**إعداد المهندس:** مجاهد بشير | **تاريخ التقرير:** {datetime.date.today()}")

# --- القسم الأول: لوحة تحكم الاهتزاز والحرارة ---
st.sidebar.header("⚙️ مدخلات الحساسات")
vibration = st.sidebar.slider("مستوى الاهتزاز (mm/s)", 0.0, 15.0, 4.5)
temp = st.sidebar.number_input("درجة الحرارة المستمرة (°C)", value=65)

st.header("📊 مراقبة حالة المعدة لحظياً")
col1, col2 = st.columns([1, 1])

# تحديد الحالة بناءً على ISO 10816
if vibration <= 2.8:
    status = "Good (Zone A)"
    color = "green"
elif vibration <= 7.1:
    status = "Satisfactory (Zone B)"
    color = "orange"
else:
    status = "Unacceptable (Zone D)"
    color = "red"

with col1:
    # رسم عداد الاهتزاز
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vibration,
        title = {'text': "Vibration Severity (ISO 10816)"},
        gauge = {'axis': {'range': [0, 15]},
                 'bar': {'color': color},
                 'steps': [
                     {'range': [0, 2.8], 'color': "#a3cfbb"},
                     {'range': [2.8, 7.1], 'color': "#fff3cd"},
                     {'range': [7.1, 15], 'color': "#f8d7da"}]}))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🤖 تحليل الذكاء الاصطناعي")
    # محاكاة التنبؤ بالعمر الافتراضي (RUL)
    rul_prediction = max(0, 100 - (vibration * 5) - (temp * 0.2))
    st.metric("العمر الافتراضي المتبقي (RUL)", f"{int(rul_prediction)} يوم")
    st.progress(int(rul_prediction) / 100)
    st.write(f"الحالة التشخيصية: **{status}**")

# --- القسم الثاني: الفحص البصري الآلي ---
st.divider()
st.header("📸 الفحص البصري واكتشاف العيوب (Computer Vision)")
st.write("ارفع صورة لسطح المعدة للكشف عن الشروخ أو التآكل برمجياً.")

uploaded_file = st.file_uploader("اختر صورة ميكانيكية...", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # معالجة الصورة لاكتشاف الحواف (Edges) لمحاكاة اكتشاف الشروخ
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    c1, c2 = st.columns(2)
    with c1:
        st.image(image, caption="الصورة الأصلية للمعدة", use_container_width=True)
    with c2:
        st.image(edges, caption="نتائج معالجة الصور (اكتشاف الشروخ/التآكل)", use_container_width=True)

# --- القسم الثالث: التقارير والتحميل ---
st.divider()
st.header("📋 إدارة التقارير الهندسية")
if st.button("توليد تقرير PDF احترافي"):
    try:
        pdf_content = create_pdf(vibration, status, temp, rul_prediction)
        b64 = base64.b64encode(pdf_content).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Maintenance_Report_{datetime.date.today()}.pdf">📥 اضغط هنا لتحميل التتقرير المعتمد</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("تم توليد التقرير بناءً على المدخلات الحالية.")
    except Exception as e:
        st.error(f"حدث خطأ أثناء توليد التقرير: {e}")

# تذييل الصفحة
st.sidebar.markdown("---")
st.sidebar.write("© 2024 نظام الصيانة التنبؤية الذكي")
st.sidebar.write("تصميم المهندس مجاهد بشير")
