import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from PIL import Image, ImageTk
import sv_ttk
import os
import colorsys

class PNGToolsApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.pack(fill=tk.BOTH, expand=True)

        self.tools = [
            {"title": "Make a PNG Transparent", "description": "Quickly replace any color in a PNG file with transparency.", "image": "image1.png", "function": self.make_transparent},
            {"title": "Change Colors in a PNG", "description": "Quickly swap colors in a PNG image.", "image": "image2.png", "function": self.change_colors},
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
        image = image.resize((50, 50), Image.LANCZOS)
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
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.images.append(photo)
        image_label = ttk.Label(self.tool_details_frame, image=photo, style="Card.TLabel")
        image_label.pack(pady=10)
        description = ttk.Label(self.tool_details_frame, text=tool["description"], wraplength=400)
        description.pack(pady=10)
        start_button = ttk.Button(self.tool_details_frame, text="Start Now", style="Accent.TButton", command=lambda: self.show_upload_interface(tool))
        start_button.pack(pady=20)

    def show_upload_interface(self, tool):
        for widget in self.tool_details_frame.winfo_children():
            widget.destroy()

        drop_frame = ttk.Frame(self.tool_details_frame, style="Dotted.TFrame", height=100, width=300)
        drop_frame.pack(pady=20)
        drop_frame.pack_propagate(0)
        drop_label = ttk.Label(drop_frame, text="Drag and drop your PNG here or click to upload", anchor="center")
        drop_label.pack(expand=True)
        drop_frame.bind("<Button-1>", lambda e: self.upload_image(e, tool))
        drop_label.bind("<Button-1>", lambda e: self.upload_image(e, tool))
        container = ttk.Frame(self.tool_details_frame)
        container.pack(expand=True, fill=tk.BOTH)
        self.before_frame = ttk.Frame(container, style="Grey.TFrame", width=250, height=250)
        self.after_frame = ttk.Frame(container, style="Grey.TFrame", width=250, height=250)
        self.before_frame.grid(row=0, column=0, padx=(0, 10), pady=20)
        self.after_frame.grid(row=0, column=1, padx=(10, 0), pady=20)
        self.before_frame.grid_propagate(False)
        self.after_frame.grid_propagate(False)
        color_frame = ttk.Frame(container)
        color_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(color_frame, text="Color:").grid(row=0, column=0, padx=5)
        self.color_entry = ttk.Entry(color_frame, width=10)
        self.color_entry.grid(row=0, column=1, padx=5)
        ttk.Button(color_frame, text="Pick Color", command=self.pick_color).grid(row=0, column=2, padx=5)
        ttk.Label(color_frame, text="Closeness %:").grid(row=0, column=3, padx=5)
        self.percentage_entry = ttk.Entry(color_frame, width=5)
        self.percentage_entry.grid(row=0, column=4, padx=5)
        self.percentage_entry.insert(0, "10")

        if tool["title"] == "Change Colors in a PNG":
            ttk.Label(color_frame, text="New Color:").grid(row=1, column=0, padx=5, pady=5)
            self.new_color_entry = ttk.Entry(color_frame, width=10)
            self.new_color_entry.grid(row=1, column=1, padx=5, pady=5)
            ttk.Button(color_frame, text="Pick New Color", command=lambda: self.pick_color(True)).grid(row=1, column=2, padx=5, pady=5)

        apply_button = ttk.Button(container, text="Apply", style="Accent.TButton", command=lambda: tool["function"]())
        apply_button.grid(row=2, column=0, columnspan=2, pady=10)
        save_button = ttk.Button(container, text="Save", style="Accent.TButton", command=self.save_image)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

    def upload_image(self, event, tool):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.before_frame)

    def display_image(self, image, frame):
        image.thumbnail((250, 250))
        photo = ImageTk.PhotoImage(image)
        self.images.append(photo)

        for widget in frame.winfo_children():
            widget.destroy()

        label = ttk.Label(frame, image=photo)
        label.pack()

    def pick_color(self, is_new_color=False):
        color = colorchooser.askcolor(title="Pick a color")
        if color:
            hex_color = color[1]
            if is_new_color:
                self.new_color_entry.delete(0, tk.END)
                self.new_color_entry.insert(0, hex_color)
            else:
                self.color_entry.delete(0, tk.END)
                self.color_entry.insert(0, hex_color)

    def make_transparent(self):
        if hasattr(self, 'original_image'):
            target_color = self.color_entry.get()
            percentage = float(self.percentage_entry.get()) / 100
            result_image = self.color_to_transparent(self.original_image, target_color, percentage)
            self.display_image(result_image, self.after_frame)
            self.converted_image = result_image

    def change_colors(self):
        if hasattr(self, 'original_image'):
            target_color = self.color_entry.get()
            new_color = self.new_color_entry.get()
            percentage = float(self.percentage_entry.get()) / 100
            result_image = self.swap_colors(self.original_image, target_color, new_color, percentage)
            self.display_image(result_image, self.after_frame)
            self.converted_image = result_image

    def color_to_transparent(self, image, target_color, threshold):
        img = image.convert("RGBA")
        data = img.getdata()
        new_data = []
        target_rgb = tuple(int(target_color[i:i+2], 16) for i in (1, 3, 5))
        
        for item in data:
            if self.color_distance(item[:3], target_rgb) <= threshold:
                new_data.append((item[0], item[1], item[2], 0))
            else:
                new_data.append(item)

        img.putdata(new_data)
        return img

    def swap_colors(self, image, target_color, new_color, threshold):
        img = image.convert("RGBA")
        data = img.getdata()
        new_data = []
        target_rgb = tuple(int(target_color[i:i+2], 16) for i in (1, 3, 5))
        new_rgb = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5))
        
        for item in data:
            if self.color_distance(item[:3], target_rgb) <= threshold:
                new_data.append(new_rgb + (item[3],))
            else:
                new_data.append(item)

        img.putdata(new_data)
        return img

    def color_distance(self, color1, color2):
        return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5 / 441.6729559300637

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
    style = ttk.Style()
    style.configure("Dotted.TFrame", borderwidth=2, relief="solid")
    style.configure("Grey.TFrame", borderwidth=2, relief="solid", bordercolor="grey")
    root.option_add("*Dotted.TFrame.borderwidth", 2)
    root.option_add("*Dotted.TFrame.relief", "solid")
    root.option_add("*Dotted.TFrame.highlightbackground", "grey")
    root.option_add("*Dotted.TFrame.highlightcolor", "grey")
    root.option_add("*Dotted.TFrame.highlightthickness", 1)
    root.option_add("*Dotted.TFrame.bd", 0)

    def apply_rounded_corners(widget):
        widget.update_idletasks()
        width = widget.winfo_width()
        height = widget.winfo_height()
        shape = f"M0,0 L{width},0 L{width},{height} L0,{height} Z M10,1 L1,10 L1,{height-10} L10,{height-1} L{width-10},{height-1} L{width-1},{height-10} L{width-1},10 L{width-10},1 Z"
        widget.create_polygon(shape, outline="grey", fill="", width=2, stipple="gray50")

    app = PNGToolsApp(root)

    root.after(100, lambda: apply_rounded_corners(app.tool_details_frame.winfo_children()[0]))

    root.mainloop()

if __name__ == "__main__":
    main()