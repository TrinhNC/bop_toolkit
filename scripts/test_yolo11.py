from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("/home/robodev/Documents/BPC/bpc_baseline/runs/detect/train13/weights/best.pt")

# Run inference on 'bus.jpg' with arguments
results = model.predict("bpc_baseline/datasets/yolo_v0/val_obj_0/images/000007_rgb_cam2_000000.png", save=False, imgsz=640, conf=0.3)

for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0]  # Get bounding box coordinates
        conf = box.conf[0]  # Confidence score
        cls = box.cls[0]  # Class ID
        print(f"Class: {int(cls)}, BBox: ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}), Confidence: {conf:.2f}")
