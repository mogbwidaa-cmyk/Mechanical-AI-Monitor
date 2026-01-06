# أضف هذا الجزء تحت رابط LinkedIn في الكود السابق:

st.sidebar.divider()
if cv_exists:
    with open(pdf_files[0], "rb") as f:
        st.sidebar.download_button(
            label="📄 تحميل السيرة الذاتية (CV)",
            data=f,
            file_name=pdf_files[0],
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.sidebar.warning("⚠️ يرجى إضافة ملف الـ CV للمجلد")
