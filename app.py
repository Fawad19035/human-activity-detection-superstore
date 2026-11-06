import os  # For file and directory operations
from flask import Flask, render_template, Response, send_file, request, send_from_directory, jsonify  # Flask modules for web handling
import cv2  # OpenCV for image and video processing
import pickle  # For saving/loading Python objects (like model data)
import numpy as np  # For numerical operations and handling arrays/images
import tempfile  # For creating temporary files and directories
import uuid  # For generating unique IDs (useful for filenames)
from ultralytics import YOLO  # Importing YOLOv8 model from Ultralytics for object detection
import threading  # For running background tasks (like video streaming)
from datetime import datetime  # For getting current date and time


app = Flask(__name__)

# Configuration
app.config['PROCESSED_VIDEOS'] = 'processed_videos'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB upload limit

# Create directories if they don't exist
os.makedirs(app.config['PROCESSED_VIDEOS'], exist_ok=True)

# Load your trained YOLOv8 model
try:
    with open("yolomodel.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    # Fallback to loading directly if pickle file doesn't exist
    model = YOLO("runs/detect/train/weights/best.pt")

# Define your activity classes
CLASS_NAMES = [
    'Comparing Products',
    'Picking Up Items',
    'Pushing a Shopping Cart',
    'Reading Label',
    'Talking with Friend',
    'Placing Items into Cart',
    'Using Mobile Phone',
    'Walking'
]

# Global variables for video control
video_active = False
cap = None
activity_count = 0
recent_activities = []  # Store last 3 activity detections
current_stream = None

# Function for video feed generation
def generate_video_feed():
    global video_active, cap, activity_count, recent_activities
    
    activity_count = 0
    recent_activities = []  # Reset recent activities
    
    while video_active and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 on the frame
        results = model(frame)
        frame_activities = []

        # Draw bounding boxes and collect activities
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                confidence = box.conf[0].item()
                activity = CLASS_NAMES[class_id]
                label = f"{activity}: {confidence:.2f}"

                # Draw rectangle and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                if confidence > 0.5:  # Only count confident detections
                    frame_activities.append(activity)
                    # Update recent activities
                    recent_activities.append(activity)
                    # Keep only the last 3
                    if len(recent_activities) > 3:
                        recent_activities = recent_activities[-3:]
        
        # Update activity count: count every frame that has at least one activity
        if frame_activities:
            activity_count += 1

        # Add activity counter and timestamp to frame
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, f"Activities: {activity_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, timestamp, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Convert frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Function for video file detection
def process_video(uploaded_file):
    # Save uploaded video to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(uploaded_file.read())
    temp_file_path = temp_file.name
    temp_file.close()
    
    cap = cv2.VideoCapture(temp_file_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Create output file with unique name
    output_filename = f"processed_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(app.config['PROCESSED_VIDEOS'], output_filename)
    
    # Use H.264 codec for better browser compatibility
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    total_activities = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 on the frame
        results = model(frame)
        frame_activities = []

        # Draw bounding boxes
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                confidence = box.conf[0].item()
                activity = CLASS_NAMES[class_id]
                label = f"{activity}: {confidence:.2f}"

                # Draw rectangle and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                if confidence > 0.5:
                    frame_activities.append(activity)
        
        # Update activity count: count every frame that has at least one activity
        if frame_activities:
            total_activities += 1
        
        # Add frame counter and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Activities: {total_activities}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, timestamp, (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    os.unlink(temp_file_path)  # Delete temp file
    
    # Return only the filename, not the full path
    return output_filename, total_activities

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_feed(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_feed', methods=['POST'])
def start_feed():
    global video_active, cap, current_stream
    
    source_type = request.json.get('source_type')
    source = request.json.get('source')
    
    # Stop any existing feed
    if cap is not None:
        cap.release()
    
    try:
        if source_type == 'webcam':
            cap = cv2.VideoCapture(0)
            current_stream = 'webcam'
        elif source_type == 'rtsp':
            cap = cv2.VideoCapture(source)
            current_stream = source
        else:
            return jsonify({'error': 'Invalid source type'}), 400
        
        if not cap.isOpened():
            return jsonify({'error': 'Could not open video source'}), 400
        
        video_active = True
        return jsonify({
            'status': 'started',
            'source_type': source_type,
            'source': source if source_type == 'rtsp' else 'webcam'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop_feed')
def stop_feed():
    global video_active, cap
    video_active = False
    if cap is not None:
        cap.release()
        cap = None
    return jsonify({'status': 'stopped'})

@app.route('/get_activity_count')
def get_activity_count():
    global activity_count, recent_activities
    return jsonify({
        'count': activity_count,
        'activities': recent_activities,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/process_video', methods=['POST'])
def handle_video_processing():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded'}), 400
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        output_filename, activity_count = process_video(video_file)
        return jsonify({
            'output_filename': output_filename,
            'activity_count': activity_count,
            'message': 'Video processed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_video/<path:filename>')
def download_video(filename):
    return send_file(
        os.path.join(app.config['PROCESSED_VIDEOS'], filename),
        as_attachment=True,
        download_name=f"activity_detection_{filename}"
    )

@app.route('/processed_videos/<path:filename>')
def serve_processed_video(filename):
    return send_from_directory(app.config['PROCESSED_VIDEOS'], filename)

@app.route('/test_rtsp', methods=['POST'])
def test_rtsp():
    rtsp_url = request.json.get('rtsp_url')
    if not rtsp_url:
        return jsonify({'error': 'No RTSP URL provided'}), 400
    
    test_cap = cv2.VideoCapture(rtsp_url)
    if test_cap.isOpened():
        test_cap.release()
        return jsonify({'status': 'success', 'message': 'RTSP stream is accessible'})
    else:
        return jsonify({'error': 'Could not open RTSP stream'}), 400

if __name__ == '__main__':
    app.run(debug=True, threaded=True)