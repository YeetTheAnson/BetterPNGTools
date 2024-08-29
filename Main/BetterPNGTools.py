import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from PIL import Image, ImageTk
import sv_ttk
import os
import colorsys
import random
import io
import base64

class PNGToolsApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.pack(fill=tk.BOTH, expand=True)

        self.tools = [
            {"title": "Make a PNG Transparent", "description": "Quickly replace any color in a PNG file with transparency.", "image": "image1.png", "function": self.make_transparent},
            {"title": "Change Colors in a PNG", "description": "Quickly swap colors in a PNG image.", "image": "image2.png", "function": self.change_colors},
            {"title": "Change PNG Color Tone", "description": "Quickly replace all colors in a PNG with a single color tone.", "image": "image3.png", "function": self.change_color_tone},
            {"title": "Change PNG Opacity", "description": "Quickly create a translucent or semi-transparent PNG.", "image": "image4.png", "function": self.change_opacity},
            {"title": "Add Noise to a PNG", "description": "Quickly add noisy pixels to your PNG image.", "image": "image5.png", "function": self.add_noise},
            {"title": "Compress a PNG", "description": "Quickly make a PNG image smaller and reduce its size.", "image": "image6.png", "function": self.compress_png},
            {"title": "Convert PNG to JPG", "description": "Quickly convert a PNG graphics file to a JPEG graphics file.", "image": "image7.png", "function": self.convert_png_to_jpg},
            {"title": "Convert JPG to PNG", "description": "Quickly convert a JPEG graphics file to a PNG graphics file.", "image": "image8.png", "function": self.convert_jpg_to_png},
            {"title": "Convert WebP to PNG", "description": "Quickly convert a WebP image to a PNG", "image": "image9.png", "function": self.convert_webp_to_png},
            {"title": "Convert PNG to WebP", "description": "Quickly convert a PNG image to a WebP image.", "image": "image10.png", "function": self.convert_png_to_webp},
            {"title": "Convert SVG to PNG", "description": "Quickly convert an SVG file to a PNG image.", "image": "image11.png", "function": self.convert_svg_to_png},
            {"title": "Convert PNG to Base64", "description": "Quickly convert a PNG image to base64 encoding.", "image": "image12.png", "function": self.convert_png_to_base64},
            {"title": "Convert Base64 to PNG", "description": "Quickly convert a base64-encoded image to PNG.", "image": "image13.png"},
            {"title": "PNG Viewer", "description": "Quickly open and view a PNG and its components in your browser.", "image": "image14.png"},
            {"title": "Preview a PNG on a Colorful Background", "description": "Quickly show how a PNG looks on various background colors.", "image": "image15.png"},
            {"title": "Remove the Alpha Channel from PNG", "description": "Quickly remove the alpha channel and transparency from a PNG.", "image": "image16.png"},
            {"title": "Fill the Alpha Channel in a PNG", "description": "Quickly fill the alpha channel in a PNG with a specific color.", "image": "image17.png"},
            {"title": "Replace the Alpha Channel in a PNG", "description": "Quickly replace the alpha channel in a PNG with opaque pixels.", "image": "image18.png"},
            {"title": "Extract Alpha Channel from a PNG", "description": "Quickly extract transparent areas (alpha channel) from a PNG.", "image": "image19.png"},
            {"title": "Analyze a PNG", "description": "Quickly get detailed information about a PNG file.", "image": "image20.png"},
            {"title": "Find PNG File Size", "description": "Quickly calculate the file size of a PNG image in bytes or kilobytes.", "image": "image21.png"},
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

        self.tools_canvas.bind("<MouseWheel>", self._on_mousewheel)

        for tool in self.tools:
            self.create_tool_item(tool)

    def _on_mousewheel(self, event):
        self.tools_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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

        if tool["title"] in ["Make a PNG Transparent", "Change Colors in a PNG"]:
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

        elif tool["title"] == "Change PNG Color Tone":
            ttk.Label(color_frame, text="New Color Tone:").grid(row=0, column=0, padx=5, pady=5)
            self.new_color_entry = ttk.Entry(color_frame, width=10)
            self.new_color_entry.grid(row=0, column=1, padx=5, pady=5)
            ttk.Button(color_frame, text="Pick New Color", command=self.pick_color).grid(row=0, column=2, padx=5, pady=5)

        elif tool["title"] == "Change PNG Opacity":
            ttk.Label(color_frame, text="Opacity %:").grid(row=0, column=0, padx=5)
            self.percentage_entry = ttk.Entry(color_frame, width=5)
            self.percentage_entry.grid(row=0, column=1, padx=5)
            self.percentage_entry.insert(0, "100")

        elif tool["title"] == "Compress a PNG":
            ttk.Label(color_frame, text="Compression level:").grid(row=0, column=0, padx=5, pady=5)
            self.compression_level = ttk.Scale(color_frame, from_=0, to=9, orient=tk.HORIZONTAL)
            self.compression_level.grid(row=0, column=1, padx=5, pady=5)
            self.compression_level.set(6)  # Default compression level

        elif tool["title"] == "Add Noise to a PNG":
            self.noise_type = tk.StringVar(value="random")
            ttk.Radiobutton(color_frame, text="Random color noise", variable=self.noise_type, value="random").grid(row=0, column=0, padx=5, pady=5)
            ttk.Radiobutton(color_frame, text="Similar pixel noise", variable=self.noise_type, value="similar").grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(color_frame, text="Noise level %:").grid(row=1, column=0, padx=5, pady=5)
            self.noise_level_entry = ttk.Entry(color_frame, width=5)
            self.noise_level_entry.grid(row=1, column=1, padx=5, pady=5)
            self.noise_level_entry.insert(0, "10")
            
            ttk.Label(color_frame, text="Color similarity %:").grid(row=2, column=0, padx=5, pady=5)
            self.color_similarity_entry = ttk.Entry(color_frame, width=5)
            self.color_similarity_entry.grid(row=2, column=1, padx=5, pady=5)
            self.color_similarity_entry.insert(0, "20")
            
            def toggle_color_similarity(*args):
                if self.noise_type.get() == "similar":
                    self.color_similarity_entry.config(state="normal")
                else:
                    self.color_similarity_entry.config(state="disabled")
            
            self.noise_type.trace("w", toggle_color_similarity)
            toggle_color_similarity()

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
            self.preview_image = self.create_preview(self.original_image)
            self.display_image(self.preview_image, self.before_frame)

    def create_preview(self, image):
        preview = image.copy()
        preview.thumbnail((250, 250))
        return preview
    
    def display_image(self, image, frame):
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
            self.processed_original = self.color_to_transparent(self.original_image, target_color, percentage)
            preview_result = self.color_to_transparent(self.preview_image, target_color, percentage)
            self.display_image(preview_result, self.after_frame)

    def change_colors(self):
        if hasattr(self, 'original_image'):
            target_color = self.color_entry.get()
            new_color = self.new_color_entry.get()
            percentage = float(self.percentage_entry.get()) / 100
            self.processed_original = self.swap_colors(self.original_image, target_color, new_color, percentage)
            preview_result = self.swap_colors(self.preview_image, target_color, new_color, percentage)
            self.display_image(preview_result, self.after_frame)

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
        return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5 / 441.6729559300637 #Refer to github documentation for more info
    
    def change_color_tone(self):
        if hasattr(self, 'original_image'):
            new_tone = self.new_color_entry.get()
            self.processed_original = self.apply_color_tone(self.original_image, new_tone)
            preview_result = self.apply_color_tone(self.preview_image, new_tone)
            self.display_image(preview_result, self.after_frame)

    def apply_color_tone(self, image, new_tone):
        img = image.convert("RGBA")
        data = img.getdata()
        new_data = []
        new_rgb = tuple(int(new_tone[i:i+2], 16) for i in (1, 3, 5))
        new_hsv = colorsys.rgb_to_hsv(*[x/255.0 for x in new_rgb])
        
        for item in data:
            if item[3] != 0:
                r, g, b = item[:3]
                h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                new_r, new_g, new_b = colorsys.hsv_to_rgb(new_hsv[0], new_hsv[1], v)
                new_data.append((int(new_r*255), int(new_g*255), int(new_b*255), item[3]))
            else:
                new_data.append(item)

        img.putdata(new_data)
        return img

    def change_opacity(self):
        if hasattr(self, 'original_image'):
            opacity = float(self.percentage_entry.get()) / 100
            self.processed_original = self.apply_opacity(self.original_image, opacity)
            preview_result = self.apply_opacity(self.preview_image, opacity)
            self.display_image(preview_result, self.after_frame)

    def apply_opacity(self, image, opacity):
        img = image.convert("RGBA")
        data = img.getdata()
        new_data = []
        
        for item in data:
            new_alpha = int(item[3] * opacity)
            new_data.append(item[:3] + (new_alpha,))

        img.putdata(new_data)
        return img
    
    def add_noise(self):
        if hasattr(self, 'original_image'):
            noise_type = self.noise_type.get()
            noise_level = float(self.noise_level_entry.get()) / 100
            color_similarity = float(self.color_similarity_entry.get()) / 100 if noise_type == "similar" else None
            self.processed_original = self.apply_noise(self.original_image, noise_type, noise_level, color_similarity)
            preview_result = self.apply_noise(self.preview_image, noise_type, noise_level, color_similarity)
            self.display_image(preview_result, self.after_frame)

    def apply_noise(self, image, noise_type, noise_level, color_similarity):
        img = image.convert("RGBA")
        width, height = img.size
        pixels = img.load()
        
        for _ in range(int(width * height * noise_level)):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            if noise_type == "random":
                new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
            else:  # similar
                r, g, b, a = pixels[x, y]
                new_r = max(0, min(255, int(r + (random.random() * 2 - 1) * 255 * color_similarity)))
                new_g = max(0, min(255, int(g + (random.random() * 2 - 1) * 255 * color_similarity)))
                new_b = max(0, min(255, int(b + (random.random() * 2 - 1) * 255 * color_similarity)))
                new_color = (new_r, new_g, new_b, a)
            
            pixels[x, y] = new_color
        
        return img

    def compress_png(self):
        if hasattr(self, 'original_image'):
            compression_level = int(self.compression_level.get())
            self.processed_original = self.apply_compression(self.original_image, compression_level)
            preview_result = self.apply_compression(self.preview_image, compression_level)
            self.display_image(preview_result, self.after_frame)

    def apply_compression(self, image, compression_level):
        img = image.convert("RGB")
        output = io.BytesIO()
        img.save(output, format="PNG", optimize=True, quality=95-compression_level*10)
        output.seek(0)
        return Image.open(output)

    def convert_png_to_jpg(self):
        self.current_operation = "convert_png_to_jpg"
        if hasattr(self, 'original_image'):
            self.processed_original = self.apply_png_to_jpg(self.original_image)
            preview_result = self.apply_png_to_jpg(self.preview_image)
            self.display_image(preview_result, self.after_frame)

    def apply_png_to_jpg(self, image):
        return image.convert("RGB")

    def convert_jpg_to_png(self):
        self.current_operation = "convert_jpg_to_png"
        if hasattr(self, 'original_image'):
            self.processed_original = self.apply_jpg_to_png(self.original_image)
            preview_result = self.apply_jpg_to_png(self.preview_image)
            self.display_image(preview_result, self.after_frame)

    def apply_jpg_to_png(self, image):
        return image.convert("RGBA")

    def convert_webp_to_png(self):
        self.current_operation = "convert_webp_to_png"
        if hasattr(self, 'original_image'):
            self.processed_original = self.apply_webp_to_png(self.original_image)
            preview_result = self.apply_webp_to_png(self.preview_image)
            self.display_image(preview_result, self.after_frame)

    def apply_webp_to_png(self, image):
        return image.convert("RGBA")

    def convert_png_to_webp(self):
        self.current_operation = "convert_png_to_webp"
        if hasattr(self, 'original_image'):
            self.processed_original = self.apply_png_to_webp(self.original_image)
            preview_result = self.apply_png_to_webp(self.preview_image)
            self.display_image(preview_result, self.after_frame)

    def apply_png_to_webp(self, image):
        output = io.BytesIO()
        image.save(output, format="WEBP")
        output.seek(0)
        return Image.open(output)

    def convert_svg_to_png(self):
        self.current_operation = "convert_svg_to_png"
        if hasattr(self, 'original_image'):
            self.processed_original = self.apply_svg_to_png(self.original_image)
            preview_result = self.apply_svg_to_png(self.preview_image)
            self.display_image(preview_result, self.after_frame)

    def apply_svg_to_png(self, image):
        return image.convert("RGBA")

    def convert_png_to_base64(self):
        self.current_operation = "convert_png_to_base64"
        if hasattr(self, 'original_image'):
            base64_string = self.apply_png_to_base64(self.original_image)
            text_widget = tk.Text(self.after_frame, wrap=tk.WORD)
            text_widget.insert(tk.END, base64_string)
            text_widget.pack(expand=True, fill=tk.BOTH)

    def apply_png_to_base64(self, image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()


    def save_image(self):
        if not hasattr(self, 'processed_original'):
            return

        file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("WebP files", "*.webp"),
        ]
        
        if hasattr(self, 'current_operation'):
            if self.current_operation == "convert_png_to_jpg":
                default_extension = ".jpg"
                file_types = [("JPEG files", "*.jpg")] + file_types
            elif self.current_operation == "convert_png_to_webp":
                default_extension = ".webp"
                file_types = [("WebP files", "*.webp")] + file_types
            else:
                default_extension = ".png"
        else:
            default_extension = ".png"

        save_path = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=file_types)
        
        if save_path:
            file_extension = os.path.splitext(save_path)[1].lower()
            
            if file_extension == '.png':
                self.processed_original.save(save_path, format="PNG")
            elif file_extension == '.jpg':
                self.processed_original.convert("RGB").save(save_path, format="JPEG")
            elif file_extension == '.webp':
                self.processed_original.save(save_path, format="WebP")

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
