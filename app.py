import streamlit as st
from ultralytics import YOLO
from PIL import Image
from collections import Counter
import io

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Object Detection",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------------------------
# LOAD YOLO MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🎯 AI Object Detection System")
st.markdown(
    """
    <div style="
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    ">
        <h1>🎯 AI Object Detection System</h1>
        <p style="font-size:20px;">
            Intelligent object detection powered by YOLOv8
        </p>
        <p>
            Upload an image or use your camera to detect objects
            using deep learning.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# TECHNOLOGY INFO
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.info("🤖 Model: YOLOv8")

with col2:
    st.info("🧠 Framework: Ultralytics")

with col3:
    st.info("🐍 Interface: Streamlit")

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------
st.subheader("📥 Choose Input Method")

input_method = st.radio(
    "Select an option:",
    ["📁 Upload Image", "📷 Use Camera"],
    horizontal=True
)

confidence = st.slider(
    "🎚️ Detection Confidence",
    min_value=0.1,
    max_value=1.0,
    value=0.5,
    step=0.05
)

uploaded_file = None

if input_method == "📁 Upload Image":
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

else:
    uploaded_file = st.camera_input(
        "Take a picture"
    )

# --------------------------------------------------
# DETECTION
# --------------------------------------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.divider()

    # Run detection
    with st.spinner("🔍 AI is detecting objects..."):
        results = model(image, conf=confidence)

    result_image = results[0].plot()

    # --------------------------------------------------
    # IMAGE DISPLAY
    # --------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Original Image")
        st.image(
            image,
            use_container_width=True
        )

    with col2:
        st.subheader("🔍 Detection Result")
        st.image(
            result_image,
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # DETECTION SUMMARY
    # --------------------------------------------------
    st.subheader("📊 Detection Results")

    detected_objects = []

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        detected_objects.append(class_name)

    if detected_objects:

        object_counts = Counter(detected_objects)

        # Statistics
        total_objects = len(detected_objects)
        unique_objects = len(object_counts)

        stat1, stat2 = st.columns(2)

        with stat1:
            st.metric(
                "Total Objects Detected",
                total_objects
            )

        with stat2:
            st.metric(
                "Unique Object Types",
                unique_objects
            )

        st.success(
            f"Successfully detected {total_objects} object(s)!"
        )

        # Object list
        st.markdown("### 🏷️ Detected Objects")

        for object_name, count in object_counts.items():
            st.write(
                f"🔹 **{object_name.title()}**: {count}"
            )

    else:
        st.warning(
            "No objects detected. Try lowering the confidence level."
        )

    st.divider()

    # --------------------------------------------------
    # DOWNLOAD RESULT
    # --------------------------------------------------
    st.subheader("📥 Download Result")

    result_pil = Image.fromarray(result_image)

    buffer = io.BytesIO()
    result_pil.save(buffer, format="PNG")

    st.download_button(
        label="⬇️ Download Detection Result",
        data=buffer.getvalue(),
        file_name="yolo_detection_result.png",
        mime="image/png",
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.markdown(
    """
    ### 👩‍💻 About This Project

    This AI-powered Object Detection System uses the YOLOv8 deep learning
    model to identify and classify multiple objects from uploaded images
    or live camera input.

    **Technologies Used:**
    Python • YOLOv8 • Ultralytics • OpenCV • Streamlit
    """
)