import streamlit as st
import pandas as pd
import json
import base64
import math
import time
from algorithm import (
    huffman_compress, huffman_decompress,
    rle_compress, rle_decompress,
    lzw_compress, lzw_decompress
)

# Cấu hình trang
st.set_page_config(page_title="Data Compression", page_icon="🗜️", layout="wide")

# Hàm bổ trợ để xử lý dữ liệu nhị phân
def bytes_to_base64_text(data_bytes):
    return base64.b64encode(data_bytes).decode("ascii")

def base64_text_to_bytes(base64_text):
    return base64.b64decode(base64_text.encode("ascii"))

# Sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình")
    algorithm = st.selectbox("Thuật toán", ["Huffman", "RLE", "LZW"])
    mode = st.radio("Chế độ", ["Nén (Compress)", "Giải nén (Decompress)"])

st.title("🗜️ Hệ Thống Nén Dữ Liệu")

uploaded_file = st.file_uploader("📂 Tải lên file của bạn", type=None)

if uploaded_file:
    # Đọc dữ liệu dưới dạng bytes
    file_bytes = uploaded_file.getvalue()
    
    if mode == "Nén (Compress)":
        if st.button("Thực hiện Nén"):
            try:
                with st.spinner("Đang xử lý nén..."):
                    # 1. Chuyển file sang Base64 để đảm bảo an toàn ký tự
                    safe_text = bytes_to_base64_text(file_bytes)
                    original_bits = len(file_bytes) * 8
                    start_time = time.time()
                    
                    # 2. Thực hiện nén
                    if algorithm == "Huffman":
                        comp_data, codes, comp_bits, _ = huffman_compress(safe_text)
                        payload = {"algorithm": "Huffman", "data": comp_data, "codes": codes}
                        ext = ".huff"
                    elif algorithm == "RLE":
                        comp_data, _ = rle_compress(safe_text)
                        payload = {"algorithm": "RLE", "data": comp_data}
                        ext = ".rle"
                        # Ước tính số bit sau nén RLE
                        comp_bits = sum((math.ceil(math.log2(c+1)) + 8) for c, _ in comp_data)
                    elif algorithm == "LZW":
                        comp_data, dict_size, _ = lzw_compress(safe_text)
                        payload = {"algorithm": "LZW", "data": comp_data}
                        ext = ".lzw"
                        comp_bits = len(comp_data) * math.ceil(math.log2(max(dict_size, 1)))

                    exec_time = time.time() - start_time
                    
                    # 3. Đóng gói JSON
                    json_output = json.dumps(payload).encode("utf-8")
                    
                    # 4. Hiển thị kết quả
                    st.subheader("📊 Kết quả nén")
                    c1, c2, c3 = st.columns(3)
                    ratio = comp_bits / max(original_bits, 1)
                    c1.metric("Tỉ lệ nén", f"{ratio:.3f}")
                    c2.metric("Tiết kiệm", f"{max(0, (1-ratio)*100):.2f}%")
                    c3.metric("Thời gian", f"{exec_time:.4f}s")
                    
                    st.download_button(
                        label="⬇️ Tải file nén về máy",
                        data=json_output,
                        file_name=uploaded_file.name + ext,
                        mime="application/json"
                    )
                    st.success("Nén hoàn tất!")
            except Exception as e:
                st.error(f"Lỗi khi nén: {str(e)}")

    else: # CHẾ ĐỘ GIẢI NÉN
        if st.button("🔓 Thực hiện Giải nén"):
            try:
                with st.spinner("Đang xử lý giải nén..."):
                    # Đọc file JSON an toàn
                    try:
                        # Thử decode utf-8 trước, nếu lỗi dùng latin-1
                        try:
                            content_str = file_bytes.decode("utf-8")
                        except UnicodeDecodeError:
                            content_str = file_bytes.decode("latin-1")
                            
                        payload = json.loads(content_str)
                    except Exception:
                        st.error("File tải lên không phải là định dạng nén hợp lệ của ứng dụng này.")
                        st.stop()

                    algo_used = payload.get("algorithm")
                    data = payload.get("data")
                    
                    # Thực hiện giải nén tùy theo thuật toán ghi trong file
                    if algo_used == "Huffman":
                        recovered_text = huffman_decompress(data, payload.get("codes"))
                    elif algo_used == "RLE":
                        recovered_text, _ = rle_decompress(data)
                    elif algo_used == "LZW":
                        recovered_text, _ = lzw_decompress(data)
                    else:
                        st.error("Thuật toán không xác định.")
                        st.stop()
                    
                    # Chuyển từ Base64 về Bytes gốc
                    final_bytes = base64_text_to_bytes(recovered_text)
                    
                    st.success("Giải nén thành công!")
                    st.metric("Kích thước khôi phục", f"{len(final_bytes)} bytes")
                    
                    # Xử lý tên file
                    original_name = uploaded_file.name
                    for ext in [".huff", ".rle", ".lzw"]:
                        if original_name.endswith(ext):
                            original_name = original_name[:-len(ext)]
                    
                    st.download_button(
                        label="⬇️ Tải file đã khôi phục",
                        data=final_bytes,
                        file_name=f"restored_{original_name}",
                        mime="application/octet-stream"
                    )
            except Exception as e:
                st.error(f"Lỗi khi giải nén: {str(e)}")