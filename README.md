# 🏆 Smart CCTV Surveillance System for Home Security  
**Awarded Best Project – Department of Information Technology**  
**Published in IJARESM (April 2025, Special Issue)**

---

## 📌 Project Overview

This project presents a **Smart Home Surveillance System** designed to enhance residential security using **computer vision, IoT concepts, and real-time alert mechanisms**. The system continuously monitors live camera feed, detects motion in a defined region, and instantly notifies users through a **Telegram Bot and SMS alerts**.

The solution integrates **OpenCV-based motion detection**, **Telegram Bot automation**, **audio alerts**, and **remote system control**, making it a reliable and user-friendly home security system.

The project was recognized as the **Best Project by the Department** and was later **published in the International Journal of All Research Education and Scientific Methods (IJARESM)**.

---

## 🎯 Objectives

- To design a real-time home surveillance system with motion detection  
- To provide instant alerts via Telegram and SMS  
- To reduce false motion alerts using region-based detection  
- To enable remote monitoring and control through a bot interface  
- To implement audio-based security responses and alarm mechanisms  

---

## 🧠 System Architecture

The system consists of:
- A camera module connected to a computing device (PC / Raspberry Pi)
- Motion detection using frame differencing
- Telegram Bot interface for user interaction
- SMS alert system using Twilio
- Speaker-based audio alerts using text-to-speech

---

## ⚙️ Key Features

### 1. Real-Time Motion Detection
- Uses frame differencing and thresholding
- Detects motion only in the lower 60% of the frame
- Minimizes false positives caused by lighting or background noise

### 2. Telegram Bot Control
- Fully keyboard-driven interface
- No manual typing required
- Multiple options available after motion detection

### 3. Image Capture & Transmission
- Captures multiple images from the live camera feed
- Sends images instantly via Telegram
- Automatically deletes temporary files after use

### 4. Optimized Video Recording
- Records a 30-second video on demand
- Resolution optimized to reduce file size
- Supports Telegram video streaming
- Thread-safe implementation to avoid crashes

### 5. Audio Pretext System
Predefined voice instructions are played through a speaker using Text-to-Speech (gTTS).

**Categories:**
- Delivery Instructions  
- Visitor Instructions  
- Cleaning Instructions  
- Security Instructions  

This feature is useful for handling visitors, deliveries, and security warnings remotely.

### 6. Alarm System
- Plays an alarm sound in a continuous loop
- Can be stopped remotely via Telegram
- Acts as an immediate security deterrent

### 7. SMS Alert Integration
- Sends SMS alerts using Twilio API
- Works as a backup notification channel
- Ensures alerts are received even if Telegram is unavailable

### 8. Reset & Recovery Mechanism
- Safely stops all running threads
- Releases and reinitializes the camera
- Restarts motion detection without restarting the program
- Prevents multiple reset conflicts using thread locks

---

## 🔐 Thread-Safe Design

The system uses multiple locks to ensure stability:
- Prevents multiple camera accesses
- Avoids overlapping audio playback
- Ensures only one reset operation runs at a time
- Allows safe parallel execution of tasks

This makes the system suitable for long-running, real-world deployment.

---

## 🧪 Algorithms Used

### Motion Detection
- Grayscale conversion
- Gaussian blur for noise reduction
- Frame differencing
- Thresholding and contour detection
- Area-based filtering
- Time-based confirmation

### Audio System
- Text-to-Speech using gTTS
- Audio playback using pygame
- Threaded execution to avoid blocking

---

## 🛠 Technologies Used

- Python  
- OpenCV (cv2)  
- NumPy  
- Telegram Bot API  
- Twilio API  
- gTTS  
- Pygame  
- Threading  

---

## 💻 Hardware Requirements

- Camera (USB / Pi Camera – 5MP recommended)
- Speaker (Bluetooth or Wired)
- PC or Raspberry Pi 3B+
- Internet connectivity

---

## 🚀 How to Run the Project

```bash
pip install -r requirements.txt
python main.py
```
---

### ✅ Ensure the following before running:

- 📷 A working camera is connected to the system  
- 🌐 Internet connectivity is available  
- 🤖 Telegram Bot Token is correctly configured in the code  
- 📲 Twilio credentials (Account SID, Auth Token, Phone Number) are configured  
- 🔊 The `alarm.mp4` file is present in the root directory  

---

## 🏅 Achievements

- 🥇 **Best Project Award – Department of Information Technology**  
- 👨‍💻 **Group Leader** – Led system design, architecture, and final integration  
- 🧠 Designed and implemented the complete core logic including:
  - Motion detection algorithm  
  - Telegram bot interaction flow  
  - Thread-safe video, image, and audio handling  
  - System reset and recovery mechanism  
- 📄 **Research paper published** in *International Journal of All Research Education and Scientific Methods (IJARESM)*  
  *(April 2025, Special Issue)*  
- 🏫 Project officially recognized for **innovation, real-world applicability, and technical depth**

---

## 👤 Authors

- 🧑‍💻 **Amaan A. Saiyyad** *(Group Leader)*  
- 👨‍💻 Sujeet S. Potdar  
- 👩‍💻 Anagha P. Gulhane  
- 👩‍💻 Madhavi A. Mohite  
- 🎓 Prof. Kaveri B. Kari *(Project Guide)*  

---

## 📚 Reference

📘 *Smart CCTV Surveillance System for Home Security using Raspberry Pi and Camera*  
📰 International Journal of All Research Education and Scientific Methods (IJARESM)  
📅 April 2025, Special Issue


