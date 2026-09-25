import streamlit as st
import qrcode
from urllib.parse import urlparse
from io import BytesIO

# 1. Cấu hình trang tối giản
st.set_page_config(page_title="Tạo QR Code Nhanh", page_icon="🔳", layout="centered")

def generate_qr(url, box_size):
    """Xử lý tạo QR Code trực tiếp trên RAM với kích thước động"""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size, # Khớp với tham số được truyền từ UI
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

# 2. Giao diện (Thêm bộ chọn kích thước)
st.title("Tạo QR Code")

# Khai báo biến môi trường cho các mốc kích thước
SIZE_MAPPING = {
    "Tiêu chuẩn (Phù hợp gửi qua chat - ~400x400px)": 10,
    "Lớn (Phù hợp chèn vào Word/PowerPoint - ~800x800px)": 20,
    "Rất lớn (Chất lượng cao để in Banner/Poster - ~1200x1200px)": 30
}

with st.form("qr_form", clear_on_submit=False):
    # Ô nhập link
    url_input = st.text_input("Link:", placeholder="Paste link vào đây (VD: facebook.com)...", label_visibility="collapsed")
    
    # Dropdown menu chọn kích thước
    selected_size_label = st.selectbox(
        "Chọn kích thước tải về:",
        options=list(SIZE_MAPPING.keys()),
        index=0 # Mặc định chọn kích thước Tiêu chuẩn
    )
    
    # Nút action
    submitted = st.form_submit_button("Tạo QR", type="primary")

# 3. Xử lý logic sự kiện
if submitted:
    if url_input.strip():
        try:
            # Lấy giá trị số (box_size) từ label người dùng chọn
            target_box_size = SIZE_MAPPING[selected_size_label]
            
            # Sinh mã QR
            qr_bytes = generate_qr(url_input, target_box_size)
            
            # KHUNG HIỂN THỊ: Ép width=250 để giao diện web không bị phình to
            st.image(qr_bytes, width=250)
            
            # Tên file động dựa trên kích thước
            file_name_suffix = selected_size_label.split(" ")[0].upper()
            
            # KHUNG XUẤT FILE: File tải về giữ nguyên dung lượng gốc (có thể lên tới 1200px)
            st.download_button(
                label="📥 Tải QR (PNG)",
                data=qr_bytes,
                file_name=f"QR_{file_name_suffix}.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"[LỖI KỸ THUẬT] Hệ thống không thể sinh mã QR. Báo cáo lỗi: {str(e)}")
    else:
        st.warning("Vui lòng nhập đường link trước khi tạo.")
