#### app.py (Streamlit Interface)
import streamlit as st
import tempfile
import os
from motion_tracking import MotionTracker

st.title("Drone Video Motion Tracking")
st.write("Upload a drone video and visualize motion tracks using FAST + ORB + Optical Flow.")

# Allow all uploads, then manually validate extension
uploaded_file = st.file_uploader("Choose a video file")
if uploaded_file:
    _, ext = os.path.splitext(uploaded_file.name)
    allowed_ext = ['.mp4', '.avi', '.mov', '.mpeg4']
    if ext.lower() not in allowed_ext:
        st.error(f"Unsupported file type: {ext}. Allowed types: {', '.join(allowed_ext)}")
    else:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        tfile.write(uploaded_file.read())
        input_path = tfile.name
        output_path = input_path.replace(ext, f"_tracked{ext}")

        if st.button("Run Motion Tracking"):
            try:
                tracker = MotionTracker()
                tracker.process(input_path, output_path)
                st.video(input_path)
                st.video(output_path)
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label="Download Tracked Video",
                        data=f,
                        file_name=os.path.basename(output_path),
                        mime=f"video/{ext.lower().strip('.') }"
                    )
            except Exception as e:
                st.error(f"Error during processing: {e}")