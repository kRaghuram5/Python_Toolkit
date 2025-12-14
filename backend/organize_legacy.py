"""
Script to move legacy Python scripts to legacy_scripts folder
Run this after setup to organize the project
"""

import os
import shutil

# Files to move to legacy_scripts
legacy_files = [
    'Extract_PDF_Image.py',
    'Image_to_pdf.py',
    'PDF_TO_IMAGE.py',
    'PDF_to_Text.py',
    'PDF_TO_WORD.py',
    'Reverse_PDF.py',
    'Text_to_pdf.py',
    'word_to_pdf.py'
]

def move_legacy_files():
    """Move legacy scripts to legacy_scripts folder"""
    legacy_dir = 'legacy_scripts'
    
    # Create directory if it doesn't exist
    os.makedirs(legacy_dir, exist_ok=True)
    
    moved_count = 0
    for filename in legacy_files:
        if os.path.exists(filename):
            destination = os.path.join(legacy_dir, filename)
            if not os.path.exists(destination):
                shutil.move(filename, destination)
                print(f"✅ Moved: {filename} -> {legacy_dir}/")
                moved_count += 1
            else:
                print(f"⚠️  Already exists: {destination}")
        else:
            print(f"❌ Not found: {filename}")
    
    if moved_count > 0:
        print(f"\n🎉 Successfully moved {moved_count} files to {legacy_dir}/")
    else:
        print(f"\n✨ All files are already organized!")

if __name__ == "__main__":
    print("=" * 60)
    print("  Organizing Legacy Scripts")
    print("=" * 60)
    print()
    move_legacy_files()
    print()
    print("=" * 60)
