import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import json
from datetime import datetime

class DockerManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Docker Manager")
        self.root.geometry("800x600")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.containers_tab = ttk.Frame(self.notebook)
        self.images_tab = ttk.Frame(self.notebook)
        self.logs_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.containers_tab, text='Containers')
        self.notebook.add(self.images_tab, text='Images')
        self.notebook.add(self.logs_tab, text='Logs')
        
        # Initialize tabs
        self.init_containers_tab()
        self.init_images_tab()
        self.init_logs_tab()
        
        # Refresh data periodically
        self.root.after(5000, self.refresh_data)

    def init_containers_tab(self):
        # Buttons frame
        btn_frame = ttk.Frame(self.containers_tab)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_containers).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Start", command=self.start_container).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Stop", command=self.stop_container).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Remove", command=self.remove_container).pack(side='left', padx=2)
        
        # Containers treeview
        columns = ('ID', 'Name', 'Image', 'Status', 'Ports')
        self.containers_tree = ttk.Treeview(self.containers_tab, columns=columns, show='headings')
        
        for col in columns:
            self.containers_tree.heading(col, text=col)
            self.containers_tree.column(col, width=100)
        
        self.containers_tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.containers_tab, orient='vertical', command=self.containers_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.containers_tree.configure(yscrollcommand=scrollbar.set)

    def init_images_tab(self):
        # Buttons frame
        btn_frame = ttk.Frame(self.images_tab)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_images).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Pull", command=self.pull_image).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Remove", command=self.remove_image).pack(side='left', padx=2)
        
        # Images treeview
        columns = ('Repository', 'Tag', 'ID', 'Size')
        self.images_tree = ttk.Treeview(self.images_tab, columns=columns, show='headings')
        
        for col in columns:
            self.images_tree.heading(col, text=col)
            self.images_tree.column(col, width=100)
        
        self.images_tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.images_tab, orient='vertical', command=self.images_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.images_tree.configure(yscrollcommand=scrollbar.set)

    def init_logs_tab(self):
        self.log_text = scrolledtext.ScrolledText(self.logs_tab)
        self.log_text.pack(expand=True, fill='both', padx=5, pady=5)

    def refresh_data(self):
        self.refresh_containers()
        self.refresh_images()
        self.root.after(5000, self.refresh_data)

    def run_docker_command(self, command):
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            
            if process.returncode != 0:
                raise Exception(error.decode())
            
            return output.decode()
        except Exception as e:
            self.log_error(f"Error running command '{command}': {str(e)}")
            return None

    def refresh_containers(self):
        # Clear existing items
        for item in self.containers_tree.get_children():
            self.containers_tree.delete(item)
            
        # Get containers data
        output = self.run_docker_command('docker ps -a --format "{{json .}}"')
        if output:
            containers = [json.loads(line) for line in output.splitlines()]
            for container in containers:
                self.containers_tree.insert('', 'end', values=(
                    container.get('ID', '')[:12],
                    container.get('Names', ''),
                    container.get('Image', ''),
                    container.get('Status', ''),
                    container.get('Ports', '')
                ))

    def refresh_images(self):
        # Clear existing items
        for item in self.images_tree.get_children():
            self.images_tree.delete(item)
            
        # Get images data
        output = self.run_docker_command('docker images --format "{{json .}}"')
        if output:
            images = [json.loads(line) for line in output.splitlines()]
            for image in images:
                self.images_tree.insert('', 'end', values=(
                    image.get('Repository', ''),
                    image.get('Tag', ''),
                    image.get('ID', '')[:12],
                    image.get('Size', '')
                ))

    def start_container(self):
        selected = self.containers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a container to start")
            return
            
        container_id = self.containers_tree.item(selected[0])['values'][0]
        output = self.run_docker_command(f'docker start {container_id}')
        if output:
            self.log_message(f"Started container {container_id}")
            self.refresh_containers()

    def stop_container(self):
        selected = self.containers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a container to stop")
            return
            
        container_id = self.containers_tree.item(selected[0])['values'][0]
        output = self.run_docker_command(f'docker stop {container_id}')
        if output:
            self.log_message(f"Stopped container {container_id}")
            self.refresh_containers()

    def remove_container(self):
        selected = self.containers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a container to remove")
            return
            
        container_id = self.containers_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this container?"):
            output = self.run_docker_command(f'docker rm {container_id}')
            if output:
                self.log_message(f"Removed container {container_id}")
                self.refresh_containers()

    def pull_image(self):
        image_name = tk.simpledialog.askstring("Pull Image", "Enter image name (e.g., ubuntu:latest):")
        if image_name:
            output = self.run_docker_command(f'docker pull {image_name}')
            if output:
                self.log_message(f"Pulled image {image_name}")
                self.refresh_images()

    def remove_image(self):
        selected = self.images_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an image to remove")
            return
            
        image_id = self.images_tree.item(selected[0])['values'][2]
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this image?"):
            output = self.run_docker_command(f'docker rmi {image_id}')
            if output:
                self.log_message(f"Removed image {image_id}")
                self.refresh_images()

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')

    def log_error(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] ERROR: {message}\n")
        self.log_text.see('end')
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    # Set window icon
    icon_path = "/usr/share/icons/hicolor/scalable/apps/docker-manager.svg"
    if os.path.exists(icon_path):
        try:
            # Convert SVG to PNG in memory (Tkinter doesn't directly support SVG)
            import cairosvg
            import io
            from PIL import Image, ImageTk
            
            png_data = cairosvg.svg2png(url=icon_path)
            icon_image = Image.open(io.BytesIO(png_data))
            icon_photo = ImageTk.PhotoImage(icon_image)
            root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Failed to load icon: {e}")
    
    app = DockerManagerApp(root)
    root.mainloop()