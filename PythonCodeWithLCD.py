from gpiozero import DistanceSensor, LED, Buzzer
import tkinter as tk
from tkinter import font
from time import sleep
from RPLCD.i2c import CharLCD

# Initialize the ultrasonic sensor
sensor = DistanceSensor(echo=24, trigger=23, max_distance=5)

# Initialize LEDs and Buzzer
led_far = LED(18)   # GPIO pin for "far" distance LED
led_mid = LED(17)   # GPIO pin for "mid" distance LED
led_close = LED(27) # GPIO pin for "close" distance LED
buzzer = Buzzer(22) # GPIO pin for buzzer

# Initialize I2C LCD (adjust address if necessary)
lcd = CharLCD('PCF8574', 0x27)  # Replace 0x27 with your I2C address if different

# Initialize the Tkinter window
window = tk.Tk()
window.title("Distance Measurement")
custom_font = font.Font(size=30)
window.geometry("800x400")

# Create a label to display the distance
distance_label = tk.Label(window, text="Distance: ", anchor='center', font=custom_font)
distance_label.pack()

# Function to control the LEDs and buzzer based on distance
def control_leds_and_buzzer(distance):
    if distance < 20:  # Close range
        led_close.on()
        led_mid.off()
        led_far.off()
        buzzer.beep(on_time=0.1, off_time=0.1, n=None, background=True)  # Fast beep
    elif distance > 50:  # Far range
        led_close.off()
        led_mid.off()
        led_far.on()
        buzzer.beep(on_time=1, off_time=1, n=None, background=True)  # Slow beep
    else:  # Mid range
        led_close.off()
        led_mid.on()
        led_far.off()
        buzzer.beep(on_time=0.3, off_time=0.3, n=None, background=True)  # Medium beep

# Function to measure distance and update the GUI
def measure_distance():
    distance = int(sensor.distance * 100)
    
    if distance < 20:
        distance_label.config(fg="red", text="Distance: {} cm\nHi!".format(distance))
    elif distance > 50:
        distance_label.config(fg="blue", text="Distance: {} cm\nBye!".format(distance))
    else:
        distance_label.config(fg="green", text="Distance: {} cm\nT_T".format(distance))
    
    # Display the distance on the I2C LCD
    lcd.clear()  # Clear the LCD screen
    lcd.write_string("Distance: {} cm".format(distance))  # Display the distance
    
    # Control the LEDs and buzzer based on the distance
    control_leds_and_buzzer(distance)
    
    window.after(300, measure_distance)  # Schedule the next measurement after 0.3 second

# Start measuring distance
measure_distance()

# Run the Tkinter event loop
window.mainloop()
