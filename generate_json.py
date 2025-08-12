import os
import json
import glob
from datetime import datetime

def generate_models_json():
    models = []
    
    # Scan for student folders
    for student_folder in glob.glob("*/"):
        student_name = student_folder.rstrip('/')
        
        # Look for platform subfolder
        platform_path = os.path.join(student_folder, "platform")
        if os.path.exists(platform_path):
            # Find GLB files in platform folder
            glb_files = glob.glob(os.path.join(platform_path, "*.glb"))
            
            for glb_file in glb_files:
                model_name = os.path.basename(glb_file)
                
                # Get file modification time
                mod_time = os.path.getmtime(glb_file)
                upload_date = datetime.fromtimestamp(mod_time).isoformat()
                
                models.append({
                    "name": student_name,
                    "modelName": model_name,
                    "modelPath": glb_file,
                    "uploadDate": upload_date
                })
    
    # Write JSON file
    with open('models.json', 'w') as f:
        json.dump(models, f, indent=2)
    
    print(f"Generated models.json with {len(models)} models")
    return models

if __name__ == "__main__":
    generate_models_json()
