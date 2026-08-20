import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="Video Monitor Status API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'monitor_user'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'ppe_monitoring_db')
        )
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database Connection Error: {err}")

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/api/status")
def get_status_summary():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query_stats = """
    SELECT 
        COUNT(*) AS total_detections,
        COUNT(DISTINCT CONCAT(video_name, '_', object_id)) AS unique_objects,
        COUNT(DISTINCT video_name) AS total_videos
    FROM detections;
    """
    cursor.execute(query_stats)
    stats = cursor.fetchone()

    query_last_video = """
    SELECT video_name, MAX(created_at) AS last_processed_at
    FROM detections
    GROUP BY video_name
    ORDER BY last_processed_at DESC
    LIMIT 1;
    """
    cursor.execute(query_last_video)
    last_video = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "total_detections": stats["total_detections"] or 0,
        "unique_objects": stats["unique_objects"] or 0,
        "total_videos": stats["total_videos"] or 0,
        "last_video": last_video["video_name"] if last_video else "N/A",
        "last_processed_at": str(last_video["last_processed_at"]) if last_video else "N/A"
    }

@app.get("/api/anomalies")
def get_anomalies(limit: int = 20):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query_anomalies = """
    SELECT 
        id, frame_number, timestamp, video_name, object_id, 
        class_name, confidence, speed
    FROM detections
    WHERE is_anomaly = TRUE
    ORDER BY id DESC
    LIMIT %s;
    """
    cursor.execute(query_anomalies, (limit,))
    anomalies = cursor.fetchall()

    for row in anomalies:
        row["timestamp"] = str(row["timestamp"])

    cursor.close()
    conn.close()

    return {"count": len(anomalies), "anomalies": anomalies}

@app.get("/api/videos")
def get_videos_summary():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query_videos = """
    SELECT 
        video_name,
        COUNT(*) AS total_detections,
        COUNT(DISTINCT object_id) AS unique_objects,
        SUM(CASE WHEN is_anomaly = 1 THEN 1 ELSE 0 END) AS anomaly_count,
        MAX(created_at) AS processed_at
    FROM detections
    GROUP BY video_name
    ORDER BY processed_at DESC;
    """
    cursor.execute(query_videos)
    videos = cursor.fetchall()

    for v in videos:
        v["processed_at"] = str(v["processed_at"])

    cursor.close()
    conn.close()

    return {"videos": videos}
