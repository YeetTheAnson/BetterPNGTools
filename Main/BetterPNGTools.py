import tkinter as tk
from tkinter import ttk
import sv_ttk

class PNGToolsApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.pack(fill=tk.BOTH, expand=True)

        self.tools = [
            {"title": "Make a PNG Transparent", "description": "Quickly replace any color in a PNG file with transparency."},
            {"title": "Change Colors in a PNG", "description": "Quickly swap colors in a PNG image."},
            {"title": "Change PNG Color Tone", "description": "Quickly replace all colors in a PNG with a single color tone."},
            {"title": "Change PNG Opacity", "description": "Quickly create a translucent or semi-transparent PNG."},
            {"title": "Add Noise to a PNG", "description": "Quickly add noisy pixels (white noise) to your PNG image."},
            {"title": "Compress a PNG", "description": "Quickly make a PNG image smaller and reduce its size."},
            {"title": "Convert PNG to JPG", "description": "Quickly convert a PNG graphics file to a JPEG graphics file."},
            {"title": "Convert JPG to PNG", "description": "Quickly convert a JPEG graphics file to a PNG graphics file."},
            {"title": "Convert WebP to PNG", "description": "Quickly convert a WebP image to a PNG"},
        ]

        self.create_widgets()

    def create_widgets(self):
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(self.paned, padding=10)
        self.right_frame = ttk.Frame(self.paned, padding=10)
        self.paned.add(self.left_frame, weight=1)
        self.paned.add(self.right_frame, weight=2)

        self.create_left_side()
        self.create_right_side()

    def create_left_side(self):
        # Search bar
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_tools)
        self.search_entry = ttk.Entry(self.left_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=5, pady=5)

        # Tools list
        self.tools_frame = ttk.Frame(self.left_frame)
        self.tools_frame.pack(fill=tk.BOTH, expand=True)

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

        title = ttk.Label(frame, text=tool["title"], style="TLabel", font=("Segoe UI", 10, "bold"))
        title.pack(anchor=tk.W)

        description = ttk.Label(frame, text=tool["description"][:50] + "...", style="TLabel", foreground="gray")
        description.pack(anchor=tk.W)

        frame.bind("<Button-1>", lambda e, t=tool: self.show_tool_details(t))
        title.bind("<Button-1>", lambda e, t=tool: self.show_tool_details(t))
        description.bind("<Button-1>", lambda e, t=tool: self.show_tool_details(t))

        # Tooltip
        self.create_tooltip(description, tool["description"])

    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(self)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        label = ttk.Label(tooltip, text=text, justify=tk.LEFT, style="Tooltip.TLabel", padding=(5, 2))
        label.pack()

        def enter(event):
            tooltip.deiconify()
            tooltip.lift()
            x = widget.winfo_rootx() + widget.winfo_width()
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

        # Placeholder for image
        image_placeholder = ttk.Label(self.tool_details_frame, text="[Image Placeholder]", style="Card.TLabel", padding=20)
        image_placeholder.pack(pady=10)

        description = ttk.Label(self.tool_details_frame, text=tool["description"], wraplength=400)
        description.pack(pady=10)

        start_button = ttk.Button(self.tool_details_frame, text="Start Now", style="Accent.TButton")
        start_button.pack(pady=20)

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
    root.geometry("800x600")

    sv_ttk.set_theme("light")

    app = PNGToolsApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()