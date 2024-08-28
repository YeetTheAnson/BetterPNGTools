import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import sv_ttk
import os

class PNGToolsApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.pack(fill=tk.BOTH, expand=True)

        self.tools = [
            {"title": "Make a PNG Transparent", "description": "Quickly replace any color in a PNG file with transparency.", "image": "image1.png"},
            {"title": "Change Colors in a PNG", "description": "Quickly swap colors in a PNG image.", "image": "image2.png"},
            {"title": "Change PNG Color Tone", "description": "Quickly replace all colors in a PNG with a single color tone.", "image": "image3.png"},
            {"title": "Change PNG Opacity", "description": "Quickly create a translucent or semi-transparent PNG.", "image": "image4.png"},
            {"title": "Add Noise to a PNG", "description": "Quickly add noisy pixels (white noise) to your PNG image.", "image": "image5.png"},
            {"title": "Compress a PNG", "description": "Quickly make a PNG image smaller and reduce its size.", "image": "image6.png"},
            {"title": "Convert PNG to JPG", "description": "Quickly convert a PNG graphics file to a JPEG graphics file.", "image": "image7.png"},
            {"title": "Convert JPG to PNG", "description": "Quickly convert a JPEG graphics file to a PNG graphics file.", "image": "image8.png"},
            {"title": "Convert WebP to PNG", "description": "Quickly convert a WebP image to a PNG", "image": "image9.png"},
        ]

        self.images = []
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=0, minsize=300)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.left_frame = ttk.Frame(self, padding=10)
        self.right_frame = ttk.Frame(self, padding=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.create_left_side()
        self.create_right_side()

    def create_left_side(self):
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(1, weight=1)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_tools)
        self.search_entry = ttk.Entry(self.left_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.tools_frame = ttk.Frame(self.left_frame)
        self.tools_frame.grid(row=1, column=0, sticky="nsew")
        self.tools_canvas = tk.Canvas(self.tools_frame)
        self.scrollbar = ttk.Scrollbar(self.tools_frame, orient=tk.VERTICAL, command=self.tools_canvas.yview)
        self.tools_list = ttk.Frame(self.tools_canvas)
        self.tools_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tools_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tools_canvas.create_window((0, 0), window=self.tools_list, anchor=tk.NW)
        self.tools_list.bind("<Configure>", lambda e: self.tools_canvas.configure(scrollregion=self.tools_canvas.bbox("all")))
        for tool in self.tools:
            self.create_tool_item(tool)

    def create_tool_item(self, tool):
        frame = ttk.Frame(self.tools_list, style="Card.TFrame", padding=5)
        frame.pack(fill=tk.X, padx=5, pady=2)
        image = Image.open(tool["image"])
        image = image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.images.append(photo)
        image_label = ttk.Label(frame, image=photo)
        image_label.pack(side=tk.LEFT, padx=(0, 10))
        title = ttk.Label(frame, text=tool["title"], style="TLabel", font=("Segoe UI", 10, "bold"))
        title.pack(anchor=tk.W)
        description = ttk.Label(frame, text=tool["description"][:50] + "...", style="TLabel", foreground="gray")
        description.pack(anchor=tk.W)
        frame.bind("<Button-1>", lambda e, t=tool: self.show_tool_details(t))
        title.bind("<Button-1>", lambda e, t=tool: self.show_tool_details(t))
        description.bind("<Button-1>", lambda e, t=tool: self.show_tool_details(t))
        self.create_tooltip(description, tool["description"])

    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(self)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        tooltip.configure(bg="#1c1c1c")
        label = ttk.Label(tooltip, text=text, justify=tk.LEFT, style="Tooltip.TLabel", padding=(10, 5), foreground="white", background="#1c1c1c")
        label.pack()

        def enter(event):
            tooltip.deiconify()
            tooltip.lift()
            x = widget.winfo_rootx() + widget.winfo_width() + 10
            y = widget.winfo_rooty()
            tooltip.wm_geometry(f"+{x}+{y}")

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
        tooltip.withdraw()

    def create_right_side(self):
        self.welcome_frame = ttk.Frame(self.right_frame)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
        welcome_label = ttk.Label(self.welcome_frame, text="Welcome to the extensive library of PNG tools", font=("Segoe UI", 16, "bold"))
        welcome_label.pack(pady=20)
        by_label = ttk.Label(self.welcome_frame, text="by Anson", font=("Segoe UI", 12))
        by_label.pack()
        self.tool_details_frame = ttk.Frame(self.right_frame)

    def show_tool_details(self, tool):
        self.welcome_frame.pack_forget()
        self.tool_details_frame.pack(fill=tk.BOTH, expand=True)
        for widget in self.tool_details_frame.winfo_children():
            widget.destroy()
        title = ttk.Label(self.tool_details_frame, text=tool["title"], font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0, 10))
        image = Image.open(tool["image"])
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.images.append(photo)
        image_label = ttk.Label(self.tool_details_frame, image=photo, style="Card.TLabel")
        image_label.pack(pady=10)
        description = ttk.Label(self.tool_details_frame, text=tool["description"], wraplength=400)
        description.pack(pady=10)
        start_button = ttk.Button(self.tool_details_frame, text="Start Now", style="Accent.TButton", command=self.show_upload_interface)
        start_button.pack(pady=20)

    def show_upload_interface(self):
        for widget in self.tool_details_frame.winfo_children():
            widget.destroy()
        drop_frame = ttk.Frame(self.tool_details_frame, relief="solid", height=100, width=300)
        drop_frame.pack(pady=20)
        drop_frame.pack_propagate(0)
        drop_label = ttk.Label(drop_frame, text="Drag and drop your PNG here or click to upload", anchor="center")
        drop_label.pack(expand=True)
        drop_frame.bind("<Button-1>", self.upload_image)
        drop_label.bind("<Button-1>", self.upload_image)
        self.before_frame = ttk.Frame(self.tool_details_frame, relief="solid", width=250, height=250)
        self.after_frame = ttk.Frame(self.tool_details_frame, relief="solid", width=250, height=250)
        self.before_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.after_frame.pack(side=tk.LEFT, padx=20, pady=20)

        self.before_frame.pack_propagate(0)
        self.after_frame.pack_propagate(0)

        save_button = ttk.Button(self.tool_details_frame, text="Save", style="Accent.TButton", command=self.save_image)
        save_button.pack(pady=20)

    def upload_image(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.display_image(file_path, self.before_frame)

    def display_image(self, file_path, frame):
        image = Image.open(file_path)
        image.thumbnail((250, 250))
        photo = ImageTk.PhotoImage(image)
        self.images.append(photo)

        label = ttk.Label(frame, image=photo)
        label.pack()

        if frame == self.before_frame:
            self.converted_image = image

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path and hasattr(self, 'converted_image'):
            self.converted_image.save(save_path)

    def filter_tools(self, *args):
        search_term = self.search_var.get().lower()
        for widget in self.tools_list.winfo_children():
            widget.destroy()

        for tool in self.tools:
            if search_term in tool["title"].lower() or search_term in tool["description"].lower():
                self.create_tool_item(tool)

def main():
    root = tk.Tk()
    root.title("PNG Tools")
    root.geometry("900x700")

    sv_ttk.set_theme("dark")

    app = PNGToolsApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()
