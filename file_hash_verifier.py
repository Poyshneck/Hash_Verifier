import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import hashlib
import os
import json
from datetime import datetime, timedelta
import threading
import queue
import webbrowser
import sys

class FileHashVerifier:
    def __init__(self, root):
        self.root = root
        self.root.title("File Hash Verifier")
        self.root.geometry("800x600")
        
        # Set theme colors
        self.bg_color = "#f0f0f0"
        self.fg_color = "#000000"
        self.accent_color = "#007bff"
        self.root.configure(bg=self.bg_color)
        
        # Initialize variables
        self.history = []
        self.max_history = 30  # Store last 30 entries
        self.log_dir = os.path.expanduser("~/Documents/FileHashVerifier")
        self.ensure_log_directory()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons
        self.create_buttons()
        
        # Create status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create result text area with tags for formatting
        self.result_text = tk.Text(self.main_frame, height=20, width=80, wrap=tk.WORD)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Configure tags for status formatting
        self.result_text.tag_configure("valid", foreground="green", font=("Arial", 10, "bold"))
        self.result_text.tag_configure("invalid", foreground="red", font=("Arial", 10, "bold"))
        
        # Create scrollbar for result text
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # Load settings
        self.load_settings()
        
        # Set up message queue for thread communication
        self.msg_queue = queue.Queue()
        self.root.after(100, self.check_queue)

    def ensure_log_directory(self):
        """Ensure the log directory exists"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def create_buttons(self):
        """Create the main buttons"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Add help button to main window
        self.create_help_button(button_frame, "main")
        
        buttons = [
            ("Verify Single File", self.verify_single_file),
            ("Compare Two Files", self.compare_files),
            ("Batch Process", self.batch_process),
            ("View History", self.view_history),
            ("Export History", self.export_history),
            ("Change Log Directory", self.change_log_directory),
            ("Light/Dark Mode", self.toggle_theme)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5)

    def calculate_hash(self, file_path, algorithm):
        """Calculate hash of a file"""
        hash_obj = hashlib.new(algorithm)
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating hash: {str(e)}")
            return None

    def show_loading_dialog(self, message="Please wait one moment. Loading hash value options..."):
        """Show a loading dialog"""
        loading_dialog = tk.Toplevel(self.root)
        loading_dialog.title("Processing")
        loading_dialog.geometry("300x100")
        
        # Center the window relative to the main window
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 100) // 2
        loading_dialog.geometry(f"+{x}+{y}")
        
        # Make the dialog modal
        loading_dialog.transient(self.root)
        loading_dialog.grab_set()
        
        # Add message
        ttk.Label(loading_dialog, text=message).pack(pady=10)
        
        # Add progress bar
        progress = ttk.Progressbar(loading_dialog, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start()
        
        return loading_dialog

    def show_help(self, section=None):
        """Show help content for a specific section"""
        try:
            # First try to find the help file in the same directory as the script
            help_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "help.html")
            
            # If not found, try to find it in the PyInstaller bundle
            if not os.path.exists(help_file):
                if getattr(sys, 'frozen', False):
                    # Running in a bundle
                    help_file = os.path.join(sys._MEIPASS, "help.html")
                else:
                    # Running in normal Python environment
                    help_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "help.html")
            
            if not os.path.exists(help_file):
                messagebox.showerror("Error", "Help file not found. Please ensure help.html is in the same directory as the script.")
                return

            url = f"file://{help_file}"
            if section:
                url += f"#{section}"
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Error opening help file: {str(e)}")

    def create_help_button(self, parent, section=None):
        """Create a help button for a window"""
        help_btn = ttk.Button(parent, text="?", width=3, 
                             command=lambda: self.show_help(section))
        help_btn.pack(side=tk.RIGHT, padx=5)
        return help_btn

    def verify_single_file(self):
        """Verify a single file's hash"""
        file_path = filedialog.askopenfilename(title="Select file to verify")
        if not file_path:
            return
            
        # Create algorithm selection dialog
        alg_dialog = tk.Toplevel(self.root)
        alg_dialog.title("Select Hash Algorithm")
        alg_dialog.geometry("300x200")
        
        # Center the algorithm dialog
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        alg_dialog.geometry(f"+{x}+{y}")
        
        # Make the dialog modal
        alg_dialog.transient(self.root)
        alg_dialog.grab_set()
        
        # Add help button
        self.create_help_button(alg_dialog, "verify")
        
        selected_alg = tk.StringVar(value="md5")
        algorithms = [
            ("MD5", "md5"),
            ("SHA-1", "sha1"),
            ("SHA-256", "sha256"),
            ("SHA-512", "sha512")
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(alg_dialog, text=text, value=value, variable=selected_alg).pack(pady=5)
        
        def on_algorithm_selected():
            alg_dialog.destroy()
            
            # Show loading dialog
            loading_dialog = tk.Toplevel(self.root)
            loading_dialog.title("Processing")
            loading_dialog.geometry("300x100")
            
            # Center the loading dialog
            x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
            y = self.root.winfo_y() + (self.root.winfo_height() - 100) // 2
            loading_dialog.geometry(f"+{x}+{y}")
            
            # Make the dialog modal
            loading_dialog.transient(self.root)
            loading_dialog.grab_set()
            
            # Add message
            ttk.Label(loading_dialog, text="Please wait one moment. Loading hash value options...").pack(pady=10)
            
            # Add progress bar
            progress = ttk.Progressbar(loading_dialog, mode='indeterminate')
            progress.pack(pady=10, padx=20, fill=tk.X)
            progress.start()
            
            # Update the UI
            self.root.update()
            
            # Calculate hash
            hash_value = self.calculate_hash(file_path, selected_alg.get())
            
            # Close loading dialog
            loading_dialog.destroy()
            
            # Show hash options if hash was calculated successfully
            if hash_value:
                self.show_hash_options(file_path, hash_value, selected_alg.get())
        
        ttk.Button(alg_dialog, text="OK", command=on_algorithm_selected).pack(pady=10)
        
        # Wait for the dialog to be closed
        self.root.wait_window(alg_dialog)

    def show_hash_options(self, file_path, hash_value, algorithm):
        """Show options for the calculated hash"""
        options_dialog = tk.Toplevel(self.root)
        options_dialog.title("Hash Options")
        options_dialog.geometry("400x300")
        
        # Center the window relative to the main window
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        options_dialog.geometry(f"+{x}+{y}")
        
        # Make the dialog modal
        options_dialog.transient(self.root)
        options_dialog.grab_set()
        
        # Add help button
        self.create_help_button(options_dialog, "verify")
        
        # Display hash information
        ttk.Label(options_dialog, text=f"File: {os.path.basename(file_path)}").pack(pady=5)
        ttk.Label(options_dialog, text=f"Hash ({algorithm.upper()}): {hash_value}").pack(pady=5)
        
        # Create buttons for different options
        ttk.Button(options_dialog, text="Verify Against Hash", 
                  command=lambda: self.verify_against_hash(hash_value, file_path, algorithm)).pack(pady=5)
        ttk.Button(options_dialog, text="Save Hash to File", 
                  command=lambda: self.save_hash_to_file(file_path, hash_value, algorithm)).pack(pady=5)
        ttk.Button(options_dialog, text="Copy Hash to Clipboard", 
                  command=lambda: self.copy_to_clipboard(hash_value)).pack(pady=5)
        ttk.Button(options_dialog, text="Generate Hash File", 
                  command=lambda: self.generate_hash_file(file_path, hash_value, algorithm)).pack(pady=5)
        
        # Wait for the window to be closed
        self.root.wait_window(options_dialog)

    def verify_against_hash(self, calculated_hash, file_path, algorithm):
        """Verify against a known hash"""
        expected_hash = tk.simpledialog.askstring("Hash Verification", 
                                                "Enter the expected hash to verify:")
        if expected_hash:
            verified = calculated_hash.lower() == expected_hash.lower()
            if verified:
                messagebox.showinfo("Success", "Hash verification successful!")
            else:
                messagebox.showerror("Error", "Hash verification failed!")
            
            # Create a new history entry for the verification
            self.add_to_history({
                'file': file_path,
                'hash': calculated_hash,
                'algorithm': algorithm,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'verified': verified,
                'compared_hash': expected_hash
            })
            
            # Update the display immediately
            self.update_history_display()

    def save_hash_to_file(self, file_path, hash_value, algorithm):
        """Save hash to a file"""
        try:
            log_file = os.path.join(self.log_dir, 
                                  f"hash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(log_file, 'w') as f:
                f.write(f"File: {file_path}\n")
                f.write(f"Algorithm: {algorithm.upper()}\n")
                f.write(f"Hash: {hash_value}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            messagebox.showinfo("Success", f"Hash saved to: {log_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving hash: {str(e)}")

    def copy_to_clipboard(self, hash_value):
        """Copy hash to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(hash_value)
        messagebox.showinfo("Success", "Hash copied to clipboard!")

    def generate_hash_file(self, file_path, hash_value, algorithm):
        """Generate a hash file"""
        try:
            hash_file = f"{file_path}.{algorithm}"
            with open(hash_file, 'w') as f:
                f.write(f"{hash_value} *{os.path.basename(file_path)}")
            messagebox.showinfo("Success", f"Hash file generated: {hash_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating hash file: {str(e)}")

    def compare_files(self):
        """Compare two files"""
        file1 = filedialog.askopenfilename(title="Select first file")
        if not file1:
            return
            
        file2 = filedialog.askopenfilename(title="Select second file")
        if not file2:
            return
            
        # Create algorithm selection dialog
        alg_dialog = tk.Toplevel(self.root)
        alg_dialog.title("Select Hash Algorithm")
        alg_dialog.geometry("300x200")
        
        # Center the algorithm dialog
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        alg_dialog.geometry(f"+{x}+{y}")
        
        # Make the dialog modal
        alg_dialog.transient(self.root)
        alg_dialog.grab_set()
        
        # Add help button
        self.create_help_button(alg_dialog, "compare")
        
        selected_alg = tk.StringVar(value="md5")
        algorithms = [
            ("MD5", "md5"),
            ("SHA-1", "sha1"),
            ("SHA-256", "sha256"),
            ("SHA-512", "sha512")
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(alg_dialog, text=text, value=value, variable=selected_alg).pack(pady=5)
        
        def on_algorithm_selected():
            alg_dialog.destroy()
            hash1 = self.calculate_hash(file1, selected_alg.get())
            hash2 = self.calculate_hash(file2, selected_alg.get())
            
            if hash1 and hash2:
                result = f"File 1: {os.path.basename(file1)}\n"
                result += f"Hash: {hash1}\n\n"
                result += f"File 2: {os.path.basename(file2)}\n"
                result += f"Hash: {hash2}\n\n"
                
                verified = hash1 == hash2
                if verified:
                    result += "Result: Files are identical!"
                else:
                    result += "Result: Files are different!"
                
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result)
                
                # Add to history only if files were compared
                self.add_to_history({
                    'file': file1,
                    'hash': hash1,
                    'algorithm': selected_alg.get(),
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'verified': verified,
                    'compared_hash': hash2
                })
                self.add_to_history({
                    'file': file2,
                    'hash': hash2,
                    'algorithm': selected_alg.get(),
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'verified': verified,
                    'compared_hash': hash1
                })
                
                # Update the display immediately
                self.update_history_display()
        
        ttk.Button(alg_dialog, text="OK", command=on_algorithm_selected).pack(pady=10)

    def batch_process(self):
        """Process multiple files"""
        files = filedialog.askopenfilenames(title="Select files to process")
        if not files:
            return
            
        # Create algorithm selection dialog
        alg_dialog = tk.Toplevel(self.root)
        alg_dialog.title("Select Hash Algorithm")
        alg_dialog.geometry("300x200")
        
        selected_alg = tk.StringVar(value="md5")
        algorithms = [
            ("MD5", "md5"),
            ("SHA-1", "sha1"),
            ("SHA-256", "sha256"),
            ("SHA-512", "sha512")
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(alg_dialog, text=text, value=value, variable=selected_alg).pack(pady=5)
        
        def process_files():
            alg_dialog.destroy()
            results = []
            
            for file_path in files:
                hash_value = self.calculate_hash(file_path, selected_alg.get())
                if hash_value:
                    results.append(f"File: {os.path.basename(file_path)}\n")
                    results.append(f"Path: {file_path}\n")
                    results.append(f"Hash: {hash_value}\n\n")
            
            # Save results to file
            try:
                log_file = os.path.join(self.log_dir, 
                                      f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                with open(log_file, 'w') as f:
                    f.writelines(results)
                
                # Display results
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "".join(results))
                self.result_text.insert(tk.END, f"\nResults saved to: {log_file}")
                
                messagebox.showinfo("Success", f"Batch processing complete!\nResults saved to: {log_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving results: {str(e)}")
        
        ttk.Button(alg_dialog, text="Process Files", command=process_files).pack(pady=10)

    def view_history(self):
        """View hash history"""
        self.update_history_display()

    def export_history(self):
        """Export history to file"""
        if not self.history:
            messagebox.showinfo("Info", "No history to export!")
            return
            
        # Create export dialog
        export_dialog = tk.Toplevel(self.root)
        export_dialog.title("Export History")
        export_dialog.geometry("300x200")
        
        # Center the export dialog
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        export_dialog.geometry(f"+{x}+{y}")
        
        # Make the dialog modal
        export_dialog.transient(self.root)
        export_dialog.grab_set()
        
        # Add help button
        self.create_help_button(export_dialog, "export")
        
        # Format selection
        format_var = tk.StringVar(value="html")
        formats = [
            ("HTML", "html"),
            ("PDF", "pdf"),
            ("CSV", "csv"),
            ("JSON", "json")
        ]
        
        for text, value in formats:
            ttk.Radiobutton(export_dialog, text=text, value=value, variable=format_var).pack(pady=5)
        
        def export():
            format_type = format_var.get()
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                filetypes=[(f"{format_type.upper()} files", f"*.{format_type}")]
            )
            
            if not file_path:
                return
                
            try:
                if format_type == "html":
                    self.export_to_html(file_path)
                elif format_type == "pdf":
                    self.export_to_pdf(file_path)
                elif format_type == "csv":
                    self.export_to_csv(file_path)
                elif format_type == "json":
                    self.export_to_json(file_path)
                    
                messagebox.showinfo("Success", f"History exported successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting history: {str(e)}")
            
            export_dialog.destroy()
        
        ttk.Button(export_dialog, text="Export", command=export).pack(pady=10)

    def export_to_html(self, file_path):
        """Export history to HTML format"""
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .valid { color: green; font-weight: bold; }
                .invalid { color: red; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>File Hash Verification History</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>File</th>
                    <th>Algorithm</th>
                    <th>Hash (last 10)</th>
                    <th>Status</th>
                    <th>Compared Hash (last 10)</th>
                </tr>
        """
        
        for entry in self.history:
            status = "Valid Hash" if entry.get('verified', False) else "Invalid Hash"
            status_class = "valid" if entry.get('verified', False) else "invalid"
            hash_display = entry['hash'][-10:] if entry['hash'] else "N/A"
            compared_hash = entry['compared_hash'][-10:] if entry['compared_hash'] else "N/A"
            
            html_content += f"""
                <tr>
                    <td>{entry['date']}</td>
                    <td>{entry['file']}</td>
                    <td>{entry['algorithm'].upper()}</td>
                    <td>{hash_display}</td>
                    <td class="{status_class}">{status}</td>
                    <td>{compared_hash}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def export_to_pdf(self, file_path):
        """Export history to PDF format"""
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Create custom styles
        styles.add(ParagraphStyle(
            name='ValidHash',
            parent=styles['Normal'],
            textColor=colors.green,
            fontSize=10,
            spaceAfter=12
        ))
        styles.add(ParagraphStyle(
            name='InvalidHash',
            parent=styles['Normal'],
            textColor=colors.red,
            fontSize=10,
            spaceAfter=12
        ))
        
        # Add title
        elements.append(Paragraph("Hash Verification History:", styles['Title']))
        elements.append(Spacer(1, 0.25*inch))
        
        if not self.history:
            elements.append(Paragraph("No verification history available.", styles['Normal']))
        else:
            for entry in self.history:
                # Show only last 10 digits of hashes
                hash_display = entry['hash'][-10:] if entry['hash'] else "N/A"
                compared_hash = entry['compared_hash'][-10:] if entry['compared_hash'] else "N/A"
                
                # Add file info
                elements.append(Paragraph(f"File: {os.path.basename(entry['file'])}", styles['Normal']))
                elements.append(Paragraph(f"Path: {entry['file']}", styles['Normal']))
                elements.append(Paragraph(f"Algorithm: {entry['algorithm'].upper()}", styles['Normal']))
                elements.append(Paragraph(f"Hash (last 10): {hash_display}", styles['Normal']))
                elements.append(Paragraph(f"Date: {entry['date']}", styles['Normal']))
                if entry['compared_hash']:
                    elements.append(Paragraph(f"Compared Hash (last 10): {compared_hash}", styles['Normal']))
                
                # Add status with appropriate formatting
                status = "Valid Hash" if entry['verified'] else "Invalid Hash"
                status_style = 'ValidHash' if entry['verified'] else 'InvalidHash'
                elements.append(Paragraph(f"Status: {status}", styles[status_style]))
                elements.append(Spacer(1, 0.1*inch))
        
        doc.build(elements)

    def export_to_csv(self, file_path):
        """Export history to CSV format"""
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'File', 'Algorithm', 'Hash (last 10)', 'Status', 'Compared Hash (last 10)'])
            
            for entry in self.history:
                status = "Valid Hash" if entry.get('verified', False) else "Invalid Hash"
                hash_display = entry['hash'][-10:] if entry['hash'] else "N/A"
                compared_hash = entry['compared_hash'][-10:] if entry['compared_hash'] else "N/A"
                writer.writerow([
                    entry['date'],
                    entry['file'],
                    entry['algorithm'].upper(),
                    hash_display,
                    status,
                    compared_hash
                ])

    def export_to_json(self, file_path):
        """Export history to JSON format"""
        import json
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4)

    def change_log_directory(self):
        """Change the log directory"""
        new_dir = filedialog.askdirectory(title="Select new log directory")
        if new_dir:
            try:
                # Test write permissions
                test_file = os.path.join(new_dir, "test.txt")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                
                self.log_dir = new_dir
                self.save_settings()
                messagebox.showinfo("Success", f"Log directory changed to: {new_dir}")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot write to selected directory: {str(e)}")

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.bg_color == "#f0f0f0":  # Light theme
            self.bg_color = "#2b2b2b"
            self.fg_color = "#ffffff"
            self.accent_color = "#007bff"
        else:  # Dark theme
            self.bg_color = "#f0f0f0"
            self.fg_color = "#000000"
            self.accent_color = "#007bff"
        
        self.root.configure(bg=self.bg_color)
        self.result_text.configure(bg=self.bg_color, fg=self.fg_color)
        self.save_settings()

    def load_settings(self):
        """Load settings from file"""
        try:
            settings_file = os.path.join(self.log_dir, "settings.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.log_dir = settings.get('log_dir', self.log_dir)
                    if settings.get('theme') == 'dark':
                        self.toggle_theme()
        except Exception:
            pass

    def save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'log_dir': self.log_dir,
                'theme': 'dark' if self.bg_color == "#2b2b2b" else 'light'
            }
            settings_file = os.path.join(self.log_dir, "settings.json")
            with open(settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass

    def check_queue(self):
        """Check message queue for updates"""
        try:
            while True:
                message = self.msg_queue.get_nowait()
                self.status_var.set(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def add_to_history(self, entry):
        """Add an entry to history, maintaining only the last 30 entries"""
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def update_history_display(self):
        """Update the main screen with current history"""
        if not self.history:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "No verification history available.")
            return
            
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Hash Verification History:\n\n")
        
        for entry in self.history:
            # Show only last 10 digits of hashes
            hash_display = entry['hash'][-10:] if entry['hash'] else "N/A"
            compared_hash = entry['compared_hash'][-10:] if entry['compared_hash'] else "N/A"
            
            # Insert file info
            self.result_text.insert(tk.END, f"File: {os.path.basename(entry['file'])}\n")
            self.result_text.insert(tk.END, f"Path: {entry['file']}\n")
            self.result_text.insert(tk.END, f"Algorithm: {entry['algorithm'].upper()}\n")
            self.result_text.insert(tk.END, f"Hash (last 10): {hash_display}\n")
            self.result_text.insert(tk.END, f"Date: {entry['date']}\n")
            if entry['compared_hash']:
                self.result_text.insert(tk.END, f"Compared Hash (last 10): {compared_hash}\n")
            
            # Insert status with appropriate formatting
            status = "Valid Hash" if entry['verified'] else "Invalid Hash"
            self.result_text.insert(tk.END, "Status: ")
            self.result_text.insert(tk.END, status, "valid" if entry['verified'] else "invalid")
            self.result_text.insert(tk.END, "\n\n")

def main():
    root = tk.Tk()
    app = FileHashVerifier(root)
    root.mainloop()

if __name__ == "__main__":
    main() 