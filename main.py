import pyautogui
import time
from PIL import ImageChops
import pytesseract

# Define the coordinates of the area you want to monitor
x1, y1, x2, y2 = 637, 671, 733, 714

# Initialize a variable to store the previous screenshot
previous_screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
previous_screenshot.save("screenshot.png")
# Define the time interval (in seconds) for monitoring
interval = 0.5  # You can adjust this as needed

while True:
    time.sleep(interval)

    # Capture the current screenshot of the defined area
    current_screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    # Calculate the absolute difference between the current and previous screenshots
    diff = ImageChops.difference(current_screenshot, previous_screenshot)

    # Convert the difference image to grayscale
    diff = diff.convert('L')

    # Threshold the difference image to highlight changes
    threshold = 10  # Adjust this threshold value as needed
    diff = diff.point(lambda p: p > threshold and 255)

    # Calculate the sum of pixel values in the thresholded image
    pixel_sum = sum(diff.getdata())

    # You can set a threshold for the change detection
    # If the pixel sum exceeds the threshold, consider it as a change
    if pixel_sum > 1000:  # Adjust the threshold as needed
        print("Change detected in the specified area.")

        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        # Perform OCR on the current screenshot to extract numerical values
        extracted_text = pytesseract.image_to_string(current_screenshot)

        # Assuming you expect numerical values in the extracted text
        # You can further process the extracted_text to filter out non-numeric characters
        numeric_text = ''.join(filter(str.isdigit, extracted_text))

        # Print the extracted numerical values
        if numeric_text:
            print(f"Extracted numerical values: {numeric_text}")
        else:
            print("No numerical values found in the extracted text.")

    # Update the previous screenshot
    previous_screenshot = current_screenshot
