import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

# Create an I2C interface and initialize the SH1106 OLED display
serial = i2c(port=1, address=0x3C)  # Use 0x3C for SH1106
device = sh1106(serial)

# Clear the display
device.clear()

# Function to display a message
def display_message(message):
    with canvas(device) as draw:
        draw.text((10, 10), message, fill="white")

# Main function to test the OLED display
def main():
    while True:
        display_message("Hello, World!")
        time.sleep(1)  # Hold the message for 1 second

if __name__ == "__main__":
    main()
