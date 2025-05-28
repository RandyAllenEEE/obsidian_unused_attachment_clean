# -*- coding: utf-8 -*-
import os
import re
import shutil
import urllib.parse
# ! Using markdown hyperlink syntax, if using wiki link syntax, please modify the regular expression matching part.
def clean_unreferenced_images():
    # --- Configuration ---
    # Target trash directory, all unreferenced images will be moved to this directory. It is recommended to set it to .trash under your Obsidian library path.
    trash_dir = r'F:\mdFiles\Obsidian_md\.trash'
    # Define the base path for the directory structure reference in the trash, it is recommended to set it as your Obsidian library path.
    base_path_for_trash_structure = r''

    # The script will scan this directory and its subdirectories for images.
    markdown_dir = r''
    image_dir = r'' 
    # --- End Configuration ---

    print(f"--- Script started ---")
    print(f"Markdown Directory: {markdown_dir}")
    print(f"Image Directory (source of images): {image_dir}")
    print(f"Trash Directory: {trash_dir}")
    print(f"Base path for trash structure reference: {base_path_for_trash_structure}")

    # Normalize paths
    markdown_dir_abs = os.path.abspath(markdown_dir)
    image_dir_abs = os.path.abspath(image_dir)
    trash_dir_abs = os.path.abspath(trash_dir)
    base_path_for_trash_structure_abs = os.path.abspath(base_path_for_trash_structure)

    if not os.path.exists(markdown_dir_abs) or not os.path.isdir(markdown_dir_abs):
        print(f"ERROR: Markdown directory '{markdown_dir_abs}' does not exist or is not a directory.")
        return
    if not os.path.exists(image_dir_abs) or not os.path.isdir(image_dir_abs):
        print(f"ERROR: Image directory '{image_dir_abs}' does not exist or is not a directory.")
        return
    if not os.path.exists(base_path_for_trash_structure_abs) or not os.path.isdir(base_path_for_trash_structure_abs):
        print(f"ERROR: Base path for trash structure '{base_path_for_trash_structure_abs}' does not exist or is not a directory.")
        # This check is important because relpath behavior depends on it.
        return
        
    print(f"All configured directories exist and are accessible.")

    os.makedirs(trash_dir_abs, exist_ok=True)

    referenced_images = set()
    image_link_pattern = re.compile(r'!\[[^\]]*\]\((.*?)\)')
    wikilink_pattern = re.compile(r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|svg|webp|bmp|tiff))\]\]', re.IGNORECASE)

    print("\nScanning Markdown files for references...")
    found_md_files_count = 0
    for root, _, files in os.walk(markdown_dir_abs):
        for file_name in files:
            if file_name.lower().endswith('.md'):
                found_md_files_count += 1
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    matches = image_link_pattern.findall(content)
                    for image_path_full in matches:
                        decoded_path = urllib.parse.unquote(image_path_full.strip())
                        path_without_anchor = decoded_path.split('#')[0]
                        image_name = os.path.basename(path_without_anchor)
                        if image_name:
                            referenced_images.add(image_name)
                    wikilink_matches = wikilink_pattern.findall(content)
                    for wikilink_image_name in wikilink_matches:
                        decoded_name = urllib.parse.unquote(wikilink_image_name.strip())
                        if decoded_name:
                            referenced_images.add(decoded_name)
                except Exception as e:
                    print(f"ERROR: Failed to read or parse '{file_path}': {str(e)}")
    
    if found_md_files_count == 0:
        print("CRITICAL: No .md files found in the markdown directory search.")
    else:
        print(f"Found {found_md_files_count} Markdown files.")
    print(f"Total unique referenced image names found: {len(referenced_images)}")

    # Store tuples of (image_basename, full_image_path, relative_path_for_trash_structure)
    all_images_details = []
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.tiff')
    
    print("\nScanning image directory for actual image files...")
    found_image_files_in_dir_count = 0
    for root, _, files in os.walk(image_dir_abs): # Scan starts from image_dir_abs
        for file_name in files:
            if file_name.lower().endswith(image_extensions):
                found_image_files_in_dir_count += 1
                full_path = os.path.join(root, file_name)
                
                relative_path_for_trash = ""
                try:
                    # Calculate path relative to the defined base_path_for_trash_structure_abs
                    relative_path_for_trash = os.path.relpath(full_path, base_path_for_trash_structure_abs)
                    # Check if the image is outside the base_path_for_trash_structure (e.g., relpath starts with '..')
                    # This can happen if image_dir is not a sub-path of base_path_for_trash_structure
                    if relative_path_for_trash.startswith("..") or os.path.isabs(relative_path_for_trash):
                        print(f"Warning: Image '{full_path}' is outside the defined base structure '{base_path_for_trash_structure_abs}'. It will be placed in the root of the trash directory.")
                        relative_path_for_trash = file_name # Fallback: use basename, place in trash root
                except ValueError:
                    # This typically happens if full_path and base_path_for_trash_structure_abs are on different drives
                    print(f"Warning: Cannot determine relative path for '{full_path}' from '{base_path_for_trash_structure_abs}' (possibly different drives). It will be placed in the root of the trash directory.")
                    relative_path_for_trash = file_name # Fallback: use basename, place in trash root
                
                all_images_details.append(
                    (file_name, full_path, relative_path_for_trash)
                )
    
    if found_image_files_in_dir_count == 0:
        print("CRITICAL: No physical image files (matching extensions) found in the image directory search.")
    else:
        print(f"Found {found_image_files_in_dir_count} physical image files in image directory.")

    unreferenced_count = 0
    print("\nChecking for unreferenced images to move...")
    
    if not all_images_details:
        print("No images found in the image directory to check.")

    for image_basename, src_path, rel_path_for_trash in all_images_details:
        is_referenced = image_basename in referenced_images

        if not is_referenced:
            # Construct destination path using the rel_path_for_trash
            # This rel_path_for_trash already contains the desired subdirectories
            dst_path = os.path.join(trash_dir_abs, rel_path_for_trash)
            
            dst_folder = os.path.dirname(dst_path)
            os.makedirs(dst_folder, exist_ok=True)
            
            # Handle duplicate filenames in the specific target location within trash
            if os.path.exists(dst_path):
                base, ext = os.path.splitext(os.path.basename(dst_path)) # Get basename for renaming
                counter = 1
                new_dst_basename = f"{base}_{counter}{ext}"
                new_dst_path = os.path.join(dst_folder, new_dst_basename)
                while os.path.exists(new_dst_path):
                    counter += 1
                    new_dst_basename = f"{base}_{counter}{ext}"
                    new_dst_path = os.path.join(dst_folder, new_dst_basename)
                dst_path = new_dst_path
            
            try:
                shutil.move(src_path, dst_path)
                unreferenced_count += 1
                print(f"Moved: '{src_path}' -> '{dst_path}'")
            except Exception as e:
                print(f"ERROR: Failed to move '{src_path}' to '{dst_path}': {str(e)}")

    print(f"\nSuccessfully moved {unreferenced_count} unreferenced image files.")
    print(f"--- Script finished ---")

if __name__ == '__main__':
    clean_unreferenced_images()
