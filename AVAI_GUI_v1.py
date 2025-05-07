import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# API URL
API_URL = "http://10.0.0.251:5000/generate"

def get_ai_response(prompt):
    data = {"prompt": prompt, "max_tokens": 100}
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            return response.json()['output']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error contacting API: {e}"

def on_submit():
    prompt = entry_prompt.get()
    if prompt.strip() == "":
        messagebox.showwarning("Input Error", "Please enter a prompt!")
        return

    ai_output = get_ai_response(prompt)
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, ai_output)
    lines = ai_output.count('\n') + 1
    text_output.config(height=min(lines, 30))
    text_output.config(state=tk.DISABLED)

# Colors
color_bg = "#1E1E1E"        # Space Grey
color_fg = "#CCCCFF"        # Periwinkle
color_periwinkle = "#AEB8FF"
color_text_output_fg = "#1E1E1E"  # Space grey text
color_text_output_bg = "#1E1E1E"  # Space Grey background for output box
color_entry_bg = "#2C2C2E"  # Cool grey for input box
color_entry_fg = "#CCCCFF"  # Periwinkle text in input box

font_main = ("Segoe UI", 12)
font_label = ("Segoe UI", 14, "underline")
font_title = ("Open Sans", 24, "bold")  # Softer font for the title
font_slogan = ("Open Sans", 16, "italic")  # Softer, italicized font for the slogan

# Root window
root = tk.Tk()
root.title("ArtVandelAI - Importer/Exporter")
root.geometry("800x700")
root.configure(bg=color_bg)

# --- Title and Logo ---
frame_header = tk.Frame(root, bg=color_bg)
frame_header.pack(pady=25)

# Load logo
try:
    logo_image = Image.open("peri.png")
    logo_image = logo_image.resize((96, 96), Image.Resampling.LANCZOS)  # Made logo larger
    logo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(frame_header, image=logo, bg=color_bg)
    logo_label.pack(side=tk.LEFT, padx=10)
except Exception as e:
    print(f"Failed to load logo: {e}")

# Title and slogan
title_text = tk.Label(frame_header, text="ArtVandelAI", fg=color_fg, bg=color_bg, font=font_title)
title_text.pack(side=tk.LEFT, padx=5)

slogan_text = tk.Label(root, text="Importer/Exporter", fg=color_fg, bg=color_bg, font=font_slogan)
slogan_text.pack(side=tk.LEFT, padx=5)

# --- Prompt Label ---
label_prompt = tk.Label(root, text="Enter your prompt:", fg=color_fg, bg=color_bg, font=font_label)
label_prompt.pack(pady=12)

# --- Entry Box with Rounded Corners (Oval Shape) ---
entry_prompt = tk.Entry(root, width=60, bg=color_entry_bg, fg=color_entry_fg, font=font_main,
                        insertbackground=color_entry_fg, relief=tk.FLAT, highlightthickness=1,
                        highlightbackground="#3D3D3F", highlightcolor=color_fg, bd=0, 
                        borderwidth=0)  # No border for a clean look
entry_prompt.pack(pady=5, ipady=10)

# Add shadow effect using an extra frame and positioning
entry_shadow = tk.Frame(root, bg="#3D3D3F", width=entry_prompt.winfo_width() + 10, height=entry_prompt.winfo_height() + 10, bd=0)
entry_shadow.pack_propagate(False)
entry_shadow.place(x=entry_prompt.winfo_x() - 5, y=entry_prompt.winfo_y() - 5)

# --- Submit Button with Rounded Corners, Space Grey, and Periwinkle ---
def on_enter(e): btn_submit.config(bg=color_periwinkle)
def on_leave(e): btn_submit.config(bg=color_bg)

btn_submit = tk.Button(root, text="→", command=on_submit, font=("Segoe UI", 18), relief=tk.FLAT,
                       bg=color_bg, fg=color_periwinkle, activebackground=color_periwinkle, 
                       activeforeground=color_bg, width=4, height=1, bd=2, 
                       highlightthickness=0, highlightbackground=color_periwinkle, 
                       highlightcolor=color_periwinkle)
btn_submit.pack(pady=20)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

# --- Output Box with Rounded Corners and Shadow Effect ---
text_output = tk.Text(root, height=10, width=90, wrap=tk.WORD, relief=tk.FLAT, bd=0,
                      state=tk.DISABLED, bg=color_text_output_bg, fg=color_text_output_fg, font=font_main)
text_output.pack(pady=10, padx=20)

# Add shadow effect behind the output box
output_shadow = tk.Frame(root, bg="#3D3D3F", width=text_output.winfo_width() + 10, height=text_output.winfo_height() + 10, bd=0)
output_shadow.pack_propagate(False)
output_shadow.place(x=text_output.winfo_x() - 5, y=text_output.winfo_y() - 5)

# --- Run App ---
root.mainloop()
