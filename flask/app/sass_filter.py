"""
Custom Flask-Assets filter for Dart Sass CLI
"""
import subprocess
import tempfile
import os
from webassets.filter import Filter


class DartSassFilter(Filter):
    """Custom filter for Dart Sass CLI."""
    
    name = 'dartsass'
    
    def __init__(self, sass_bin='sass', **kwargs):
        super().__init__(**kwargs)
        self.sass_bin = sass_bin
    
    def apply(self, _in, out, **kwargs):
        """Apply Dart Sass compilation."""
        
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.scss', delete=False) as temp_in:
            temp_in.write(_in.read())
            temp_in_path = temp_in.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False) as temp_out:
            temp_out_path = temp_out.name
        
        try:
            # Run Dart Sass CLI
            cmd = [
                self.sass_bin,
                '--style=compressed',
                '--no-source-map',
                temp_in_path,
                temp_out_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Read compiled CSS
            with open(temp_out_path, 'r') as compiled_file:
                compiled_css = compiled_file.read()
            
            # Write to output
            out.write(compiled_css)
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Dart Sass compilation failed: {e.stderr}")
        
        finally:
            # Clean up temporary files
            if os.path.exists(temp_in_path):
                os.unlink(temp_in_path)
            if os.path.exists(temp_out_path):
                os.unlink(temp_out_path)
