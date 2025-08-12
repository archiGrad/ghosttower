import os
import json
import glob
import shutil
from datetime import datetime

def archive_existing_models():
    """Archive existing model.glb files to .models folder before new push"""
    for student_folder in glob.glob("*/"):
        student_name = student_folder.rstrip('/')
        platform_path = os.path.join(student_folder, "platform")
        current_model = os.path.join(platform_path, "model.glb")
        
        if os.path.exists(current_model):
            # Create .models folder (hidden)
            models_folder = os.path.join(platform_path, ".models")
            os.makedirs(models_folder, exist_ok=True)
            
            # Create timestamp folder inside .models
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            archive_folder = os.path.join(models_folder, timestamp)
            os.makedirs(archive_folder, exist_ok=True)
            
            # Copy (not move) current model to archive
            archive_path = os.path.join(archive_folder, "model.glb")
            shutil.copy2(current_model, archive_path)
            print(f"Archived {current_model} to {archive_path}")

def generate_timeline_json():
    timeline = {}
    
    # Scan for student folders
    for student_folder in glob.glob("*/"):
        student_name = student_folder.rstrip('/')
        platform_path = os.path.join(student_folder, "platform")
        
        if os.path.exists(platform_path):
            student_models = []
            
            # Get archived models from .models folder
            models_folder = os.path.join(platform_path, ".models")
            if os.path.exists(models_folder):
                for timestamp_folder in sorted(glob.glob(os.path.join(models_folder, "????-??-??_??-??"))):
                    model_file = os.path.join(timestamp_folder, "model.glb")
                    if os.path.exists(model_file):
                        # Parse timestamp from folder name
                        timestamp_str = os.path.basename(timestamp_folder)
                        try:
                            date_obj = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M")
                            student_models.append({
                                "date": date_obj.isoformat(),
                                "path": model_file,
                                "version": len(student_models) + 1
                            })
                        except ValueError:
                            continue
            
            # Get current model
            current_model = os.path.join(platform_path, "model.glb")
            if os.path.exists(current_model):
                mod_time = os.path.getmtime(current_model)
                student_models.append({
                    "date": datetime.fromtimestamp(mod_time).isoformat(),
                    "path": current_model,
                    "version": len(student_models) + 1,
                    "current": True
                })
            
            if student_models:
                timeline[student_name] = student_models
    
    # Write timeline JSON
    with open('timeline.json', 'w') as f:
        json.dump(timeline, f, indent=2)
    
    print(f"Generated timeline.json with {len(timeline)} students")
    return timeline

if __name__ == "__main__":
    # Only archive if this is a push (not initial generation)
    if os.getenv('GITHUB_EVENT_NAME') == 'push':
        archive_existing_models()
    
    generate_timeline_json()
