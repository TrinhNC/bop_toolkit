from ultralytics import YOLO

# Load a model
model = YOLO("yolo11x.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="/home/robodev/Documents/BPC/bop_toolkit/scripts/yolo11_bop.yaml", epochs=500, imgsz=640, batch=-1)