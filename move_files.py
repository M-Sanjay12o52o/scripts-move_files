import os
import shutil
from datetime import datetime

# Define source and destination folders on the Desktop
source_folder = os.path.expanduser("~/Desktop/Gallery/")
destination_folder = os.path.expanduser("~/Desktop/ScreenSaver/")

# Ensure both folders exist
if not os.path.exists(source_folder):
    os.makedirs(source_folder)
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Log file to track moves
log_file = os.path.expanduser("~/Desktop/file_move_log.txt")

# File to track the last moved image
last_moved_file = os.path.expanduser("~/Desktop/last_moved_image.txt")


def log_message(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()}: {message}\n")


# Define image extensions
image_extensions = (".jpg", ".jpeg", ".webp", ".png")

# Get list of image files in source folder
source_images = [
    f
    for f in os.listdir(source_folder)
    if os.path.isfile(os.path.join(source_folder, f))
    and f.lower().endswith(image_extensions)
]

# Move any existing image in destination back to source
for filename in os.listdir(destination_folder):
    if filename.lower().endswith(image_extensions):
        source_path = os.path.join(destination_folder, filename)
        destination_path = os.path.join(source_folder, filename)
        try:
            shutil.move(source_path, destination_path)
            log_message(f"Moved back: {filename} from ScreenSaver to Gallery")
        except Exception as e:
            log_message(f"Error moving back {filename}: {str(e)}")

# Refresh the list of source images after moving back
source_images = [
    f
    for f in os.listdir(source_folder)
    if os.path.isfile(os.path.join(source_folder, f))
    and f.lower().endswith(image_extensions)
]

# Move the next image from source to destination
if source_images:
    source_images.sort()  # Sort alphabetically
    # Read the last moved image (if exists)
    last_moved_image = None
    if os.path.exists(last_moved_file):
        try:
            with open(last_moved_file, "r") as f:
                last_moved_image = f.read().strip()
        except Exception as e:
            log_message(f"Error reading last moved image file: {str(e)}")

    # Find the next image to move
    if last_moved_image and last_moved_image in source_images:
        last_index = source_images.index(last_moved_image)
        next_index = (last_index + 1) % len(source_images)  # Circular rotation
    else:
        next_index = 0  # Start from the first image if no last moved or not found

    selected_image = source_images[next_index]
    source_path = os.path.join(source_folder, selected_image)
    destination_path = os.path.join(destination_folder, selected_image)
    try:
        shutil.move(source_path, destination_path)
        log_message(f"Moved: {selected_image} to {destination_folder}")
        # Update the last moved image file
        with open(last_moved_file, "w") as f:
            f.write(selected_image)
    except Exception as e:
        log_message(f"Error moving {selected_image}: {str(e)}")
else:
    log_message("No images found in Gallery to move")

log_message("Image rotation operation completed.")
