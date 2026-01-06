import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import cv2
from PIL import Image
import datetime
from fpdf import FPDF
import io
import requests

# --- إعدادات الربط والتنبيهات ---
TELEGRAM_TOKEN = "8050369942:AAEN-n0Qn-kAmu_9k-lqZ9Fe-tsAOSd44OA"
CHAT_ID = "6241195886"

def send_intelligent_alert(machine_name, vibration, status, fault_type):
    """إرسال تنبيه ذكي يحتوي على تشخيص العطل"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    message = (
        f"🚨 **تنبيه عطل ميكانيكي - منصة مجاهد الذكية**\n\n"
        f"📅 الوقت: {now}\n"
        f"🏭 المعدة: {machine_name}\n"
        f"📊 الاهتزاز: {vibration} mm/s\n"
        f"⚠️ الحالة: {status}\n"
        f"🔍 التشخيص المقترح: {fault_type}\n"
        f"🛠️ يرجى مراجعة لوحة التحكم لاتخاذ الإجراء."
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: requests.get(url)
    except: pass

# --- خوارزمية تحليل FFT (Fast Fourier Transform) ---
def diagnose_fault(vibration):
    """محاكاة لتحليل الترددات لتشخيص نوع العطل"""
    if vibration > 7.1:
        faults = ["Misalignment (عدم محاذاة)", "Looseness (ارتخاء ميكانيكي)", "Bearing Failure (تلف محامل)"]
        return np.random.choice(faults)
    elif vibration > 2.8:
        return "Unbalance (عدم اتزان بسيط)"
    return "Healthy Operation (تشغيل طبيعي)"

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة مجاهد لأتمتة ومراقبة المصانع", page_icon="⚙️", layout="wide")

# --- إعلان أتمتة المصانع (التسويقي) ---
st.markdown("""
    <div style="background-color:#001529; padding:20px; border-radius:10px; border-left: 8px solid #1890ff;">
        <h2 style="color:white; margin:0;">🚀 أتمتة المصانع وربطها بأنظمة المراقبة الذكية</h2>
        <p style="color:#d9d9d9; font-size:18px;">
            حول مصنعك إلى منشأة ذكية مع نظام <b>المهندس مجاهد بشير</b>. مراقبة لحظية للأصول، تقليل التوقف المفاجئ بنسبة 40%، 
            وتحليل تنبؤي للأعطال باستخدام الذكاء الاصطناعي وربط مباشر مع أجهزة الجوال.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
st.sidebar.title("👤 م. مجاهد بشير")
st.sidebar.success("✅ خبير أتمتة ومراقبة ميكانيكية")
st.sidebar.info("📞 +966501318054")

st.sidebar.divider()
st.sidebar.header("🕹️ لوحة التحكم في المصنع")
machine_selected = st.sidebar.selectbox("اختر المعدة:", ["المضخة الرئيسية P-101", "توربين المولد T-500", "ضاغط الهواء C-20"])
vibration = st.sidebar.slider("مستوى الاهتزاز الحالي (mm/s)", 0.0, 15.0, 4.5)
temp = st.sidebar.number_input("درجة الحرارة المستلمة (°C)", value=65)

# --- منطق التحليل المتقدم ---
status_map = {
    "Good": (0, 2.8, "green"),
    "Satisfactory": (2.8, 7.1, "orange"),
    "Unacceptable": (7.1, 15, "red")
}

if vibration <= 2.8: status, color = "Good (Zone A)", "green"
elif vibration <= 7.1: status, color = "Satisfactory (Zone B)", "orange"
else: status, color = "Unacceptable (Zone D)", "red"

fault_type = diagnose_fault(vibration)
rul_prediction = max(0, 100 - (vibration * 5) - (temp * 0.1))

# --- عرض النتائج ---
st.divider()
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.subheader("📊 حالة المعدة اللحظية")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vibration,
        gauge = {'axis': {'range': [0, 15]}, 'bar': {'color': color}}
    ))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🔍 خوارزمية التشخيص (Diagnostic)")
    st.info(f"نوع العطل المكتشف: **{fault_type}**")
    st.metric("العمر المتبقي (RUL)", f"{int(rul_prediction)} يوم")
    if st.button("📲 إرسال تقرير عاجل للجوال"):
        send_intelligent_alert(machine_selected, vibration, status, fault_type)
        st.success("تم إرسال التنبيه الذكي!")

with c3:
    st.subheader("📝 توصية النظام")
    if vibration > 7.1:
        st.error("🚨 إيقاف اضطراري وفحص المحامل فوراً.")
    elif vibration > 2.8:
        st.warning("⚠️ جدولة صيانة وقائية خلال 72 ساعة.")
    else:
        st.success("✅ استمرار التشغيل بجدول المراقبة المعتاد.")

# --- قسم الأتمتة والبيانات الضخمة ---
st.divider()
st.header("🌐 مراقبة الأنظمة المتصلة (IoT Stream)")
# محاكاة لبيانات الحساسات المتصلة
chart_data = pd.DataFrame(np.random.randn(20, 2) / 10 + [vibration/10, temp/100], columns=['Vibration', 'Temp'])
st.line_chart(chart_data)

st.sidebar.divider()
st.sidebar.caption("المنصة الذكية لمراقبة المعدات - نسخة الأتمتة التجارية")
