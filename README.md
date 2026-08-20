````markdown
# 📹 Industrial Video Monitoring & Tracking System — Week 3

An end-to-end industrial video monitoring pipeline for object detection, multi-object tracking, database persistence, Linux automation, anomaly detection, and web-based status monitoring.

The system uses **YOLOv8** for object detection, **ByteTrack** for multi-object tracking, **OpenCV** for video processing, **MySQL** for persistent detection storage, **Linux cron + Bash** for automated video processing, **FastAPI** for the backend API, and **Next.js** for the monitoring dashboard.

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Objectives](#-objectives)
3. [Industrial Use Case](#-industrial-use-case)
4. [Key Features](#-key-features)
5. [System Architecture](#-system-architecture)
6. [Project Structure](#-project-structure)
7. [Technology Stack](#-technology-stack)
8. [Database Design](#-database-design)
9. [Installation and Setup](#-installation-and-setup)
10. [Environment Configuration](#-environment-configuration)
11. [Running the System](#-running-the-system)
12. [Automated Video Processing](#-automated-video-processing)
13. [FastAPI Backend](#-fastapi-backend)
14. [Next.js Status Dashboard](#-nextjs-status-dashboard)
15. [Logging](#-logging)
16. [Speed and Anomaly Detection](#-speed-and-anomaly-detection)
17. [Verification and Testing](#-verification-and-testing)
18. [Definition of Done](#-definition-of-done)
19. [Git Versioning](#-git-versioning)
20. [Project Status](#-project-status)

---

## 🎯 Project Overview

This project implements an automated industrial video monitoring pipeline capable of processing video files, detecting objects, tracking them across frames, calculating relative movement speed, storing detection results in MySQL, and presenting system statistics through a web dashboard.

The system is designed around a complete processing workflow:

```text
Video Input
    ↓
Linux Watcher / Cron
    ↓
YOLOv8 Object Detection
    ↓
ByteTrack Multi-Object Tracking
    ↓
Speed Calculation
    ↓
Anomaly Detection
    ↓
MySQL Database
    ↓
FastAPI Backend
    ↓
Next.js Monitoring Dashboard
````

The implementation is designed for short and low-resolution video clips so that the processing pipeline can run comfortably on a CPU-based Linux/WSL environment.

---

## 🎯 Objectives

The main objectives of Week 3 are:

* Process video files using OpenCV.
* Detect objects using a pretrained YOLOv8 model.
* Track detected objects across video frames using ByteTrack.
* Assign tracking IDs to detected objects.
* Calculate relative movement speed in pixels per frame.
* Identify abnormal movement using a configurable speed threshold.
* Store detection and tracking information in MySQL.
* Automatically process newly added videos using a Bash watcher.
* Schedule automatic processing using Linux cron.
* Generate timestamped application and automation logs.
* Provide a FastAPI backend for database access.
* Display live monitoring statistics through a Next.js dashboard.
* Verify the complete end-to-end pipeline.

---

## 🏭 Industrial Use Case

### Conveyor and Line Monitoring

The system can be applied to industrial environments where objects need to be detected and tracked across a monitored area.

A typical workflow is:

1. A video file is placed inside the input directory.
2. The watcher detects the new video.
3. The video is passed to the monitoring pipeline.
4. YOLOv8 detects supported objects.
5. ByteTrack assigns tracking IDs.
6. Object movement is measured between consecutive frames.
7. Detection information is stored in MySQL.
8. Potential speed anomalies are flagged.
9. An annotated output video is generated.
10. The dashboard retrieves the latest statistics through FastAPI.

### Example Applications

* 🏭 Manufacturing line monitoring
* 📦 Conveyor belt monitoring
* 🚗 Traffic and vehicle monitoring
* 👷 Industrial area monitoring
* 📊 Production-line analytics
* ⚠️ Movement and speed anomaly detection

> **Important:** The current implementation calculates relative speed in **pixels per frame (px/frame)**. It does not represent physical speed such as km/h. Real-world speed measurement would require camera calibration and a known physical scale.

---

## ✨ Key Features

### Computer Vision

* YOLOv8 pretrained object detection.
* OpenCV video processing.
* Bounding-box visualization.
* Configurable confidence threshold.

### Object Tracking

* ByteTrack multi-object tracking.
* Tracking IDs assigned to detected objects.
* Previous bounding boxes maintained for movement calculation.

### Speed Analysis

* Relative object movement calculated in pixels/frame.
* Configurable anomaly threshold.
* Anomalous detections marked in the database.
* Anomalies exposed through the API and dashboard.

### Database

* MySQL persistence.
* Detection records stored for every tracked detection.
* Video filename stored with each detection.
* Indexed database fields for common queries.
* Batch insertion of detection records to reduce database write overhead.

### Automation

* Bash-based video watcher.
* Duplicate processing prevention.
* Linux cron scheduling.
* Automated logging of watcher activity.

### Backend

* FastAPI REST API.
* MySQL-backed status endpoints.
* Separate endpoints for overall status, processed videos, and anomalies.

### Frontend

* Next.js dashboard.
* Live database statistics.
* Processed video summary.
* Unique tracked object count.
* Speed anomaly section.
* Automatic refresh every 5 seconds.
* Manual refresh button.

### Security

* Database credentials loaded through environment variables.
* `.env` excluded from version control.
* Sensitive credentials are not hard-coded into the repository.

---

## 🏗️ System Architecture

```text
┌───────────────────────────────┐
│       Input Video (.mp4)      │
│        input_videos/           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Linux Cron Scheduler     │
│             ↓                 │
│         watcher.sh            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       monitor.py              │
│                               │
│   YOLOv8 Detection             │
│            +                  │
│   ByteTrack Tracking            │
│            +                  │
│   Speed / Anomaly Analysis     │
└───────────────┬───────────────┘
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
┌───────────────┐  ┌──────────────────┐
│ Output Video  │  │   MySQL Database │
│ output_videos │  │ ppe_monitoring_db│
└───────────────┘  └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ FastAPI Backend  │
                   │      :8000       │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Next.js Dashboard│
                   │      :3000       │
                   └──────────────────┘
```

---

## 📁 Project Structure

```text
week3-video-monitor/
│
├── input_videos/
│   └── # Input video files
│
├── output_videos/
│   └── # Annotated processed videos
│
├── logs/
│   ├── monitor.log
│   ├── cron.log
│   └── processed_files.txt
│
├── db/
│   └── schema.sql
│
├── status_api/
│   └── main.py
│
├── status_ui/
│   ├── app/
│   │   └── page.tsx
│   ├── package.json
│   └── ...
│
├── monitor.py
├── watcher.sh
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

### Main Components

| Component            | Purpose                                                                                            |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| `monitor.py`         | Core YOLOv8 detection, ByteTrack tracking, speed calculation, anomaly detection, and MySQL logging |
| `watcher.sh`         | Detects new video files and launches the monitoring pipeline                                       |
| `db/schema.sql`      | Defines the MySQL database and detection table                                                     |
| `status_api/main.py` | FastAPI backend that exposes database information                                                  |
| `status_ui/`         | Next.js monitoring dashboard                                                                       |
| `input_videos/`      | Directory for incoming video files                                                                 |
| `output_videos/`     | Directory for annotated output videos                                                              |
| `logs/`              | Application and automation logs                                                                    |
| `.env`               | Local database configuration and credentials                                                       |
| `requirements.txt`   | Python dependencies                                                                                |

> The `.env` file is a local configuration file and must not be committed to Git.

---

## 🛠️ Technology Stack

| Technology               | Purpose                        |
| ------------------------ | ------------------------------ |
| Python 3.11+             | Core programming language      |
| YOLOv8                   | Object detection               |
| ByteTrack                | Multi-object tracking          |
| Ultralytics              | YOLOv8 implementation          |
| OpenCV                   | Video reading and writing      |
| MySQL                    | Detection data persistence     |
| `mysql-connector-python` | Python/MySQL connectivity      |
| FastAPI                  | Backend REST API               |
| Uvicorn                  | FastAPI application server     |
| Next.js                  | Monitoring dashboard           |
| TypeScript               | Frontend development           |
| Tailwind CSS             | Dashboard styling              |
| Bash                     | Automation watcher             |
| Linux cron               | Scheduled execution            |
| Git                      | Version control                |
| Python `argparse`        | Command-line configuration     |
| Python `logging`         | Structured application logging |
| `python-dotenv`          | Environment variable loading   |

---

## 🗄️ Database Design

### Database

```sql
CREATE DATABASE IF NOT EXISTS ppe_monitoring_db;
USE ppe_monitoring_db;
```

### Detections Table

```sql
CREATE TABLE IF NOT EXISTS detections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    frame_number INT NOT NULL,
    timestamp DATETIME NOT NULL,
    video_name VARCHAR(255) NOT NULL,
    object_id INT NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    x1 FLOAT NOT NULL,
    y1 FLOAT NOT NULL,
    x2 FLOAT NOT NULL,
    y2 FLOAT NOT NULL,
    speed FLOAT DEFAULT 0.0,
    is_anomaly BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_video_name (video_name),
    INDEX idx_object_id (object_id),
    INDEX idx_is_anomaly (is_anomaly)
);
```

### Stored Information

| Field                  | Description                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| `id`                   | Unique database record ID                                        |
| `frame_number`         | Video frame number                                               |
| `timestamp`            | Relative video timestamp                                         |
| `video_name`           | Source video filename                                            |
| `object_id`            | ByteTrack object ID                                              |
| `class_name`           | Detected object class                                            |
| `confidence`           | YOLO detection confidence                                        |
| `x1`, `y1`, `x2`, `y2` | Bounding-box coordinates                                         |
| `speed`                | Relative movement in pixels/frame                                |
| `is_anomaly`           | Indicates whether the movement exceeded the configured threshold |
| `created_at`           | Database insertion timestamp                                     |

---

## ⚙️ Installation and Setup

### 1. Prerequisites

Install the following software:

* Python 3.11+
* Node.js 20+
* npm
* MySQL Server
* Linux or WSL
* Git

Verify the environment:

```bash
python3 --version
node --version
npm --version
mysql --version
git --version
```

---

### 2. Clone the Repository

```bash
git clone <repository-url>
cd week3-video-monitor
```

---

### 3. Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 5. Initialize MySQL

The project includes the database schema in:

```text
db/schema.sql
```

Run:

```bash
mysql -u root -p < db/schema.sql
```

The schema creates the database and the `detections` table if they do not already exist.

---

### 6. Create the Database User

The application expects a dedicated MySQL user.

Example:

```sql
CREATE USER 'monitor_user'@'localhost'
IDENTIFIED BY 'your_mysql_password';

GRANT ALL PRIVILEGES
ON ppe_monitoring_db.*
TO 'monitor_user'@'localhost';

FLUSH PRIVILEGES;
```

Use your own secure password.

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=monitor_user
DB_PASSWORD=your_mysql_password
DB_NAME=ppe_monitoring_db
```

The application loads these values using `python-dotenv`.

### Security

Never commit `.env` to Git.

The repository should exclude sensitive configuration such as:

```text
.env
venv/
__pycache__/
*.log
yolov8n.pt
input_videos/
output_videos/
status_ui/node_modules/
```

---

## 🚀 Running the System

### 1. Process a Video Manually

Place a supported video inside:

```text
input_videos/
```

Run:

```bash
python monitor.py \
    --input input_videos/test_video_v3.mp4 \
    --output output_videos/day3_final_test.mp4 \
    --threshold 0.35
```

Available arguments:

```text
--input       Path to the input video
--output      Path to the processed output video
--threshold   YOLO confidence threshold
```

Example:

```bash
python monitor.py \
    --input input_videos/test_video_v3.mp4 \
    --threshold 0.35
```

The pipeline generates an annotated video containing:

* Bounding boxes
* Object classes
* Tracking IDs
* Confidence scores
* Relative speed

---

## 🤖 Automated Video Processing

The project includes:

```text
watcher.sh
```

The watcher monitors the input directory and processes newly detected video files.

### Make the watcher executable

```bash
chmod +x watcher.sh
```

### Run the watcher manually

```bash
./watcher.sh
```

The watcher maintains:

```text
logs/processed_files.txt
```

to prevent already processed files from being processed again.

Example watcher output:

```text
🚀 [Watcher] New video detected: test_video_v3.mp4.
Starting monitor pipeline...

✅ [Watcher] Successfully processed and recorded:
test_video_v3.mp4

⏭️ [Watcher] Skipping already processed file:
test_video_v3.mp4
```

---

## ⏰ Linux Cron Automation

The watcher is scheduled through Linux `cron`.

Check the configured cron jobs:

```bash
crontab -l
```

Example:

```cron
* * * * * /home/user-rn/week3-video-monitor/watcher.sh >> /home/user-rn/week3-video-monitor/logs/cron.log 2>&1
```

This configuration executes the watcher every minute.

The cron output is stored in:

```text
logs/cron.log
```

---

## 🚀 FastAPI Backend

The project provides a FastAPI backend that reads monitoring information from MySQL.

Start the API:

```bash
source venv/bin/activate

python -m uvicorn status_api.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
```

The API runs on:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## 🌐 API Endpoints

### `GET /`

Checks whether the backend is online.

Example response:

```json
{
  "status": "online"
}
```

---

### `GET /api/status`

Returns overall system statistics.

Example:

```json
{
  "total_detections": 2060,
  "unique_objects": 26,
  "total_videos": 2,
  "last_video": "test_video_v3.mp4",
  "last_processed_at": "2026-08-10 11:24:11"
}
```

The endpoint provides:

* Total detections
* Unique tracked objects
* Number of processed videos
* Latest processed video
* Latest processing timestamp

---

### `GET /api/videos`

Returns a summary for each processed video.

Information includes:

* Video name
* Number of detections
* Number of unique objects
* Number of anomalies
* Processing timestamp

---

### `GET /api/anomalies`

Returns detected speed anomalies.

The endpoint supports a configurable limit:

```text
/api/anomalies?limit=20
```

---

## 🖥️ Next.js Status Dashboard

The project includes a Next.js dashboard for monitoring the database through the FastAPI backend.

Start the frontend:

```bash
cd status_ui
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

### Dashboard Features

The dashboard displays:

* 📊 Total detections
* 🆔 Unique tracked objects
* 🎞️ Number of processed videos
* 🎥 Latest processed video
* 📋 Processed video summary
* ⚠️ Speed anomalies
* 🕒 Processing timestamps

### Automatic Refresh

The dashboard automatically refreshes its data every **5 seconds**.

A `LIVE (Auto 5s)` indicator shows that the dashboard is periodically retrieving updated information.

A manual **Refresh** button is also available.

---

## 📝 Logging

The project uses Python's `logging` module for application-level logging.

### Application Log

```text
logs/monitor.log
```

Contains timestamped events such as:

```text
2026-08-10 11:23:53 | INFO    | Starting Video Monitor Pipeline for: test_video_v3.mp4
2026-08-10 11:23:53 | INFO    | Loading YOLOv8 Tracking Model (yolov8n.pt)...
2026-08-10 11:23:53 | INFO    | Connected successfully to MySQL DB
2026-08-10 11:24:11 | INFO    | Processing finished successfully.
2026-08-10 11:24:11 | INFO    | Annotated output video saved
2026-08-10 11:24:11 | INFO    | MySQL Connection closed safely.
```

### Cron Log

```text
logs/cron.log
```

Contains watcher and cron execution information.

### Processed Files

```text
logs/processed_files.txt
```

Stores the names of videos that have already been processed to prevent duplicate execution.

---

## ⚡ Speed and Anomaly Detection

The system calculates relative movement between the centers of consecutive bounding boxes.

The distance is calculated as:

```text
distance =
sqrt(
    (current_x - previous_x)^2 +
    (current_y - previous_y)^2
)
```

The resulting value represents relative movement in:

```text
pixels/frame
```

The current anomaly threshold is:

```python
SPEED_ANOMALY_THRESHOLD = 70.0
```

An object is marked as anomalous when:

```text
speed > 70.0 px/frame
```

Anomalous detections are:

* Stored in MySQL.
* Marked using `is_anomaly`.
* Exposed through `/api/anomalies`.
* Displayed in the dashboard.

> The threshold is an application-level relative movement threshold and is not a physical velocity measurement.

---

## 🔄 Object Tracking

The system uses:

```text
YOLOv8 + ByteTrack
```

The tracker is initialized through Ultralytics using:

```python
model.track(
    frame,
    persist=True,
    conf=args.threshold,
    tracker="bytetrack.yaml",
    verbose=False
)
```

The `persist=True` configuration allows tracking information to be maintained between processed frames.

Each detected object receives a tracking ID which is stored in:

```text
object_id
```

The system also maintains the previous bounding box for each active tracking ID in memory to calculate relative movement.

---

## 📦 Database Batch Insertion

Detection records are accumulated before being written to MySQL.

The application uses a batch size of:

```python
BATCH_SIZE = 100
```

This means detection records are inserted in batches rather than opening a separate database transaction for every individual detection.

This reduces the frequency of database writes during video processing.

---

## 🧪 Verification and Testing

The complete pipeline was tested using video files processed through the system.

### Video Processing Test

A test video was successfully processed with:

```text
Input:
input_videos/test_video_v3.mp4

Frames processed:
647

Output:
output_videos/day3_final_test.mp4
```

The processing completed successfully without stopping.

---

### Database Verification

The MySQL database was queried to verify stored detection records.

Example:

```bash
mysql -u monitor_user -p -e \
"USE ppe_monitoring_db;
 SELECT video_name,
        COUNT(*) AS total_detections,
        COUNT(DISTINCT object_id) AS unique_objects
 FROM detections
 GROUP BY video_name;"
```

The database successfully stored detection records grouped by video name.

---

### Cron Verification

The cron configuration was verified using:

```bash
crontab -l
```

The watcher successfully detected new video files and skipped files already listed in:

```text
logs/processed_files.txt
```

---

### API Verification

The FastAPI endpoint was tested using:

```bash
curl http://127.0.0.1:8000/api/status
```

The API returned valid JSON containing:

* Total detections
* Unique objects
* Number of videos
* Latest processed video
* Latest processing time

---

### Dashboard Verification

The Next.js dashboard was verified at:

```text
http://localhost:3000
```

The dashboard successfully displayed:

* Detection counts
* Unique tracked objects
* Processed videos
* Latest processed video
* Anomaly count
* Processing timestamps

The dashboard also successfully retrieved data through the FastAPI endpoints.

---

## ✅ Definition of Done

The Week 3 requirements were verified as follows:

* [x] System processes a complete video clip without stopping.
* [x] YOLOv8 object detection is integrated.
* [x] ByteTrack multi-object tracking is integrated.
* [x] Tracking IDs are stored with detection records.
* [x] Relative speed is calculated in pixels/frame.
* [x] Speed anomalies are identified using a configurable threshold.
* [x] Detection results are persisted in MySQL.
* [x] Video filenames are stored with detection records.
* [x] Database schema is documented.
* [x] Detection records are inserted in batches.
* [x] `watcher.sh` automatically detects new video files.
* [x] Duplicate processing is prevented using `processed_files.txt`.
* [x] Linux cron automation is configured.
* [x] Timestamped application logs are generated.
* [x] Cron/watcher logs are generated.
* [x] `argparse` supports input, output, and confidence threshold options.
* [x] Environment variables are used for database credentials.
* [x] FastAPI backend exposes database statistics.
* [x] FastAPI provides video summaries and anomaly endpoints.
* [x] Next.js dashboard reads monitoring data through the API.
* [x] Dashboard displays live monitoring statistics.
* [x] Dashboard automatically refreshes every 5 seconds.
* [x] End-to-end pipeline was tested successfully.

---

## 📌 Git Versioning

The project uses Git tags to mark major milestones during Week 3 development.

### Day 2

```text
v0.2.0-day2
```

Milestone:

```text
YOLO tracking + MySQL detection logging
```

### Day 3

```text
v0.3.0-day3
```

Milestone:

```text
Video-level tracking + production logging +
cron automation
```

### Week 3 Completion

The final Week 3 release should be tagged after the final README, API, dashboard, configuration, and code changes have been committed and verified.

Suggested tag:

```text
v0.4.0-week3-complete
```

---

## 📊 Project Status

```text
Project:     Industrial Video Monitoring & Tracking System
Week:        Week 3
Status:      Completed
Detection:   YOLOv8
Tracking:    ByteTrack
Database:    MySQL
Automation:  Linux cron + Bash
Backend:     FastAPI
Frontend:    Next.js
Logging:     Python logging + cron logs
Speed Unit:  pixels/frame
Dashboard:   Live 5-second refresh
```

---

## 🔒 Security Notes

The project uses environment variables for database credentials.

Do not commit:

```text
.env
```

Do not place real passwords directly inside:

```text
monitor.py
status_api/main.py
README.md
```

Use environment variables instead:

```env
DB_HOST=localhost
DB_USER=monitor_user
DB_PASSWORD=your_mysql_password
DB_NAME=ppe_monitoring_db
```

The repository should also exclude local datasets, generated videos, model weights, virtual environments, and log files when appropriate.

---

## 🚀 Conclusion

This Week 3 project demonstrates a complete video-monitoring workflow that combines:

```text
Computer Vision
      +
Object Tracking
      +
Speed Analysis
      +
Anomaly Detection
      +
MySQL Persistence
      +
Linux Automation
      +
FastAPI
      +
Next.js
```

The resulting system can automatically detect and track objects in video, persist detection information, process newly added videos through scheduled automation, expose monitoring information through an API, and present the results through a web-based dashboard.

The project establishes a complete foundation for extending the system toward more advanced industrial monitoring capabilities such as:

* Custom object detectors
* Camera calibration
* Physical speed estimation
* Region-of-interest monitoring
* Advanced anomaly detection
* Real-time camera streams
* Alert and notification systems
* Historical analytics
* Production-line performance metrics

```
```
