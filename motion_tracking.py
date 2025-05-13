import cv2
import numpy as np

class MotionTracker:
    def __init__(self, resize_width=640, resize_height=480):
        self.fast = cv2.FastFeatureDetector_create()
        self.orb = cv2.ORB_create()
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.resize_dim = (resize_width, resize_height)

    def process(self, input_path, output_path, fps=20):
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise IOError("Cannot open video file")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, self.resize_dim)

        ret, prev_frame = cap.read()
        if not ret:
            raise IOError("Cannot read video frame or file is empty.")
        prev_frame = cv2.resize(prev_frame, self.resize_dim)
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        prev_kps = self.fast.detect(prev_gray, None)
        if not prev_kps:
            raise RuntimeError("No FAST keypoints in first frame.")
        prev_pts = np.array([kp.pt for kp in prev_kps], dtype=np.float32).reshape(-1, 1, 2)

        mask = np.zeros_like(prev_frame)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, self.resize_dim)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev_pts is None or len(prev_pts) == 0:
                kps = self.fast.detect(prev_gray, None)
                if kps:
                    prev_pts = np.array([kp.pt for kp in kps], dtype=np.float32).reshape(-1,1,2)
                else:
                    prev_gray = gray.copy()
                    continue

            next_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_pts, None, **self.lk_params)
            if next_pts is None or status is None:
                prev_gray = gray.copy()
                continue

            good_new = next_pts[status.flatten()==1]
            good_old = prev_pts[status.flatten()==1]

            for new, old in zip(good_new, good_old):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0,255,0), 2)
                frame = cv2.circle(frame, (int(a), int(b)), 3, (0,0,255), -1)

            output = cv2.add(frame, mask)
            out.write(output)

            prev_gray = gray.copy()
            prev_pts = good_new.reshape(-1,1,2)

        cap.release()
        out.release()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Drone Video Motion Tracker")
    parser.add_argument("--input", required=True, help="Path to input video")
    parser.add_argument("--output", required=True, help="Path to save output video")
    args = parser.parse_args()
    tracker = MotionTracker()
    tracker.process(args.input, args.output)