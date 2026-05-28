```markdown
# Local Edge AI Projects 🤖🏠

A collection of lightweight, real-time Edge AI applications designed to run efficiently on standard Windows laptops using a webcam. This repository demonstrates practical implementations of Object Detection, Computer Vision, and Real-time Human-Computer Interaction (HCI).

> ⚠️ **Operating System Note:** These projects utilize Windows-specific system APIs (`winsound`, `pycaw`, `comtypes`) and are designed to run on **Windows OS**.

---

## 📁 Repository Structure

```text
├── Cheating-Detection/
│   ├── ai_alarm.mp4              # Demo video of the cheating detection system
│   └── cheating-detection.py     # Source code for YOLOv11-based anti-cheating system
├── Volume-Control/
│   ├── volume_control.mp4         # Demo video of hand gesture volume control
│   └── volume_control.py          # Source code for MediaPipe volume controller
└── README.md                      # Project documentation (this file)

```

---

## 🛠️ Project 1: AI Cheating Detection & Evidence Collector

**Directory:** `Cheating-Detection/`

This application turns a standard webcam into an automated anti-cheating proctoring tool. Using the state-of-the-art **YOLOv11** object detection model, the system scans the camera feed for unauthorized items (like cell phones or remotes), triggers an audio alarm, and automatically takes snapshots of the violation.

### 🚀 Key Features & Logic:

* **Real-time Object Detection:** Leverages `yolo11s.pt` (via `ultralytics`) to monitor and identify target objects with low latency.
* **Hardware Alert & On-Screen UI:** Uses Windows native `winsound.Beep` to trigger an instant audio alarm and overlays a red warning banner ("DA CHUP ANH BANG CHUNG!") on the video stream.
* **Smart Evidence Capture:** Automatically creates a `canh_bao/` directory and saves evidence photos (`.jpg`) timestamped via Python's `time` module.
* **Anti-Flood Cooldown:** Implements a strict **2-second cooldown interval** between snapshots to prevent flooding the storage with duplicate alerts.

---

## 🖐️ Project 2: Hand Gesture Volume Control

**Directory:** `Volume-Control/`

An interactive Computer Vision application that transforms your laptop's webcam into a gesture sensor, allowing you to seamlessly control the Windows master volume using hand movements.

### 🚀 Key Features & Logic:

* **Hand Landmarks Tracking:** Utilizes Google's **MediaPipe Hands** solution configured for single-hand tracking with a high detection confidence (`0.7`).
* **Mathematical Mapping:** * Tracks coordinates for the **Thumb tip (ID 4)** and **Index finger tip (ID 8)**.
* Calculates the Euclidean distance between them using `math.hypot`.
* Maps pixel distance ranges `[50, 200]` directly into the Windows native decibel range using `numpy.interp`.


* **Direct Audio Interaction:** Hooks directly into the Windows Core Audio API via `pycaw` and `comtypes` to control the master volume slider.
* **Visual Status Feedback:** Draws interactive trackers on screen, turning the center indicator **green** when the fingers pinch together (`< 50` distance) signifying minimum volume/mute.

---

## ⚙️ How to Customize Parameters

You can easily tweak both applications by modifying specific variables inside the source code to match your environment:

### 1. Modifying the Cheating Detector (`cheating-detection.py`)

* **Change Target Objects:** Look for `if name in ['cell phone', 'remote']:` and add or swap with any standard YOLO COCO classes (e.g., `['book', 'laptop']` to detect hidden materials).
* **Adjust Sensitivity:** Change the `conf=0.25` value inside `model(frame, conf=0.25)`. Raise it higher (e.g., `0.50`) to avoid false alarms, or lower it if the camera struggles to catch the object.
* **Change Snapshot Frequency:** Modify the number `2` in `if current_time - last_saved_time > 2:` to change the interval (in seconds) before taking another evidence photo.

### 2. Modifying the Volume Controller (`volume-control.py`)

* **Calibrate Hand Distance:** Find `np.interp(length, [50, 200], [min_vol, max_vol])`. If your hand is far from the camera, you might want to adjust the pixel range `[50, 200]` to something like `[30, 120]` for smoother control.
* **Tweak the Mute Visual Trigger:** Change the threshold in `if length < 50:` to match the minimum thumb-to-index distance set in your interpolation function.

---

## 💻 Environment & Installation

Since these are **Edge AI** projects, they are highly optimized to run locally on an everyday office laptop without needing an expensive dedicated GPU.

### Prerequisites

* Windows OS
* Python 3.8+

### Installation Steps

1. **Clone the repository:**
```bash
git clone [https://github.com/donglearning-pro/Edge-AI.git](https://github.com/donglearning-pro/Edge-AI.git)
cd Edge-AI

```


2. **Install the exact required dependencies:**
```bash
pip install opencv-python ultralytics mediapipe numpy comtypes==1.1.14 pycaw==20181226

```


3. **Run the AI Cheating Detection:**
```bash
cd Cheating-Detection
python cheating-detection.py

```


4. **Run the Hand Gesture Volume Control:**
```bash
cd Volume-Control
python volume_control.py

```



---

## 📈 Key Takeaways & Journey

* **Edge AI Deployment:** Learned how to deploy modern neural networks (`YOLOv11`) and geometric tracking models (`MediaPipe`) in production environments with strict CPU limits.
* **System-level Programming:** Gained practical experience interacting with internal Windows OS sound components through COM interfaces.
* **Logic & UI Design:** Solved real-time UI synchronization challenges, such as implementing cool-down logic for data logging and giving dynamic visual feedback via OpenCV graphics.
