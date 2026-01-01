import streamlit as st
import os
import shutil
from pathlib import Path
from collections import defaultdict
import time
from typing import Dict, List, Tuple, Optional

# Configure Streamlit page
st.set_page_config(
    page_title="Smart File Organizer",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FileOrganizer:
    """
    Main class for organizing files based on their extensions.
    Handles scanning, categorization, and file operations.
    """
    
    # File extension mapping for categorization
    FILE_CATEGORIES = {
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.ico', '.heic'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.aiff'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
        'Code Files': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala']
    }
    
    def __init__(self):
        """Initialize the FileOrganizer with empty data structures."""
        self.scan_results = []
        self.category_count = defaultdict(int)
        self.total_files = 0
        self.organized_count = 0
        self.errors = []
    
    def validate_directory(self, directory_path: str) -> Tuple[bool, str]:
        """
        Validate if the directory exists and is safe to organize.
        
        Args:
            directory_path (str): Path to the directory to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            path = Path(directory_path)
            
            # Check if path exists and is a directory
            if not path.exists():
                return False, "Directory does not exist"
            
            if not path.is_dir():
                return False, "Path is not a directory"
            
            # Check if it's a system directory (basic protection)
            system_dirs = ['/', '/usr', '/bin', '/sbin', '/etc', '/dev', '/proc', '/sys', 'C:\\Windows']
            if str(path) in system_dirs or any(str(path).lower().startswith(sys_dir.lower()) for sys_dir in system_dirs if sys_dir != '/'):
                return False, "Cannot organize system directories for safety reasons"
            
            # Check write permissions
            if not os.access(path, os.W_OK):
                return False, "No write permission for this directory"
            
            return True, ""
            
        except Exception as e:
            return False, f"Error validating directory: {str(e)}"
    
    def scan_directory(self, directory_path: str) -> List[Dict]:
        """
        Scan the directory for files at the root level and list subfolders.
        Does not access files inside subfolders.

        Args:
            directory_path (str): Path to scan

        Returns:
            List[Dict]: List of file information dictionaries (only for root level files)
        """
        scan_results = []

        try:
            # List items in the directory (no recursive scan)
            for item in os.scandir(directory_path):
                # Skip hidden files and directories
                if item.name.startswith('.') or item.name.startswith('~'):
                    continue

                if item.is_file():
                    # Process files only at the root level
                    file_extension = item.name.lower().split('.')[-1]
                    file_size = item.stat().st_size
                    category = self._categorize_file(f'.{file_extension}')

                    scan_results.append({
                        'filename': item.name,
                        'current_path': str(item.path),
                        'relative_path': str(Path(item.path).relative_to(directory_path)),  # Relative path for files
                        'extension': f'.{file_extension}',
                        'size_bytes': file_size,
                        'size_readable': self._format_file_size(file_size),
                        'category': category,
                        'target_folder': category
                    })
                
                elif item.is_dir():
                    # List subfolders, but do not analyze their contents
                    scan_results.append({
                        'folder_name': item.name,
                        'type': 'folder',
                        'path': str(item.path),
                        'category': 'Subfolder'
                    })

        except Exception as e:
            self.errors.append(f"Error scanning directory: {str(e)}")

        self.scan_results = scan_results
        self.total_files = len([result for result in scan_results if 'filename' in result])  # Count only files

        # Update category counts
        self.category_count = defaultdict(int)
        for file_info in scan_results:
            if 'category' in file_info and file_info['category'] != 'Subfolder':  # Ignore subfolders
                self.category_count[file_info['category']] += 1

        return scan_results
    
    def _categorize_file(self, extension: str) -> str:
        """
        Categorize file based on its extension.
        
        Args:
            extension (str): File extension (e.g., '.pdf')
            
        Returns:
            str: Category name
        """
        for category, extensions in self.FILE_CATEGORIES.items():
            if extension in extensions:
                return category
        return 'Others'
    
    def _format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human readable format.
        
        Args:
            size_bytes (int): File size in bytes
            
        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def organize_files(self, directory_path: str, progress_callback=None) -> Tuple[int, int]:
        """
        Organize files into categorized folders.
        
        Args:
            directory_path (str): Target directory path
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Tuple[int, int]: (success_count, error_count)
        """
        success_count = 0
        error_count = 0
        
        if not self.scan_results:
            return 0, 0
        
        # Create category folders
        category_folders = {}
        base_path = Path(directory_path)
        
        for category in set(file_info['category'] for file_info in self.scan_results if 'filename' in file_info):  # Only files
            folder_path = base_path / category
            try:
                folder_path.mkdir(exist_ok=True)
                category_folders[category] = folder_path
            except Exception as e:
                self.errors.append(f"Error creating folder {category}: {str(e)}")
                error_count += 1
    
        # Move files to their categories
        for idx, file_info in enumerate(self.scan_results):
            if 'filename' in file_info:  # Only move files, ignore subfolders
                try:
                    source_path = Path(file_info['current_path'])
                    target_folder = category_folders.get(file_info['category'], base_path / file_info['category'])
                    target_path = target_folder / file_info['filename']
                    
                    # Handle duplicate file names
                    if target_path.exists():
                        base_name = source_path.stem
                        extension = source_path.suffix
                        counter = 1
                        while target_path.exists():
                            new_filename = f"{base_name}_{counter}{extension}"
                            target_path = target_folder / new_filename
                            counter += 1
                    
                    # Move the file
                    shutil.move(str(source_path), str(target_path))
                    success_count += 1
                    
                    # Update progress
                    if progress_callback:
                        progress_callback(idx + 1, len(self.scan_results))
                
                except Exception as e:
                    error_count += 1
                    self.errors.append(f"Error moving {file_info['filename']}: {str(e)}")
    
        self.organized_count = success_count
        return success_count, error_count


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'organizer' not in st.session_state:
        st.session_state.organizer = FileOrganizer()
    if 'scan_completed' not in st.session_state:
        st.session_state.scan_completed = False
    if 'organization_completed' not in st.session_state:
        st.session_state.organization_completed = False
    if 'selected_directory' not in st.session_state:
        st.session_state.selected_directory = ""


def main():
    """Main application function."""
    initialize_session_state()
    
    # Sidebar
    st.sidebar.title("📁 Smart File Organizer")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    This application automatically organizes your files into categorized folders based on file extensions.
    
    **Categories:**
    - 📄 Documents
    - 🖼️ Images  
    - 🎥 Videos
    - 🎵 Audio
    - 📦 Archives
    - 💻 Code Files
    - 📁 Others
    """)
    
    st.sidebar.markdown("### Safety Features")
    st.sidebar.markdown("""
    - ✓ Validates directory permissions
    - ✓ Prevents system directory organization
    - ✓ Handles duplicate file names
    - ✓ Shows preview before organizing
    - ✓ Comprehensive error handling
    """)
    
    # Main content area
    st.title("🚀 Smart File Organizer")
    st.markdown("Organize your files automatically with intelligent categorization")
    st.markdown("---")
    
    # Directory selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        directory_path = st.text_input(
            "📂 Enter Directory Path:",
            placeholder="e.g., /home/user/Downloads or C:\\Users\\User\\Downloads",
            help="Enter the full path to the directory you want to organize"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📍 Browse", help="Coming soon - Use text input for now"):
            st.info("💡 Please use the text input field above to enter your directory path")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scan_button = st.button("🔍 Scan Directory", type="secondary", use_container_width=True)
    
    with col2:
        preview_button = st.button("📊 Preview Results", type="secondary", use_container_width=True, 
                                   disabled=not st.session_state.scan_completed)
    
    with col3:
        organize_button = st.button("⚡ Organize Files", type="primary", use_container_width=True,
                                   disabled=not st.session_state.scan_completed)
    
    # Handle button actions
    if scan_button and directory_path:
        # Validate directory
        is_valid, error_msg = st.session_state.organizer.validate_directory(directory_path)
        
        if is_valid:
            st.session_state.selected_directory = directory_path
            
            # Scan directory with progress
            with st.spinner("🔍 Scanning directory..."):
                scan_results = st.session_state.organizer.scan_directory(directory_path)
            
            if scan_results:
                st.session_state.scan_completed = True
                st.success(f"✅ Scan completed! Found {len(scan_results)} files.")
            else:
                st.warning("No files found in the directory or error occurred during scanning.")
        else:
            st.error(f"❌ {error_msg}")
    
    elif scan_button and not directory_path:
        st.error("Please enter a directory path first!")
    
    if preview_button and st.session_state.scan_completed:
        st.markdown("---")
        st.header("📊 Scan Results Preview")
        
        organizer = st.session_state.organizer
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Files", organizer.total_files)
        
        with col2:
            st.metric("Categories", len(organizer.category_count))
        
        # Calculate total size, only for files (ignore subfolders)
        total_size = sum(file_info['size_bytes'] for file_info in organizer.scan_results if 'size_bytes' in file_info)
        st.metric("Total Size", organizer._format_file_size(total_size))
        
        with col4:
            st.metric("Average Size", organizer._format_file_size(total_size // organizer.total_files if organizer.total_files > 0 else 0))
        
        # Category distribution
        st.subheader("📈 File Distribution by Category")
        
        if organizer.category_count:
            # Create category chart data
            categories = list(organizer.category_count.keys())
            counts = list(organizer.category_count.values())
            
            # Use columns to show category cards
            cols = st.columns(max(len(categories), 1))
            
            for idx, (category, count) in enumerate(organizer.category_count.items()):
                with cols[idx % len(cols)]:
                    # Category icon mapping
                    icons = {
                        'Documents': '📄', 'Images': '🖼️', 'Videos': '🎥',
                        'Audio': '🎵', 'Archives': '📦', 'Code Files': '💻', 'Others': '📁'
                    }
                    icon = icons.get(category, '📁')
                    
                    st.metric(f"{icon} {category}", count)
        
    if organize_button and st.session_state.scan_completed:
        st.markdown("---")
        st.header("⚡ Organizing Files")
        
        # Progress container
        progress_container = st.empty()
        progress_bar = progress_container.progress(0)
        status_text = st.empty()
        
        def update_progress(current, total):
            progress = int((current / total) * 100)
            progress_bar.progress(progress)
            status_text.text(f"Moving file {current} of {total}...")
        
        # Organize files
        with st.spinner("Organizing files..."):
            success_count, error_count = st.session_state.organizer.organize_files(
                st.session_state.selected_directory,
                progress_callback=update_progress
            )
        
        # Clear progress indicators
        progress_container.empty()
        status_text.empty()
        
        # Show results
        st.session_state.organization_completed = True
        
        st.markdown("---")
        st.header("✅ Organization Complete!")
        
        # Results metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("✅ Files Organized", success_count)
        
        with col2:
            st.metric("❌ Errors", error_count)
        
        with col3:
            success_rate = (success_count / (success_count + error_count) * 100) if (success_count + error_count) > 0 else 0
            st.metric("📊 Success Rate", f"{success_rate:.1f}%")
        
        # Show errors if any
        if st.session_state.organizer.errors:
            st.warning("⚠️ Some errors occurred during organization:")
            for error in st.session_state.organizer.errors[-5:]:  # Show last 5 errors
                st.error(error)
            
            if len(st.session_state.organizer.errors) > 5:
                st.info(f"... and {len(st.session_state.organizer.errors) - 5} more errors")
        
        # Success message
        if success_count > 0:
            st.success(f"🎉 Successfully organized {success_count} files into categorized folders!")
            st.info(f"📁 Check your directory: {st.session_state.selected_directory}")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Smart File Organizer v1.0")


if __name__ == "__main__":
    main()
