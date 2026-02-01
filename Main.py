import telebot
import cv2
import pygame
import time
import os
from gtts import gTTS
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import threading
from twilio.rest import Client  
import numpy as np  

video_lock = threading.Lock()  # Prevent multiple video accesses

camera_lock = threading.Lock() # Prevent multiple picture accesses

reset_lock = threading.Lock()  # Prevent multiple resets

audio_lock = threading.Lock()  # Prevent multiple audio accesses in pretext menu


# Telegram Credentials
TELEGRAM_BOT_TOKEN = "8064126822:AAHAxsJJuJqLm0SenAsvwn9TRL0N7m4aKl7"
CHAT_IDS = ["1134494580"]


# Twilio Credentials
TWILIO_ACCOUNT_SID = "ACc2363109b1e551b0502c0d0c3f60cce1"
TWILIO_AUTH_TOKEN = "22e15c26ab16495655e69b2daf45d22c"
TWILIO_PHONE_NUMBER = "+18283445xxx"


# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# List of phone numbers to send SMS alerts
ALERT_PHONE_NUMBERS = ["+91xxxxxxxxxx"] 
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# Initialize camera
camera_index = 0  # Change this index if you have multiple cameras
camera = cv2.VideoCapture(camera_index)  # Use DirectShow backend

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Camera not accessible. Please check your camera settings.")
    exit()



# Function to Send SMS Alert
def send_sms_alert(message):
    for phone_number in ALERT_PHONE_NUMBERS:
        try:
            twilio_client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            print(f" SMS sent to {phone_number}")
        except Exception as e:
            print(f" Failed to send SMS to {phone_number}: {e}")



# Function to Send Telegram Alert to All Users
def send_to_all_users(message, photo_path=None):
    for chat_id in CHAT_IDS:
        try:
            if photo_path:
                with open(photo_path, "rb") as img:
                    bot.send_photo(chat_id, img, caption=message)
            else:
                bot.send_message(chat_id, message)
        except Exception as e:
            print(f" Failed to send message to {chat_id}: {e}")



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, " Welcome! Initializing system...")
    main_menu(message.chat.id)  # Show main menu


# Main Menu
def main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Send Image"), KeyboardButton("Send Video"))
    markup.add(KeyboardButton("Audio Pretext"), KeyboardButton("Alarm"))
    markup.add(KeyboardButton("Reset System")) 
    bot.send_message(chat_id, "Select an option:", reply_markup=markup)



# Capture and Send Image
@bot.message_handler(func=lambda message: message.text == "Send Image")
def send_image(message):
    with camera_lock:
        for i in range(5):
            ret, frame = camera.read()
            if ret:
                image_path = f"capture_{i}.jpg"
                cv2.imwrite(image_path, frame)
                with open(image_path, "rb") as img:
                    bot.send_photo(message.chat.id, img)
                os.remove(image_path)
            time.sleep(1)




# Capture and Send Optimized Video
@bot.message_handler(func=lambda message: message.text == "Send Video")
def handle_send_video(message):
    threading.Thread(target=send_video_safely, args=(message.chat.id,), daemon=True).start()

def send_video_safely(chat_id):
    with video_lock:
        try:
            filename = "output_video.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'avc1' sometimes gives issues without ffmpeg
            fps = 10  # Optimized for size
            duration = 30  # seconds
            total_frames = fps * duration

            original_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            original_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(original_width * 0.75)
            height = int(original_height * 0.75)

            video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))

            frame_count = 0
            while frame_count < total_frames:
                ret, frame = camera.read()
                if ret:
                    resized_frame = cv2.resize(frame, (width, height))
                    video_writer.write(resized_frame)
                    frame_count += 1
                else:
                    break

            video_writer.release()

            with open(filename, 'rb') as video_file:
                bot.send_video(chat_id, video_file, supports_streaming=True)

            os.remove(filename)
        except Exception as e:
            bot.send_message(chat_id, f"Video error: {e}")




# Audio Pretext Menu
@bot.message_handler(func=lambda message: message.text == "Audio Pretext")
def audio_pretext_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Delivery Instructions"), KeyboardButton("Visitor Instructions"))
    markup.add(KeyboardButton("Cleaning Instructions"), KeyboardButton("Security Instructions"))
    markup.add(KeyboardButton("Back to Main Menu"))
    bot.send_message(message.chat.id, "Choose a category:", reply_markup=markup)


# Handle Audio Pretext Selection
@bot.message_handler(func=lambda message: message.text in submenus.keys())
def handle_audio_pretext_selection(message):
    category = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    for option in submenus[category]:
        markup.add(KeyboardButton(option))
    
    markup.add(KeyboardButton("Back to Audio Pretext"))
    bot.send_message(message.chat.id, f"Choose an instruction from {category}:", reply_markup=markup)


# Submenus for Audio Pretext
submenus = {
    "Delivery Instructions": [
        "The homeowner is away. Please leave the package with our neighbor.",
        "Please place the parcel inside the designated delivery box near the door.",
        "No one is available to receive the package. Kindly reschedule the delivery for another time.",
        "This address is currently not accepting deliveries. Please return the package to the sender.",
    ],
    "Visitor Instructions": [
        "The homeowner is unavailable. Please call [Phone Number] for further assistance.",
        "If you have an appointment, please wait while your visit is verified."
    ],
    "Cleaning Instructions": [
        "Trash bins are placed near the gate. Please collect them as per the schedule.",
        "All leaves and yard waste should be collected in compostable bags and placed in the designated area.",
        "Lawn maintenance is scheduled for today. Please ensure all cut grass and debris are cleared after trimming."
    ],
    "Security Instructions": [
        "Attention! Your presence has been recorded. Please state your purpose or leave immediately.",
        "This property is private. Unapproved visitors are not allowed beyond this point.",
        "Warning! A silent alarm has been triggered. Authorities have been notified."
    ]
}


# Handle Back Navigation
@bot.message_handler(func=lambda message: message.text == "Back to Audio Pretext")
def back_to_audio_pretext(message):
    audio_pretext_menu(message)

@bot.message_handler(func=lambda message: message.text == "Back to Main Menu")
def back_to_main_menu(message):
    main_menu(message.chat.id)

# Function to Play Multiple Audio Safely
def play_audio(text):
    with audio_lock:  # Prevent multiple audios from playing simultaneously
        filename = "audio.mp3"

        try:
            # Delete old audio file if exists
            if os.path.exists(filename):
                os.remove(filename)

            # Generate new audio file
            tts = gTTS(text=text, lang="en")
            tts.save(filename)

            # Initialize pygame properly
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(1)  # Prevents CPU overload

            pygame.mixer.music.stop()
            pygame.mixer.quit()

            # Delete the audio file after playing
            os.remove(filename)
        except Exception as e:
            print(f" Error playing audio: {e}")


# Handle Audio Playback - Run in a separate thread
@bot.message_handler(func=lambda message: any(message.text in options for options in submenus.values()))
def handle_audio_playback(message):
    threading.Thread(target=play_audio, args=(message.text,), daemon=True).start()




# Alarm Menu
@bot.message_handler(func=lambda message: message.text == "Alarm")
def alarm_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Stop Alarm"))
    markup.add(KeyboardButton("Back to Main Menu"))
    play_alarm()
    bot.send_message(message.chat.id, "Alarm is playing! Choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Stop Alarm")
def stop_alarm_handler(message):
    stop_alarm()
    bot.send_message(message.chat.id, "Alarm stopped.")


# Alarm Playback Function 
def play_alarm():
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play(-1)  # Loop indefinitely

def stop_alarm():
    pygame.mixer.music.stop()
    pygame.mixer.quit()




# --- Reset System Function ---
@bot.message_handler(func=lambda message: message.text == "Reset System")
def restart_motion_detection(message):
    global restart_flag, last_alert_time, camera

    if reset_lock.acquire(blocking=False):
        try:
            bot.send_message(message.chat.id, " Restarting system...")

            # Stop current motion detection
            restart_flag = True
            time.sleep(3)  # Allow thread to notice flag and shut down

            # Close OpenCV windows and release camera safely
            cv2.destroyAllWindows()
            try:
                camera.release()
            except Exception as e:
                print(f"Error releasing camera: {e}")

            time.sleep(1)  # Small delay to ensure clean release

            # Reinitialize camera
            camera = cv2.VideoCapture(camera_index)
            time.sleep(2)  # Allow camera to warm up

            if not camera.isOpened():
                bot.send_message(message.chat.id, " Camera failed to reinitialize.")
                return

            # Reset motion detection
            restart_flag = False
            last_alert_time = time.time() - cooldown_time

            start_motion_detection()

            bot.send_message(message.chat.id, " System restarted! Motion detection is now active.")
        finally:
            reset_lock.release()
            main_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, " Another reset is already in progress. Please wait.")




# --- Motion Detection Variables ---
cooldown_time = 300  # 5-minute cooldown
last_alert_time = time.time() - cooldown_time
restart_flag = False
first_frame = None  # Ensure it's globally accessible


# --- Motion Detection Function ---
def motion_detection():
    global last_alert_time, restart_flag, first_frame
    time.sleep(2)  # Camera warm-up
    first_frame = None  # Reset first frame

    motion_start_time = None
    person_detected = False
    
    # Motion Detection on Reset
    while True:
        if restart_flag:
            print(" Stopping motion detection for restart...")
            #camera.release()
            cv2.destroyAllWindows()
            return

        ret, frame = camera.read()
        if not ret:
            print("Error: Can't grab frame")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if first_frame is None:
            first_frame = gray
            continue

        frame_delta = cv2.absdiff(first_frame, gray)
        threshold = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)

        height, width = frame.shape[:2]
        mask = np.zeros_like(gray)
        mask[int(height * 0.4):, :] = 255
        masked_threshold = cv2.bitwise_and(threshold, threshold, mask=mask)

        contours, _ = cv2.findContours(masked_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < 8000:
                continue
            motion_detected = True
            break  # No need to check more contours

        current_time = time.time()
       
       # Motion Detection at start 
        if motion_detected:
            if not person_detected:
                motion_start_time = current_time
                person_detected = True
            elif current_time - motion_start_time >= 2:  # 2 seconds check
                if current_time - last_alert_time >= cooldown_time:
                    last_alert_time = current_time
                    print(" Motion confirmed! Sending alerts...")

                    image_path = "motion.jpg"
                    cv2.imwrite(image_path, frame)

                    for chat_id in CHAT_IDS:
                        try:
                            with open(image_path, "rb") as img:
                                bot.send_photo(chat_id, img, caption=" Motion detected!")
                                print(f" Telegram alert sent to {chat_id}")
                        except telebot.apihelper.ApiTelegramException as e:
                            print(f" Failed to send alert to {chat_id}: {e}")

                    os.remove(image_path)
                    send_sms_alert(" Alert: Motion detected at your location!")
                    person_detected = False
        else:
            person_detected = False
            motion_start_time = None

        cv2.line(frame, (0, int(height * 0.4)), (width, int(height * 0.4)), (0, 0, 255), 2)
        cv2.imshow("Motion Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(" Motion detection stopped.")
    camera.release()
    cv2.destroyAllWindows()


# --- Start Motion Detection in a Thread ---
def start_motion_detection():
    global restart_flag, first_frame
    restart_flag = False  # Ensure restart flag is reset
    first_frame = None  # Reset first frame
    threading.Thread(target=motion_detection, daemon=True).start()


# --- Start Motion Detection at Launch ---
start_motion_detection()
    

# --- Start Bot ---
bot.polling(none_stop=True)
