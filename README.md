# Human Activity Detection in Superstore Using Computer Vision and Machine Learning

**A Real-Time AI-Based Human Activity Recognition System for Supermarkets**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-green.svg)](https://github.com/ultralytics/ultralytics)
[![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![Computer Vision](https://img.shields.io/badge/Domain-Computer%20Vision-orange.svg)]()
[![Machine Learning](https://img.shields.io/badge/Domain-Machine%20Learning-purple.svg)]()

## 1. Project Overview

Human Activity Detection in Superstore is an AI-powered system designed to detect and classify customer activities in supermarket surveillance footage using Computer Vision and Machine Learning.

The system uses a YOLOv8 object-detection model to identify eight different customer activities from video frames in real time. It is integrated with a Flask-based web application that allows users to process uploaded videos and connect live CCTV input.

The main objective is to explore how Artificial Intelligence can support supermarket monitoring, customer activity analysis, and intelligent retail management.

## 2. Project Objectives

- Develop an AI-based human activity detection system for supermarket environments.
- Build a custom dataset representing different customer activities.
- Train and evaluate a YOLOv8 model for activity detection.
- Implement real-time detection using video and CCTV footage.
- Develop a user-friendly web interface using Flask.
- Explore the practical application of Computer Vision in intelligent retail environments.

## 3. Supported Human Activities

The system detects and classifies the following eight activities:

1. Comparing Products
2. Picking Up Items
3. Pushing a Shopping Cart
4. Reading a Product Label
5. Talking with a Friend
6. Placing Items into a Shopping Cart
7. Using a Mobile Phone
8. Walking

## 4. Technologies and Tools

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Deep Learning | YOLOv8 |
| Machine Learning | ML and Deep Learning |
| Dataset Annotation | Roboflow |
| Model Training | Google Colab |
| GPU | NVIDIA Tesla T4 |
| Web Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Data Augmentation | Albumentations / training pipeline tools as implemented |
| Model Evaluation | Precision, Recall, mAP |

## 5. Dataset Development

We developed our own dataset for the project instead of relying entirely on an existing activity dataset.

The dataset development process included:

- Collecting supermarket-related video clips from different camera angles and environments.
- Extracting video frames for dataset creation.
- Defining and organizing eight activity classes.
- Annotating activity bounding boxes using Roboflow.
- Exporting annotations in YOLO format.
- Removing unclear, blurred and unusable frames.
- Applying data augmentation to improve dataset diversity.

**Dataset statistics:**

- Initial dataset: 6,200 frames.
- Augmented dataset: 8,000 frames.
- Training set: 80%.
- Validation set: 10%.
- Testing set: 10%.

## 6. Methodology

The project follows these major development stages:

1. Literature Review: Studying existing approaches, including HOG + SVM, CNN-LSTM, Faster R-CNN, SSD and YOLO.
2. Dataset Collection: Collecting supermarket video footage and extracting frames.
3. Data Annotation: Labelling the eight activities using Roboflow.
4. Data Preprocessing: Cleaning, augmentation and dataset splitting.
5. Model Training: Training the YOLOv8 model using Google Colab.
6. Model Evaluation: Evaluating detection performance using standard metrics.
7. Web Application Development: Integrating the trained model into a Flask application.
8. Real-Time Detection: Processing live CCTV footage and uploaded videos.

## 7. Model Performance

The trained YOLOv8 model achieved the following results on the test dataset:

| Evaluation Metric | Result |
|---|---:|
| Precision | 0.975 |
| Recall | 0.966 |
| mAP@0.5 | 0.987 |
| Inference Time | Approximately 3.6 ms/image |

These results indicate strong detection performance on the project's test dataset.

*Note: Performance figures represent the reported experimental results and should be interpreted in the context of the project's dataset and evaluation setup.*

## 8. Web Application Features

The project includes a Flask-based web application with the following functionality:

- Video Upload: Upload supermarket video files for activity detection.
- Live CCTV Detection: Process live CCTV input.
- Real-Time Predictions: Detect activities in video frames.
- Activity Classification: Display predicted activity labels.
- Detection Visualization: Overlay bounding boxes and activity labels on frames.
- Web-Based Interface: Access the detection system through a browser.

## 9. System Workflow

Video Input / CCTV Footage  
↓  
Frame Extraction  
↓  
Image Preprocessing  
↓  
YOLOv8 Model  
↓  
Human Activity Detection and Classification  
↓  
Bounding Boxes and Predicted Labels  
↓  
Flask Web Application  
↓  
Real-Time Activity Visualization

## 10. Project Structure

The repository contains the model implementation, backend, frontend, dataset-related resources and project documentation.

The exact folder structure will be updated according to the uploaded source code.

## 11. Installation and Setup

**Prerequisites:**

- Python 3.10 or a compatible version.
- Git.
- pip.
- A compatible environment for running YOLOv8.

**Clone the repository:**

```bash
git clone https://github.com/Fawad19035/human-activity-detection-superstore.git

cd human-activity-detection-superstore
```

**Create a virtual environment:**

```bash
python -m venv venv
```

**Activate the environment (Windows):**

```bash
venv\Scripts\activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run the application:**

```bash
python app.py
```

The application entry point and commands may need adjustment according to the actual source-code structure.

## 12. Academic Information

**Project Title:** Human Activity Detection in Superstore Using Computer Vision and Machine Learning

**Degree:** BS Software Engineering

**Department:** Department of Software Engineering

**University:** University of Malakand

**Academic Session:** 2024–2025

**Project Supervisor:** Dr. Khalil Ullah

**Project Type:** Group Final Year Project

## 13. Project Contributors

**Fawad Azam**
- Literature review and methodology selection.
- Custom dataset design and development.
- Video-frame extraction and annotation.
- Data preprocessing and augmentation.
- YOLOv8 model training and evaluation.
- Flask-based application development and integration.
- Project documentation and thesis contributions.

**Ahmad Ullah**
- Project development and implementation.
- Dataset collection and annotation collaboration.
- Contribution to project documentation and final report.

## 14. Future Improvements

- Expand the dataset with more activities and environments.
- Improve detection under occlusion and poor lighting.
- Optimize inference for edge devices.
- Add advanced customer behavior analytics.
- Introduce activity statistics and reporting dashboards.
- Explore multi-camera monitoring and tracking.

## 15. Acknowledgements

We sincerely thank our project supervisor, **Dr. Khalil Ullah**, for his guidance, support and valuable feedback throughout the project.

We also acknowledge the Department of Software Engineering, University of Malakand, for providing the academic environment to complete this project.

---

**Developed as a BS Final Year Project (2024–2025).**

**Repository:** Fawad19035 / Human Activity Detection in Superstore

**Project Domain:** Artificial Intelligence | Machine Learning | Deep Learning | Computer Vision | Web Development
