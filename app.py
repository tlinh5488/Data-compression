import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import base64
import math

from algorithm import (
    huffman_compress,
    huffman_decompress,
    rle_compress,
    rle_decompress,
    lzw_compress,
    lzw_decompress,
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Compression Demo",
    layout="wide"
)

st.title("🗜️ Data Compression Demo")

# =====================================================
# SIDEBAR
# =====================================================

algorithm = st.sidebar.selectbox(
    "Algorithm",
    ["Huffman", "RLE", "LZW"]
)

mode = st.sidebar.radio(
    "Mode",
    ["Compress", "Decompress"]
)

uploaded_file = st.file_uploader(
    "Upload File",
    type=None
)

# =====================================================
# HELPERS
# =====================================================

def bytes_to_text(data_bytes):
    """
    Convert any file bytes -> safe text
    """
    return base64.b64encode(data_bytes).decode("utf-8")


def text_to_bytes(text):
    """
    Restore original bytes
    """
    return base64.b64decode(text.encode("utf-8"))


def serialize_rle(data):
    return json.dumps(data).encode()


def deserialize_rle(data):
    return json.loads(data.decode())


def serialize_lzw(data):
    return json.dumps(data).encode()


def deserialize_lzw(data):
    return json.loads(data.decode())


# =====================================================
# MAIN
# =====================================================

if uploaded_file:

    original_bytes = uploaded_file.read()

    safe_text = bytes_to_text(original_bytes)

    original_bits = len(original_bytes) * 8

    st.subheader("📄 File Information")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Filename", uploaded_file.name)

    with c2:
        st.metric("Original Size", f"{len(original_bytes)} bytes")

    with c3:
        st.metric("Original Bits", original_bits)

    st.info(
        f"Detected file type: {uploaded_file.type}"
    )

    # =====================================================
    # EXECUTE
    # =====================================================

    if st.button("🚀 Execute"):

        # =====================================================
        # COMPRESS
        # =====================================================

        if mode == "Compress":

            # =========================
            # HUFFMAN
            # =========================

            if algorithm == "Huffman":

                compressed, root, overhead, t = huffman_compress(safe_text)

                compressed_bits = len(compressed) + overhead

                payload = {
                    "algorithm": "Huffman",
                    "data": compressed
                }

                output_data = json.dumps(payload).encode()

                extension = ".huff"

            # =========================
            # RLE
            # =========================

            elif algorithm == "RLE":

                compressed, t = rle_compress(safe_text)

                compressed_bits = 0

                for count, _ in compressed:
                    compressed_bits += (
                        math.ceil(math.log2(count + 1)) + 8
                    )

                payload = {
                    "algorithm": "RLE",
                    "data": compressed
                }

                output_data = json.dumps(payload).encode()

                extension = ".rle"

            # =========================
            # LZW
            # =========================

            elif algorithm == "LZW":

                compressed, dict_size, t = lzw_compress(safe_text)

                bits = math.ceil(math.log2(dict_size))

                compressed_bits = len(compressed) * bits

                payload = {
                    "algorithm": "LZW",
                    "data": compressed
                }

                output_data = json.dumps(payload).encode()

                extension = ".lzw"

            # =========================
            # RESULT
            # =========================

            ratio = compressed_bits / max(original_bits, 1)

            saving = (1 - ratio) * 100

            st.subheader("📊 Compression Result")

            r1, r2, r3 = st.columns(3)

            with r1:
                st.metric(
                    "Compression Ratio",
                    f"{ratio:.3f}"
                )

            with r2:
                st.metric(
                    "Saving",
                    f"{saving:.2f}%"
                )

            with r3:
                st.metric(
                    "Execution Time",
                    f"{t:.6f}s"
                )

            # =========================
            # CHART
            # =========================

            df = pd.DataFrame({
                "Type": ["Original", "Compressed"],
                "Bits": [original_bits, compressed_bits]
            })

            fig, ax = plt.subplots()

            ax.bar(df["Type"], df["Bits"])

            ax.set_ylabel("Bits")

            st.pyplot(fig)

            # =========================
            # DOWNLOAD
            # =========================

            st.download_button(
                label="⬇️ Download Compressed File",
                data=output_data,
                file_name=uploaded_file.name + extension,
                mime="application/octet-stream"
            )

        # =====================================================
        # DECOMPRESS
        # =====================================================

        else:

            try:

                payload = json.loads(original_bytes.decode())

                alg = payload["algorithm"]

                compressed_data = payload["data"]

                # =========================
                # RLE
                # =========================

                if alg == "RLE":

                    decompressed_text, t = rle_decompress(
                        compressed_data
                    )

                # =========================
                # LZW
                # =========================

                elif alg == "LZW":

                    decompressed_text, t = lzw_decompress(
                        compressed_data
                    )

                # =========================
                # HUFFMAN
                # =========================

                elif alg == "Huffman":

                    st.error(
                        "Huffman decompression cần Huffman Tree để giải nén."
                    )

                    st.stop()

                restored_bytes = text_to_bytes(
                    decompressed_text
                )

                st.success("✅ Decompression successful")

                st.metric(
                    "Recovered Size",
                    f"{len(restored_bytes)} bytes"
                )

                # preview text files only
                try:
                    preview = restored_bytes.decode("utf-8")

                    st.text_area(
                        "Preview",
                        preview[:3000],
                        height=200
                    )

                except:
                    st.info(
                        "Binary/non-text file preview unavailable"
                    )

                # =========================
                # DOWNLOAD
                # =========================

                original_name = uploaded_file.name

                if "." in original_name:
                    original_name = original_name.rsplit(".", 1)[0]

                st.download_button(
                    label="⬇️ Download Restored File",
                    data=restored_bytes,
                    file_name=f"restored_{original_name}",
                    mime="application/octet-stream"
                )

            except Exception as e:
                st.error(f"Error: {e}")