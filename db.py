from gpiozero import LED, MotionSensor
import time
import speech_recognition as sr
import sqlite3

# GPIO pin setup
blue_led = LED(17)  # GPIO pin for the blue LED
pir = MotionSensor(4)

# Recognize speech setup
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        print(audio)
    
    try:
        recognized_text = recognizer.recognize_google(audio).lower()
        print("Recognized:", recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

# Database setup
def insert_command(command):
    conn = sqlite3.connect("commands.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO light_commands (command) VALUES (?)", (command,))
    conn.commit()
    conn.close()

def main():
    print("Magic Bulb with Motion Sensor and Voice Control started...")
    blue_led.off()
    light_on = False
    
    try:
        while True:
            print("Waiting for motion...")
            pir.wait_for_motion()
            print("Motion detected!")
            
            recognized_text = recognize_speech()
            
            if "turn on the light" in recognized_text and not light_on:
                print("Turning on the light as per voice command")
                blue_led.on()
                light_on = True
                insert_command("turn on the light")  # Insert command into database
            
            if "turn off the light" in recognized_text and light_on:
                print("Turning off the light as per voice command")
                blue_led.off()
                light_on = False
                insert_command("turn off the light")  # Insert command into database
            
    except KeyboardInterrupt:
        blue_led.off()  # Turn off the blue LED on exit
        print("Exiting...")
        
if __name__ == "__main__":
    main()
