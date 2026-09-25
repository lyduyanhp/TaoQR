import streamlit as st
import qrcode
from urllib.parse import urlparse
from io import BytesIO

# 1. Cấu hình trang tối giản
st.set_page_config(page_title="Tạo QR Code Nhanh", page_icon="🔳", layout="centered")

def generate_qr(url):
    """Xử lý tạo QR Code trực tiếp trên RAM"""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

# 2. Giao diện (Chỉ bao gồm Form và Kết quả)
st.title("Tạo QR Code")

# Block Form: Hỗ trợ Paste link và ấn Enter để chạy ngay
with st.form("qr_form", clear_on_submit=False):
    # Ô nhập liệu mở rộng, ẩn label thừa
    url_input = st.text_input("Link:", placeholder="Paste link vào đây (VD: facebook.com)...", label_visibility="collapsed")
    
    # Nút action
    submitted = st.form_submit_button("Tạo QR", type="primary")

# 3. Xử lý logic khi trigger event
if submitted:
    if url_input.strip():
        try:
            # Sinh mã QR
            qr_bytes = generate_qr(url_input)
            
            # Hiển thị kết quả ngay lập tức
            st.image(qr_bytes, width=250)
            
            # Khởi tạo nút tải file
            st.download_button(
                label="📥 Tải QR (PNG)",
                data=qr_bytes,
                file_name="QR_Code.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"[LỖI KỸ THUẬT] Không thể tạo QR. Mã lỗi: {str(e)}")
    else:
        st.warning("Vui lòng nhập đường link trước khi tạo.")