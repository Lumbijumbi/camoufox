"""
Main GUI application for Camoufox Playwright automation.
"""

import json
import os
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional

from ..pkgman import INSTALL_DIR


class CamoufoxGUI:
    """
    GUI for Camoufox Playwright automation with recording capabilities.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Camoufox Playwright Automation")
        self.root.geometry("900x700")
        
        # Recording state
        self.recording_process: Optional[subprocess.Popen] = None
        self.is_recording = False
        self.output_file: Optional[Path] = None
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🦊 Camoufox Playwright Automation", 
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Target URL section
        url_frame = ttk.LabelFrame(main_frame, text="Target URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.url_entry = ttk.Entry(url_frame, width=60)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.url_entry.insert(0, "https://example.com")
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame, 
            text="Headless Mode", 
            variable=self.headless_var
        ).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Viewport size
        viewport_frame = ttk.Frame(options_frame)
        viewport_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Label(viewport_frame, text="Viewport:").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(viewport_frame, text="Width:").pack(side=tk.LEFT)
        self.viewport_width = ttk.Entry(viewport_frame, width=8)
        self.viewport_width.pack(side=tk.LEFT, padx=(5, 10))
        self.viewport_width.insert(0, "1920")
        
        ttk.Label(viewport_frame, text="Height:").pack(side=tk.LEFT)
        self.viewport_height = ttk.Entry(viewport_frame, width=8)
        self.viewport_height.pack(side=tk.LEFT, padx=5)
        self.viewport_height.insert(0, "1080")
        
        # Language
        lang_frame = ttk.Frame(options_frame)
        lang_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT, padx=(0, 10))
        self.language_entry = ttk.Entry(lang_frame, width=10)
        self.language_entry.pack(side=tk.LEFT)
        self.language_entry.insert(0, "en-US")
        
        # Output format
        format_frame = ttk.Frame(options_frame)
        format_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Label(format_frame, text="Output Format:").pack(side=tk.LEFT, padx=(0, 10))
        self.format_var = tk.StringVar(value="python")
        format_combo = ttk.Combobox(
            format_frame, 
            textvariable=self.format_var,
            values=["python", "python-async", "javascript", "java", "csharp"],
            width=15,
            state="readonly"
        )
        format_combo.pack(side=tk.LEFT)
        
        # Control buttons section
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.record_button = ttk.Button(
            control_frame,
            text="🔴 Start Recording",
            command=self._toggle_recording,
            width=20
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(
            control_frame,
            text="💾 Save Script",
            command=self._save_script,
            state=tk.DISABLED,
            width=20
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(
            control_frame,
            text="🗑️ Clear",
            command=self._clear_output,
            width=15
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready to record",
            foreground="green"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Generated Code", padding="10")
        output_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Text area with scrollbar
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Consolas', 10)
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def _toggle_recording(self):
        """Start or stop recording."""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        """Start recording Playwright actions."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a target URL")
            return
        
        # Create temporary file for output
        self.output_file = Path(tempfile.mktemp(suffix=f".{self._get_file_extension()}"))
        
        # Build command
        cmd = self._build_codegen_command(url)
        
        try:
            # Update UI
            self.is_recording = True
            self.record_button.config(text="⏹️ Stop Recording")
            self.status_label.config(text="Recording in progress...", foreground="red")
            self.url_entry.config(state=tk.DISABLED)
            
            # Start codegen in a separate thread
            threading.Thread(target=self._run_codegen, args=(cmd,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
            self.is_recording = False
            self._reset_ui()
    
    def _run_codegen(self, cmd):
        """Run codegen command in a separate thread."""
        try:
            # Run the command
            self.recording_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for process to complete
            stdout, stderr = self.recording_process.communicate()
            
            # Schedule UI update in main thread
            self.root.after(0, self._on_recording_complete, stdout, stderr)
            
        except Exception as e:
            self.root.after(0, self._on_recording_error, str(e))
    
    def _on_recording_complete(self, stdout, stderr):
        """Handle recording completion."""
        # Read the output file if it exists
        if self.output_file and self.output_file.exists():
            try:
                code = self.output_file.read_text()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, code)
                self.save_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read generated code: {str(e)}")
        
        self._reset_ui()
        self.status_label.config(text="Recording completed", foreground="green")
    
    def _on_recording_error(self, error_msg):
        """Handle recording error."""
        messagebox.showerror("Error", f"Recording failed: {error_msg}")
        self._reset_ui()
    
    def _stop_recording(self):
        """Stop the recording process."""
        if self.recording_process:
            try:
                self.recording_process.terminate()
                self.recording_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.recording_process.kill()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop recording: {str(e)}")
        
        self._reset_ui()
        self.status_label.config(text="Recording stopped", foreground="orange")
    
    def _reset_ui(self):
        """Reset UI to initial state."""
        self.is_recording = False
        self.record_button.config(text="🔴 Start Recording")
        self.url_entry.config(state=tk.NORMAL)
        self.recording_process = None
    
    def _build_codegen_command(self, url: str) -> list:
        """Build the codegen command."""
        cmd = [
            sys.executable,
            "-m",
            "playwright",
            "codegen"
        ]
        
        # Add target URL
        if url:
            cmd.append(url)
        
        # Add output file
        cmd.extend(["-o", str(self.output_file)])
        
        # Add format
        format_value = self.format_var.get()
        if format_value == "python-async":
            cmd.append("--target=python-async")
        elif format_value != "python":
            cmd.append(f"--target={format_value}")
        
        # Add viewport size
        try:
            width = self.viewport_width.get()
            height = self.viewport_height.get()
            if width and height:
                cmd.append(f"--viewport-size={width},{height}")
        except ValueError:
            pass
        
        # Add browser args for Camoufox
        browser_path = INSTALL_DIR / "firefox" / ("firefox.exe" if sys.platform == "win32" else "firefox")
        if browser_path.exists():
            cmd.extend(["--browser", "firefox"])
            cmd.extend(["--browser-path", str(browser_path)])
        
        return cmd
    
    def _get_file_extension(self) -> str:
        """Get file extension based on output format."""
        format_map = {
            "python": "py",
            "python-async": "py",
            "javascript": "js",
            "java": "java",
            "csharp": "cs"
        }
        return format_map.get(self.format_var.get(), "py")
    
    def _save_script(self):
        """Save the generated script to a file."""
        code = self.output_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "No code to save")
            return
        
        # Ask user for save location
        file_types = [
            ("Python files", "*.py"),
            ("JavaScript files", "*.js"),
            ("Java files", "*.java"),
            ("C# files", "*.cs"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="Save Script",
            defaultextension=f".{self._get_file_extension()}",
            filetypes=file_types
        )
        
        if file_path:
            try:
                Path(file_path).write_text(code)
                messagebox.showinfo("Success", f"Script saved to {file_path}")
                self.status_label.config(text=f"Script saved to {file_path}", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save script: {str(e)}")
    
    def _clear_output(self):
        """Clear the output text area."""
        self.output_text.delete(1.0, tk.END)
        self.save_button.config(state=tk.DISABLED)
        self.status_label.config(text="Output cleared", foreground="blue")


def launch_gui():
    """Launch the Camoufox GUI application."""
    root = tk.Tk()
    app = CamoufoxGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
