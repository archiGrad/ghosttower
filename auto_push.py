import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class PRCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Push to gh-pages")
        self.root.geometry("300x150")
        
        tk.Label(root, text="Push to gh-pages").pack(pady=10)
        
        self.create_button = tk.Button(root, text="Push Changes", 
                                     command=self.push_changes, bg="green", fg="white",
                                     width=20, height=2)
        self.create_button.pack(pady=20)
        
        self.status_label = tk.Label(root, text="Ready", fg="blue")
        self.status_label.pack(pady=10)

    def push_changes(self):
        try:
            self.status_label.config(text="Pushing...", fg="orange")
            self.root.update()
            
            subprocess.run(["git", "checkout", "gh-pages"], check=True, capture_output=True)
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", f"Update from {os.getenv('USERNAME', 'student')}"], check=True, capture_output=True)
            subprocess.run(["git", "push", "origin", "gh-pages"], check=True, capture_output=True)
            
            self.status_label.config(text="Changes Pushed!", fg="green")
            messagebox.showinfo("Success", "Changes pushed to gh-pages!")
                
        except Exception as e:
            self.status_label.config(text="Error occurred", fg="red")
            messagebox.showerror("Error", f"Failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PRCreator(root)
    root.mainloop()
