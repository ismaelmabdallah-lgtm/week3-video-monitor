import argparse
import datetime
import math
import os
from pathlib import Path
import cv2
import mysql.connector
from dotenv import load_dotenv
from ultralytics import YOLO

# Define Base Directory (Absolute Paths)
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'monitor_user'),
    'password': os.getenv('DB_PASSWORD', 'root1234'),
    'database': os.getenv('DB_NAME', 'ppe_monitoring_db')
}

# Relative Anomaly Threshold in pixels/frame
SPEED_ANOMALY_THRESHOLD = 70.0

def calculate_speed(prev_bbox, curr_bbox):
    """Calculate relative displacement speed in pixels/frame."""
    if prev_bbox is None:
        return 0.0
    px1, py1, px2, py2 = prev_bbox
    cx1, cy1, cx2, cy2 = curr_bbox
    
    prev_center = ((px1 + px2) / 2, (py1 + py2) / 2)
    curr_center = ((cx1 + cx2) / 2, (cy1 + cy2) / 2)
    
    distance = math.sqrt((curr_center[0] - prev_center[0])**2 + (curr_center[1] - prev_center[1])**2)
    return round(distance, 2)

def main():
    parser = argparse.ArgumentParser(description="Industrial Video Monitoring & Tracking System")
    parser.add_argument("--input", type=str, required=True, help="Path to input video file")
    parser.add_argument("--output", type=str, default=str(BASE_DIR / "output_videos" / "processed_output.mp4"), help="Path to output video file")
    parser.add_argument("--threshold", type=float, default=0.3, help="Confidence threshold")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.exists():
        print(f"❌ Error: Input video '{input_path}' not found!")
        return

    print(f"🚀 Loading YOLOv8 Tracking Model...")
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(str(input_path))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Connect to MySQL Database
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Connected to MySQL Database successfully.")
    except Exception as e:
        print(f"❌ MySQL Connection Error: {e}")
        return

    frame_count = 0
    previous_bboxes = {}  # {object_id: (x1, y1, x2, y2)}
    batch_records = []
    BATCH_SIZE = 100  # Commit to DB every 100 detections/frames

    print(f"🎥 Processing Video: {input_path}...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        
        # Accurate Video Timestamp
        video_seconds = frame_count / fps
        video_timestamp = datetime.datetime(2026, 1, 1) + datetime.timedelta(seconds=video_seconds)

        # Run YOLOv8 ByteTrack
        results = model.track(frame, persist=True, conf=args.threshold, tracker="bytetrack.yaml", verbose=False)

        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().numpy()
            clss = results[0].boxes.cls.int().cpu().numpy()
            confs = results[0].boxes.conf.cpu().numpy()

            for bbox, track_id, cls_idx, conf in zip(boxes, track_ids, clss, confs):
                x1, y1, x2, y2 = bbox
                class_name = model.names[cls_idx]

                # Calculate speed (pixels/frame)
                speed = calculate_speed(previous_bboxes.get(track_id), bbox)
                previous_bboxes[track_id] = bbox

                # Anomaly check based on relative speed threshold
                is_anomaly = speed > SPEED_ANOMALY_THRESHOLD

                batch_records.append((
                    frame_count, video_timestamp, int(track_id), class_name, 
                    float(conf), float(x1), float(y1), float(x2), float(y2), 
                    float(speed), is_anomaly
                ))

                # Draw bounding box and track info
                color = (0, 0, 255) if is_anomaly else (0, 255, 0)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                label = f"ID:{track_id} {class_name} {conf:.2f} Spd:{speed}"
                cv2.putText(frame, label, (int(x1), max(15, int(y1) - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Batch Insert into MySQL
        if len(batch_records) >= BATCH_SIZE:
            insert_query = """
            INSERT INTO detections 
            (frame_number, timestamp, object_id, class_name, confidence, x1, y1, x2, y2, speed, is_anomaly)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, batch_records)
            conn.commit()
            batch_records.clear()

        out.write(frame)

    # Insert remaining records
    if batch_records:
        insert_query = """
        INSERT INTO detections 
        (frame_number, timestamp, object_id, class_name, confidence, x1, y1, x2, y2, speed, is_anomaly)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, batch_records)
        conn.commit()

    cap.release()
    out.release()
    cursor.close()
    conn.close()

    print(f"🎉 Processing Complete! Output saved to: {output_path}")
    print(f"📊 Processed {frame_count} frames and logged all detections to MySQL efficiently.")

if __name__ == "__main__":
    main()
