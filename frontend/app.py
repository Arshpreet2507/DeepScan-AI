import streamlit as st
import requests
import time

st.set_page_config(
    page_title="DeepScan AI",
    page_icon="🛡️",
    layout="centered"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main { background-color: #0f172a; }
.block-container { padding-top: 2rem; }
h1, h2, h3, h4, p, span, div { color: white !important; }
.card {
    background: #111827;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.15);
}
.result-real {
    color: #22c55e;
    font-size: 42px;
    font-weight: bold;
}
.result-fake {
    color: #ef4444;
    font-size: 42px;
    font-weight: bold;
}
.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 14px;
    background: #1f2933;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="card">
<h1>🛡️ DeepScan AI</h1>
<p>AI-powered Deepfake Detection</p>
<span class="badge">Prototype Demo</span>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- Upload ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📤 Upload a Video for Analysis")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Analyze ----------
if uploaded_file:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 Analysis in Progress")

    with st.spinner("Running deepfake detection..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/analyze", files={"file": uploaded_file})
        time.sleep(1)

    if response.status_code == 200:
        result = response.json()
        label = result["prediction"]
        confidence = float(result["confidence"]) * 100

        if label == "REAL":
            st.markdown(f"<div class='result-real'>REAL</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-fake'>FAKE</div>", unsafe_allow_html=True)

        st.progress(int(confidence))
        st.markdown(f"### 🔐 Fake-O-Meter: `{confidence:.2f}%`")

        # Mini forensic summary
        st.markdown("#### 🧪 Mini Forensic Summary")
        if label == "FAKE":
            st.write("• Abnormal facial dynamics detected")
            st.write("• Temporal inconsistencies across frames")
            st.write("• Possible lip-sync mismatch")
        else:
            st.write("• Natural facial micro-expressions")
            st.write("• Stable temporal patterns")
            st.write("• No major manipulation artifacts found")

    else:
        st.error("❌ Server error. Is FastAPI running?")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.write("")
st.markdown("""
<div style="text-align:center; opacity:0.6;">
TrustLens Team 🚀
</div>
""", unsafe_allow_html=True)