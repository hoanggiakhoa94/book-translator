import re
from pathlib import Path
import logging

def rename_chapters(folder_path: str) -> None:
    """
    Rename all chapter files in a folder to follow numerical order.
    
    Args:
        folder_path: Path to the folder containing chapter files
    """
    # Convert to Path object
    folder = Path(folder_path)
    
    # Get all txt files in the folder
    txt_files = list(folder.glob("*.txt"))
    
    if not txt_files:
        logging.warning(f"No text files found in {folder_path}")
        return
        
    # Sort files by their numerical order
    txt_files.sort(key=lambda x: int(re.search(r'(\d+)', x.stem).group(1)) if re.search(r'(\d+)', x.stem) else 0)
    
    # Rename files
    for i, file_path in enumerate(txt_files, 1):
        try:
            # Create new filename with 4-digit chapter number
            new_name = f"chapter_{i:04d}.txt"
            new_path = file_path.parent / new_name
            
            # Skip if filename is already correct
            if file_path.name == new_name:
                continue
                
            # Rename the file
            file_path.rename(new_path)
            logging.info(f"Renamed {file_path.name} to {new_name}")
            
        except Exception as e:
            logging.error(f"Error renaming {file_path.name}: {str(e)}")

if __name__ == "__main__":
    import sys
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    if len(sys.argv) != 2:
        print("Usage: python rename_chapters.py <folder_path>")
        sys.exit(1)
        
    folder_path = sys.argv[1]
    rename_chapters(folder_path) 