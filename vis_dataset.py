import os
import cv2
import numpy as np
from bop_toolkit_lib import inout, renderer

# Set paths
dataset_path = '/home/robodev/Documents/BPC/Data/ipd_train_pbr/train_pbr/000000/'  # Path to your dataset
camera_id = 'cam1'                    # Camera ID (e.g., 'cam1')
scene_id = 0                          # Scene ID to visualize
view_id = 0                           # View ID to visualize

# Load camera parameters
camera_file = os.path.join(dataset_path, f'scene_camera_{camera_id}.json')
if os.path.exists(camera_file):
    scene_camera = inout.load_json(camera_file)
    camera_data = scene_camera[str(view_id)]
    K = np.array(camera_data['cam_K']).reshape(3, 3)  # Camera intrinsic matrix
    print("Camera Matrix: \n", K)
else:
    raise FileNotFoundError(f"Camera file not found: {camera_file}")

# Load ground truth poses
gt_file = os.path.join(dataset_path, f'scene_gt_{camera_id}.json')
if os.path.exists(gt_file):
    scene_gt = inout.load_json(gt_file)
    gt_poses = scene_gt[str(view_id)]  # Ground truth poses for the current view
else:
    raise FileNotFoundError(f"Ground truth file not found: {gt_file}")

# Load RGB image
rgb_path = os.path.join(dataset_path, f'rgb_{camera_id}', f'{view_id:06d}.jpg')
if os.path.exists(rgb_path):
    rgb = cv2.imread(rgb_path)
else:
    raise FileNotFoundError(f"RGB image not found: {rgb_path}")

# Initialize renderer
ren = renderer.create_renderer(640, 480, mode='rgb')  # Adjust image size as needed

# Load object models (assuming models are in the BOP format)
models_path = os.path.join(dataset_path, '../models')
import glob
models = glob.glob(os.path.join(models_path, "*.ply"))
for obj_id, obj in enumerate(models):  # Assuming object IDs are sequential
    model_path = obj
    if os.path.exists(model_path):
        ren.add_object(obj_id, model_path)
    else:
        print(f"Model not found: {model_path}")

# Create a copy of the RGB image for overlay
rgb_overlay = rgb.copy()

# Render objects with their ground truth poses
for gt in gt_poses:
    obj_id = gt['obj_id']
    R = np.array(gt['cam_R_m2c']).reshape(3, 3)  # Rotation matrix
    t = np.array(gt['cam_t_m2c'])               # Translation vector
    
    fx = K[0,0]
    fy = K[1,1]
    cx = K[0,2]
    cy = K[1,2]
    # Render the object
    ren.render_object(obj_id, R, t, fx, fy, cx, cy)
    
    # Get the rendered mask and color image
    #rendered_mask = ren.get_mask(obj_id)
    rendered_rgb = ren.get_rgb()

    # Overlay the rendered object onto the RGB image
    #rgb_overlay[rendered_mask > 0] = rendered_rgb[rendered_mask > 0]

# Display the RGB image with overlaid ground truth poses
cv2.imshow(f'RGB Image (Camera {camera_id}, View {view_id}) with Ground Truth Poses', rendered_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()