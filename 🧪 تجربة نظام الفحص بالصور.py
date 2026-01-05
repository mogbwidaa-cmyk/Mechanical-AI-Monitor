import streamlit as st
import cv2
import numpy as np
from PIL import Image

# تأكد أن هذا السطر موجود قبل أي استخدام لـ st
st.title("📸 نظام الفحص البصري الذكي بواسطة مهندس مجاهد بشير")

uploaded_img = st.file_uploader("ارفع صورة للقطعة الميكانيكية", type=["jpg", "png", "jpeg"])

if uploaded_img is not None:
    # معالجة الصورة
    image = Image.open(uploaded_img)
    img_array = np.array(image)
    
    # تحويل الصورة لرمادي واكتشاف الحواف
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    
    # عرض النتائج
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="الصورة الأصلية", use_container_width=True)
    with col2:
        st.image(edges, caption="نتائج تحليل الشروخ (Edges)", use_container_width=True)