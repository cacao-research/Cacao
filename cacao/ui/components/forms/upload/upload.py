"""
Upload Component Python Integration
"""

from typing import Dict, Any, Optional, List
from ...base import Component

class Upload(Component):
    """
    Server-side logic for upload component
    """
    
    def __init__(self, multiple: bool = False, disabled: bool = False, 
                 accept: str = None, max_size: int = None, **kwargs):
        """
        Initialize upload component
        
        Args:
            multiple: Whether to allow multiple file uploads
            disabled: Whether upload is disabled
            accept: Accepted file types (e.g., ".jpg,.png,.pdf")
            max_size: Maximum file size in bytes
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.multiple = multiple
        self.disabled = disabled
        self.accept = accept
        self.max_size = max_size
        self.uploaded_files = []
    
    def validate_file(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single file
        
        Args:
            file_info: File information dictionary
            
        Returns:
            Dict containing validation result
        """
        errors = []
        
        # Check file size
        if self.max_size and file_info.get('size', 0) > self.max_size:
            errors.append(f"File size exceeds maximum of {self.max_size} bytes")
        
        # Check file type
        if self.accept:
            file_name = file_info.get('name', '')
            file_ext = '.' + file_name.split('.')[-1] if '.' in file_name else ''
            accepted_types = [t.strip() for t in self.accept.split(',')]
            
            if file_ext not in accepted_types:
                errors.append(f"File type {file_ext} not accepted. Accepted types: {self.accept}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def on_upload(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle file upload
        
        Args:
            files: List of file information dictionaries
            
        Returns:
            Dict containing response data
        """
        if not self.multiple and len(files) > 1:
            return {
                "success": False,
                "error": "Multiple files not allowed",
                "files": []
            }
        
        validated_files = []
        upload_errors = []
        
        for file_info in files:
            validation = self.validate_file(file_info)
            
            if validation["valid"]:
                validated_files.append({
                    **file_info,
                    "status": "uploaded",
                    "upload_time": "now"  # Replace with actual timestamp
                })
            else:
                upload_errors.extend(validation["errors"])
        
        # Update uploaded files list
        if self.multiple:
            self.uploaded_files.extend(validated_files)
        else:
            self.uploaded_files = validated_files
        
        return {
            "success": len(upload_errors) == 0,
            "files": validated_files,
            "errors": upload_errors,
            "total_files": len(self.uploaded_files)
        }
    
    def remove_file(self, file_id: str) -> Dict[str, Any]:
        """
        Remove an uploaded file
        
        Args:
            file_id: ID of file to remove
            
        Returns:
            Dict containing response data
        """
        original_count = len(self.uploaded_files)
        self.uploaded_files = [f for f in self.uploaded_files if f.get('id') != file_id]
        
        return {
            "success": len(self.uploaded_files) < original_count,
            "removed": original_count - len(self.uploaded_files) > 0,
            "remaining_files": len(self.uploaded_files)
        }
    
    def clear_files(self) -> Dict[str, Any]:
        """
        Clear all uploaded files
        
        Returns:
            Dict containing response data
        """
        cleared_count = len(self.uploaded_files)
        self.uploaded_files = []
        
        return {
            "success": True,
            "cleared_count": cleared_count,
            "remaining_files": 0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "multiple": self.multiple,
            "disabled": self.disabled,
            **self.get_base_props()
        }
        
        if self.accept:
            props["accept"] = self.accept
        if self.max_size:
            props["maxSize"] = self.max_size
            
        return {
            "type": "upload",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Upload':
        """
        Create upload component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Upload instance
        """
        return Upload(
            multiple=data.get('multiple', False),
            disabled=data.get('disabled', False),
            accept=data.get('accept'),
            max_size=data.get('maxSize')
        )

def create_upload(multiple: bool = False, disabled: bool = False, accept: str = None,
                 max_size: int = None, **kwargs) -> Dict[str, Any]:
    """Create an upload component"""
    component = Upload(multiple, disabled, accept, max_size, **kwargs)
    return component.to_dict()