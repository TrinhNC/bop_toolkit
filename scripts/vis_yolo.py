import cv2
# import numpy as np
import matplotlib.pyplot as plt

def visualize_yolo_sample(image_path, annotation_path):
    """
    Visualizes a sample from the YOLO dataset by drawing the bounding boxes on the image.
    
    Args:
    - image_path: Path to the image file.
    - annotation_path: Path to the YOLO annotation text file.
    """
    # Load the image
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    # Read the annotation file
    with open(annotation_path, 'r') as file:
        annotations = file.readlines()

    # Iterate over each annotation and draw the bounding box
    for i, annotation in enumerate(annotations):
        # Parse the annotation: class_id x_center y_center width height
        parts = annotation.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        # Convert normalized coordinates to pixel values
        x_center_px = int(x_center * image_width)
        y_center_px = int(y_center * image_height)
        width_px = int(width * image_width)
        height_px = int(height * image_height)

        # Calculate the top-left and bottom-right corners of the bounding box
        xmin = int(x_center_px - width_px / 2)
        ymin = int(y_center_px - height_px / 2)
        xmax = int(x_center_px + width_px / 2)
        ymax = int(y_center_px + height_px / 2)
        print(i, " ", xmin, " ", ymin)
        # Draw the bounding box on the image
        color = (0, 255, 0)  # Green color for bounding box
        thickness = 2
        image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

        # Optionally, add class label text
        label = f'Class {class_id}'
        font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.putText(image, label, (xmin, ymin - 10), font, 0.6, (255, 0, 0), 2)
        image = cv2.putText(image, str(i), (xmin, ymin - 40), font, 0.6, (255, 0, 0), 2)

    # Display the image with bounding boxes
    # image1 = cv2.resize(image, (640*2, 480*2))
    # cv2.imshow("YOLO Sample Visualization", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    plt.imshow(image)
    plt.show()


# Example usage:
image_path = "/home/robodev/Documents/BPC/bpc_baseline/datasets/yolo_v1/train_obj_0/images/000000_rgb_cam1_000001.jpg"  # Path to the image file
annotation_path = "/home/robodev/Documents/BPC/bpc_baseline/datasets/yolo_v1/train_obj_0/labels/000000_rgb_cam1_000001.txt"  # Path to the corresponding annotation file

visualize_yolo_sample(image_path, annotation_path)
