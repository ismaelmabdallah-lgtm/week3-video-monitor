CREATE DATABASE IF NOT EXISTS ppe_monitoring_db;
USE ppe_monitoring_db;

CREATE TABLE IF NOT EXISTS detections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    frame_number INT NOT NULL,
    timestamp DATETIME NOT NULL,
    object_id INT NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    x1 FLOAT NOT NULL,
    y1 FLOAT NOT NULL,
    x2 FLOAT NOT NULL,
    y2 FLOAT NOT NULL,
    speed FLOAT DEFAULT 0.0,
    is_anomaly BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
