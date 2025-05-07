from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
import requests

# API endpoint
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

class ArtVandelAIApp(App):
    def build(self):
        # Center the whole UI
        anchor = AnchorLayout(anchor_x='center', anchor_y='center')

        # Main layout
        root = BoxLayout(orientation='vertical', size_hint=(None, None), size=(700, 800), padding=30, spacing=20)

        # Header layout
        header = BoxLayout(orientation='horizontal', size_hint=(1, None), height=120, spacing=20)
        logo = Image(source='peri.png', size_hint=(None, None), size=(96, 96))
        header_text = BoxLayout(orientation='vertical', spacing=5)
        title = Label(text="ArtVandelAI", font_size=36, color=(0.8, 0.8, 1, 1), bold=True)
        subtitle = Label(text="Importer/Exporter", font_size=20, color=(0.8, 0.8, 1, 1), italic=True)
        header_text.add_widget(title)
        header_text.add_widget(subtitle)
        header.add_widget(logo)
        header.add_widget(header_text)
        root.add_widget(header)

        # Input prompt
        prompt_label = Label(text="Enter your prompt below:", font_size=18, color=(0.8, 0.8, 1, 1), size_hint=(1, None), height=30)
        self.input_box = TextInput(
            hint_text="Type your prompt here...",
            font_size=18,
            size_hint=(1, None),
            height=50,
            multiline=False,
            padding=[10, 10],
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(0.9, 0.9, 1, 1),
            cursor_color=(0.9, 0.9, 1, 1)
        )
        root.add_widget(prompt_label)
        root.add_widget(self.input_box)

        # Submit button
        submit_btn = Button(
            text="Submit",  # Changed from → to "Submit" to avoid X rendering
            size_hint=(None, None),
            size=(200, 50),
            font_size=20,
            background_normal='',
            background_color=(0.8, 0.7, 0.9, 1),
            color=(0.1, 0.1, 0.1, 1)
        )
        submit_btn.bind(on_press=self.on_submit)
        with submit_btn.canvas.before:
            Color(0.8, 0.7, 0.9, 1)
            self.btn_bg = RoundedRectangle(pos=submit_btn.pos, size=submit_btn.size, radius=[20])
        submit_btn.bind(size=self.update_btn_bg, pos=self.update_btn_bg)
        root.add_widget(submit_btn)

        # Scrollable output
        self.output_scroll = ScrollView(size_hint=(1, 1))
        self.output_label = Label(
            text="",
            font_size=16,
            color=(0.8, 0.8, 1, 1),
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.output_label.bind(texture_size=self.resize_label)
        self.output_scroll.add_widget(self.output_label)
        root.add_widget(self.output_scroll)

        anchor.add_widget(root)
        return anchor

    def on_submit(self, instance):
        prompt = self.input_box.text.strip()
        if prompt:
            response = get_ai_response(prompt)
            self.output_label.text = f"AI Response:\n{response}"
        else:
            self.output_label.text = "Error: Please enter a prompt."

    def update_btn_bg(self, instance, value):
        self.btn_bg.pos = instance.pos
        self.btn_bg.size = instance.size

    def resize_label(self, instance, value):
        self.output_label.text_size = (self.output_scroll.width - 20, None)
        self.output_label.height = self.output_label.texture_size[1]

if __name__ == "__main__":
    ArtVandelAIApp().run()
