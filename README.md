# Smart Study Planner: Machine-Learning-Based Personalized Study-Scheduling Agent for Adaptive Learning

## Overview

Smart Study Planner is an AI-powered personalized study scheduling system designed to help students manage their study time efficiently. The system uses Machine Learning models to predict the required study hours for each subject and automatically prioritize subjects based on urgency, performance, and exam schedules.

The application generates adaptive study plans, tracks progress, and reschedules missed sessions to provide a personalized learning experience.

---

## Problem Statement

Many students struggle with:

* Poor time management
* Difficulty estimating study hours
* Lack of subject prioritization
* Ineffective study planning
* Inability to adapt schedules when sessions are missed

Existing planners rely on manual scheduling and fail to provide intelligent recommendations.

---

##  Proposed Solution

Smart Study Planner leverages Machine Learning to:

* Predict required study hours for each subject
* Assign study priorities automatically
* Generate personalized study schedules
* Track learning progress
* Reschedule missed study sessions
* Provide analytics and performance insights

---

## System Architecture

### Input Layer

The system collects:

* Subject Difficulty
* Total Chapters
* Chapters Completed
* Days Until Exam
* Daily Free Hours
* Mid-Term Score
* Urgency Score

### Machine Learning Layer

#### Random Forest Regressor

Predicts:

* Estimated study hours required per subject

#### Random Forest Classifier

Predicts:

* High Priority
* Medium Priority
* Low Priority

### Scheduling Engine

Uses ML predictions to:

* Allocate study sessions
* Prioritize subjects
* Create daily schedules
* Adapt schedules dynamically

### User Interface

Developed using Streamlit:

* AI Planner
* Dashboard
* Progress Tracker
* Analytics Module

---

## Features

### AI Planner

* Subject Input Form
* Study Hour Prediction
* Priority Prediction
* Automatic Schedule Generation
* CSV Export

### Dashboard

* Progress Overview
* Weekly Analytics
* Study Streak Tracking
* Performance Metrics

### Progress Tracking

* Mark Tasks as Complete
* Track Subject Progress
* Monitor Study Consistency

### Adaptive Rescheduling

* Detect Missed Sessions
* Automatically Generate Updated Plans

### Analytics

* Priority Distribution Charts
* Completion Analysis
* Schedule Summary Reports

---

##  Machine Learning Models

### Random Forest Regressor

**Purpose:** Predict study hours required.

#### Input Features

* Subject Difficulty
* Total Chapters
* Chapters Completed
* Days Until Exam
* Daily Free Hours
* Mid-Term Score
* Urgency Score

#### Output

Estimated Study Hours

Example:

Subject: Artificial Intelligence

Predicted Study Time: 8.5 Hours

---

### Random Forest Classifier

**Purpose:** Predict study priority.

#### Classes

* High Priority
* Medium Priority
* Low Priority

#### Output Example

AI → High Priority

Database Systems → Medium Priority

Statistics → Low Priority

---

## 🛠️ Technology Stack

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python 3.10  | Core Programming Language  |
| Streamlit    | Web Application Framework  |
| Scikit-learn | Machine Learning Models    |
| Pandas       | Data Processing            |
| NumPy        | Numerical Computation      |
| Plotly       | Interactive Visualizations |
| Joblib       | Model Serialization        |

---

## Project Structure

```bash
Smart-Study-Planner/
│
├── app.py
├── models/
│   ├── regressor.pkl
│   └── classifier.pkl
│
├── data/
│   ├── training_data.csv
│   └── processed_data.csv
│
├── pages/
│   ├── dashboard.py
│   ├── planner.py
│   ├── analytics.py
│   └── progress_tracker.py
│
├── assets/
│   └── images
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

##  Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Smart-Study-Planner.git

cd Smart-Study-Planner
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

Application will launch at:

```bash
http://localhost:8501
```

---

##  Results

The project successfully achieved:

* Fully functional Streamlit web application
* Integration of two Machine Learning models
* Personalized study schedule generation
* Adaptive rescheduling system
* Interactive analytics dashboard
* CSV export functionality

---

##  Future Enhancements

* User Authentication
* Database Integration
* Mobile Application
* Google Calendar Synchronization
* Pomodoro Timer
* Deep Learning-Based Recommendations
* Cloud Deployment

---

##  Authors

### Sarfraz Ali Katpar

BS Computer Science

### Amjad Ali Abro

BS Computer Science

Supervisor: **Dr. Muhammad Ismail Mangrio**

---

## 📜 License

This project is developed for academic and research purposes.

MIT License © 2026

---


