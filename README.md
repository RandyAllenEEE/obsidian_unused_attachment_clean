# obsidian_unused_attachment_clean
A Python script for deleting unreferenced attachments in markdown files within the Obsidian environment

## Purpose
The script scans a specified directory with markdown files for references to images (via Markdown link syntax) and compares them to the images found in a specified image directory. Unreferenced images are moved to a trash directory for review or deletion.

## Usage
Run the script using:
```bash
python file_clean.py
```

Before running the script, you must configure the paths in the script to match your directory structure. See the configuration section below for details.

## Configuration
You need to edit the following variables in the `file_clean.py` script under the `Configuration` section to match your environment:

1. **`trash_dir`**:
   - **Description**: The directory where unreferenced images will be moved. It is recommended to set this to a `.trash` folder under your Obsidian library or project root.
   - **Example**: `trash_dir = r'F:\mdFiles\Obsidian_md\.trash'`
   - **Note**: Ensure you have write permissions for this directory. The script will create it if it doesn't exist.

2. **`base_path_for_trash_structure`**:
   - **Description**: The base path used to maintain the relative directory structure of moved images in the trash directory. It is recommended to set this to your Obsidian library root or the parent directory of your image folder.
   - **Example**: `base_path_for_trash_structure = r'F:\mdFiles\Obsidian_md'`
   - **Note**: If this is not set or is invalid, images may be moved to the root of the trash directory without preserving their original structure.

3. **`markdown_dir`**:
   - **Description**: The directory containing your Markdown files (`.md`). The script will recursively scan this directory and its subdirectories for image references.
   - **Example**: `markdown_dir = r'F:\mdFiles\Obsidian_md\notes'`
   - **Note**: Ensure this path exists and is readable.

4. **`image_dir`**:
   - **Description**: The directory containing your image files. The script will recursively scan this directory for images to check against references in Markdown files.
   - **Example**: `image_dir = r'F:\mdFiles\Obsidian_md\attachments'`
   - **Note**: Ensure this path exists and is readable.

## Supported Image Formats
The script checks for the following image file extensions (case-insensitive):
- `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.bmp`, `.tiff`
you can change them if you want.

## Supported Link Syntax
- **Markdown Syntax**: `![alt text](path/to/image.png)`
- **Wiki Link Syntax**: `![[image.png]]` (Note: If you use a different syntax, you may need to modify the regular expressions in the script.)

## Important Notes and Warnings
- **Backup First**: Always back up your files before running the script. While the script moves files to a trash directory (instead of deleting them), errors or misconfigurations could result in data loss.
- **Path Accuracy**: Double-check the configured paths (`trash_dir`, `base_path_for_trash_structure`, `markdown_dir`, `image_dir`). Incorrect paths may lead to unexpected behavior or errors.
- **Relative Structure in Trash**: The script attempts to preserve the relative directory structure of moved images in the trash directory based on `base_path_for_trash_structure`. If the image directory is outside this base path or on a different drive, images will be placed in the root of the trash directory.
- **Duplicate Handling**: If a file with the same name already exists in the target trash location, the script will append a number to the filename (e.g., `image_1.png`) to avoid overwriting.
- **Permissions**: Ensure you have appropriate read/write permissions for all configured directories.
- **Error Handling**: The script includes basic error checking and will log issues (e.g., missing directories, unreadable files) to the console. Review the output for any warnings or errors.
- **No Undo**: The script does not provide an automatic undo feature. You can manually move files back from the trash directory if needed.

## Output
When the script runs, it will print detailed logs to the console, including:
- The configured directories being used.
- The number of Markdown files scanned.
- The number of image references found.
- The number of physical image files found.
- Details of each unreferenced image moved to the trash directory.
- A summary of the total unreferenced images moved.

## Troubleshooting
- **Error: Directory does not exist**: Verify that all configured paths exist and are correctly spelled.
- **No Markdown files found**: Ensure `markdown_dir` points to a directory containing `.md` files.
- **No image files found**: Ensure `image_dir` points to a directory containing image files with supported extensions.
- **Images not moved as expected**: Check if `base_path_for_trash_structure` is correctly set to maintain the desired structure in the trash directory.
