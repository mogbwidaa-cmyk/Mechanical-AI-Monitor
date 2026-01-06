import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import cv2
from PIL import Image
import datetime
from fpdf import FPDF
import io

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="نظام التشخيص الميكانيكي - المهندس مجاهد",
    page_icon="🛠️",
    layout="wide"
)

# --- دالة توليد PDF الاحترافية ---
def create_pdf(vibration, status, temp, rul):
    pdf = FPDF()
    pdf.add_page()
    
    # إعداد الخط والعنوان
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Mechanical Inspection Report", ln=True, align='C')
    pdf.ln(10)
    
    # بيانات المهندس مجاهد بشير
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Lead Engineer: Mogahed Bashir Ahmed", ln=True)
    pdf.cell(200, 10, txt=f"Location: Madinah Al Munawwarah, KSA", ln=True)
    pdf.cell(200, 10, txt=f"Phone: +966501318054", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True)
    
    # حالة التوظيف
    pdf.set_text_color(200, 0, 0)
    pdf.cell(200, 10, txt="Employment Status: Available for Hire / Ready to Start", ln=True)
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)
    pdf.cell(200, 10, txt="-------------------------------------------------------------------------", ln=True)
    pdf.ln(5)
    
    # النتائج الفنية
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Technical Analysis Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"- Vibration Level: {vibration} mm/s", ln=True)
    pdf.cell(200, 10, txt=f"- Machine Condition (ISO 10816): {status}", ln=True)
    pdf.cell(200, 10, txt=f"- Measured Temperature: {temp} C", ln=True)
    pdf.cell(200, 10, txt=f"- Predicted Remaining Useful Life (RUL): {int(rul)} Days", ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Generated via AI-Powered Mechanical Monitoring Platform", ln=True, align='C')
    
    # تصدير الملف كـ bytes
    return pdf.output(dest='S').encode('latin-1')

# --- القائمة الجانبية: هنا تظهر بياناتك الشخصية ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/6840/6840478.png", width=100)
st.sidebar.title("👤 الملف الشخصي")
st.sidebar.markdown(f"### **المهندس مجاهد بشير**")
st.sidebar.info("📍 **المدينة المنورة، السعودية**")
st.sidebar.write("📞 **الجوال:** `+966501318054` ")
st.sidebar.success("✅ **متاح للتوظيف فوراً**")

# روابط التواصل
linkedin_url = "https://www.linkedin.com/in/mogahed-bashir-52a5072ba/" # تأكد من صحة الرابط
st.sidebar.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin)]({linkedin_url})")

st.sidebar.divider()
st.sidebar.header("⚙️ إعدادات الحساسات")
vibration = st.sidebar.slider("مستوى الاهتزاز (mm/s)", 0.0, 15.0, 4.5)
temp = st.sidebar.number_input("درجة الحرارة (°C)", value=65)

# --- منطق التحليل الهندسي ---
if vibration <= 2.8:
    status = "Good (Zone A)"
    color = "green"
elif vibration <= 7.1:
    status = "Satisfactory (Zone B)"
    color = "orange"
else:
    status = "Unacceptable (Zone D)"
    color = "red"

rul_prediction = max(0, 100 - (vibration * 5) - (temp * 0.1))

# --- واجهة العرض الرئيسية ---
st.title("🛠️ المنصة الذكية لمراقبة المعدات الميكانيكية")
st.write("نظام متكامل لتحليل الاهتزازات والتنبؤ بالأعطال باستخدام الذكاء الاصطناعي.")

col1, col2 = st.columns([1, 1])

with col1:
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
    st.subheader("🤖 نتائج التشخيص الذكي")
    st.metric("العمر الافتراضي المتبقي (RUL)", f"{int(rul_prediction)} يوم")
    st.write(f"الحالة الراهنة: **{status}**")
    st.progress(int(rul_prediction) / 100)

# --- قسم الفحص البصري ---
st.divider()
st.header("📸 فحص السطح الميكانيكي (AI Vision)")
uploaded_file = st.file_uploader("ارفع صورة للتروس أو المحامل للكشف عن التآكل", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    c1, c2 = st.columns(2)
    with c1: st.image(image, caption="الصورة الأصلية", use_container_width=True)
    with c2: st.image(edges, caption="تحليل الشروخ والتآكل", use_container_width=True)

# --- قسم التقارير (التحميل المباشر) ---
st.divider()
st.header("📋 التوثيق الهندسي")
st.write("اضغط أدناه لتوليد وتحميل التقرير الرسمي بصيغة PDF.")

# تجهيز البيانات للتحميل
pdf_data = create_pdf(vibration, status, temp, rul_prediction)

# زر التحميل الرسمي الذي يعمل على الجوال والكمبيوتر
st.download_button(
    label="📥 تحميل تقرير المهندس مجاهد بشير (PDF)",
    data=pdf_data,
    file_name=f"Mechanical_Report_Mogahed_{datetime.date.today()}.pdf",
    mime="application/pdf"
)

st.sidebar.divider()
st.sidebar.caption("تم التطوير بواسطة م. مجاهد بشير - 2026")

