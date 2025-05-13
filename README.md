# Motion Tracking in Drone Videos using FAST and ORB

**Team:**
- KRISHNA RAJEEV  
- ADITHYA S KUMAR  
- ADIN REJO R  
- ASWIN S

---

## Description
This project implements a real-time motion tracking pipeline for drone-captured videos using OpenCV. We combine FAST keypoint detection, ORB descriptors, and Lucas–Kanade optical flow to extract and visualize movement trajectories across frames. A Streamlit interface allows easy uploading, processing, and download of the tracked output.

## Repository Structure
```
├── motion_tracking.py    # Core tracking module
├── app.py                # Streamlit web app
├── requirements.txt      # Python dependencies
└── README.md             # Project overview and instructions
```

## requirements.txt
```text
opencv-python>=4.5.0
numpy>=1.19.0
streamlit>=1.0.0
```

Install dependencies with:
```bash
pip install -r requirements.txt
```

## How It Works
1. **Frame Extraction**: Read and resize each video frame to a fixed resolution.  
2. **Feature Detection**: Use FAST to detect interest points on the first frame.  
3. **Descriptor Computation**: Compute ORB descriptors for each keypoint (optional extension).  
4. **Optical Flow Tracking**: Track detected points across subsequent frames using Lucas–Kanade.  
5. **Trajectory Drawing**: Draw lines and circles to visualize motion paths.  
6. **Output Video**: Save processed frames to a new video file.

## Data
https://drive.google.com/file/d/1UiU-GxPrQQqouLaBVd7R9hOtMwka11gM/view

## How to Run

### 1. Core Tracking Script
```bash
python motion_tracking.py --input path/to/drone_video.mp4 --output tracked_output.mp4
```
- `--input`: Path to the source drone video.  
- `--output`: Path where the processed video with motion tracks will be saved.

### 2. Streamlit Web App
```bash
streamlit run app.py
```
1. Open the generated localhost URL in your browser.  
2. Upload an `.mp4`, `.avi`, `.mov`, or `.mpeg4` video.  
3. Click **Run Motion Tracking**.  
4. Preview original and tracked videos side by side.  
5. Download the processed output.

## Typical Usage
1. Capture video with a drone-mounted camera.  
2. Clone this repository:  
   ```bash  
   git clone https://github.com/yourusername/motion-tracking-drone.git  
   cd motion-tracking-drone  
   ```  
3. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
4. Process via CLI or web app as described above.  

---

## License
This project is released under the MIT License.
