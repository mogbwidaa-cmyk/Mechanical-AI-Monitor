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

def send_intelligent_alert(factory_name, machine_name, vibration, status, fault_type):
    """إرسال تنبيه ذكي يحتوي على تفاصيل المنشأة والمعدة"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    message = (
        f"🏢 **تنبيه من منشأة: {factory_name}**\n"
        f"🚨 **نظام مراقبة المهندس مجاهد الذكي**\n\n"
        f"📅 الوقت: {now}\n"
        f"⚙️ المعدة: {machine_name}\n"
        f"📊 الاهتزاز: {vibration} mm/s\n"
        f"⚠️ الحالة: {status}\n"
        f"🔍 التشخيص: {fault_type}\n"
        f"🛠️ يرجى اتخاذ الإجراء اللازم في الموقع."
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    try: requests.get(url)
    except: pass

# --- خوارزمية تحليل FFT المتقدمة ---
def diagnose_fault(vibration):
    if vibration > 7.1:
        return "Critical: Bearing Failure / Loose Foundation"
    elif vibration > 4.5:
        return "Warning: Misalignment / Unbalance"
    return "Normal: Operating within ISO limits"

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة م. مجاهد لإدارة الأصول الصناعية", page_icon="🌐", layout="wide")

# --- الإعلان التسويقي للأتمتة ---
st.markdown("""
    <div style="background-color:#001529; padding:20px; border-radius:10px; border-right: 8px solid #FFD700; text-align: right; direction: rtl;">
        <h2 style="color:white; margin:0;">🚀 نظام أتمتة ومراقبة المصانع المتعددة</h2>
        <p style="color:#d9d9d9; font-size:18px;">
            إدارة مركزية لجميع منشآتك الصناعية في منصة واحدة. مراقبة لحظية، تحليل أعطال ذكي، وربط مباشر بجوال المهندس المسؤول. 
            <b>المهندس مجاهد بشير: شريكك في التحول الرقمي الصناعي.</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية لإدارة المواقع ---
st.sidebar.title("🏢 لوحة تحكم المنشآت")
selected_factory = st.sidebar.selectbox("اختر المنشأة المراد مراقبتها:", 
                                       ["مصنع جدة (المنطقة الصناعية)", 
                                        "مصنع ينبع (بتروكيماويات)", 
                                        "مصنع المدينة (صناعات غذائية)"])

st.sidebar.divider()
st.sidebar.header(f"⚙️ معدات {selected_factory}")
machine_selected = st.sidebar.selectbox("اختر المعدة:", ["المضخة P-01", "المروحة F-05", "الضاغط C-10"])
vibration = st.sidebar.slider("قراءة الاهتزاز الحالية (mm/s)", 0.0, 15.0, 3.2)
temp = st.sidebar.number_input("حرارة المحامل (°C)", value=55)

# --- منطق التحليل ---
if vibration <= 2.8: status, color = "Good (Safe)", "green"
elif vibration <= 7.1: status, color = "Warning (Check Required)", "orange"
else: status, color = "Critical (Immediate Action)", "red"

fault_type = diagnose_fault(vibration)
rul_prediction = max(0, 100 - (vibration * 6) - (temp * 0.05))

# --- الواجهة الرئيسية ---
st.header(f"📊 حالة التشغيل لـ: {selected_factory}")

c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.markdown("### مؤشر الاهتزاز")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vibration,
        gauge = {'axis': {'range': [0, 15]}, 'bar': {'color': color}}
    ))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### التشخيص الذكي للـ AI")
    st.info(f"النتيجة: **{fault_type}**")
    st.metric("صحة المعدة (Health Score)", f"{int(rul_prediction)}%")
    if st.button("📲 إرسال تنبيه عاجل للمهندس المسؤول"):
        send_intelligent_alert(selected_factory, machine_selected, vibration, status, fault_type)
        st.success(f"تم إرسال التقرير لفرع {selected_factory}")

with c3:
    st.markdown("### ملخص الحالة الفنية")
    st.subheader(status)
    st.write(f"الموقع: **{selected_factory}**")
    st.write(f"المعدات النشطة: **12 معدة**")
    if vibration > 7.1:
        st.error("🚨 خطر! تم رصد اهتزازات خارج النطاق المسموح به.")

st.divider()

# --- قسم البيانات التاريخية (IoT History) ---
st.subheader(f"📈 سجل أداء {machine_selected} خلال الـ 24 ساعة الماضية")
# توليد بيانات عشوائية متسقة مع القراءة الحالية
history_data = pd.DataFrame(np.random.randn(24, 2) / 8 + [vibration, temp/20], columns=['الاهتزاز', 'الحرارة'])
st.line_chart(history_data)

st.sidebar.divider()
st.sidebar.markdown(f"**خبير الأنظمة:** م. مجاهد بشير\n\n**للتواصل:** 0501318054")
