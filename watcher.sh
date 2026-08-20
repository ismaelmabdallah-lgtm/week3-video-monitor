cat << 'EOF' > watcher.sh
#!/bin/bash
set -u

# Define absolute directory paths
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="$PROJECT_DIR/input_videos"
OUTPUT_DIR="$PROJECT_DIR/output_videos"
LOG_DIR="$PROJECT_DIR/logs"
PROCESSED_LIST="$LOG_DIR/processed_files.txt"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"

# Ensure required directories and files exist
mkdir -p "$OUTPUT_DIR" "$LOG_DIR" "$INPUT_DIR"
touch "$PROCESSED_LIST"

for video_file in "$INPUT_DIR"/*.mp4; do
    # Check if actual file exists
    [ -f "$video_file" ] || continue

    filename=$(basename "$video_file")

    # Deduplication check: Skip if already processed
    if grep -Fxq "$filename" "$PROCESSED_LIST"; then
        echo "⏭️  [Watcher] Skipping already processed file: $filename"
        continue
    fi

    echo "🚀 [Watcher] New video detected: $filename. Starting monitor pipeline..."
    output_file="$OUTPUT_DIR/processed_$filename"

    # Execute monitor.py via venv python
    if "$VENV_PYTHON" "$PROJECT_DIR/monitor.py" --input "$video_file" --output "$output_file" --threshold 0.35; then
        echo "$filename" >> "$PROCESSED_LIST"
        echo "✅ [Watcher] Successfully processed and recorded: $filename"
    else
        echo "❌ [Watcher] Failed to process video: $filename (Exit code non-zero)" >&2
    fi
done
EOF
chmod +x watcher.sh