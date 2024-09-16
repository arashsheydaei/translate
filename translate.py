import tkinter as tk
from tkinter import messagebox, scrolledtext
from googletrans import Translator
import subprocess

class TranslateApp:
    def __init__(self, master):
        self.master = master
        self.master.title("برنامه ترجمه و خواندن متن")
        self.master.geometry("700x500")

        self.label = tk.Label(master, text="متن خود را وارد کنید:")
        self.label.pack(pady=10)

        self.text_entry = tk.Entry(master, width=70)
        self.text_entry.pack(pady=10)

        self.translate_button = tk.Button(master, text="ترجمه", command=self.translate_text)
        self.translate_button.pack(pady=10)

        self.translated_text = scrolledtext.ScrolledText(master, width=80, height=10, wrap=tk.WORD)
        self.translated_text.pack(pady=10)

        self.voice_speed_label = tk.Label(master, text="تنظیم سرعت:")
        self.voice_speed_label.pack(pady=5)
        self.voice_speed = tk.Scale(master, from_=80, to=450, orient='horizontal')
        self.voice_speed.set(175)  # سرعت پیش‌فرض
        self.voice_speed.pack(pady=5)

        self.voice_pitch_label = tk.Label(master, text="تنظیم زیر و بمی:")
        self.voice_pitch_label.pack(pady=5)
        self.voice_pitch = tk.Scale(master, from_=0, to=100, orient='horizontal')
        self.voice_pitch.set(50)  # زیر و بمی پیش‌فرض
        self.voice_pitch.pack(pady=5)

        self.speak_button = tk.Button(master, text="خواندن متن", command=self.speak_text, state=tk.DISABLED)
        self.speak_button.pack(pady=10)

        self.translator = Translator()
        self.translation = ""

    def translate_text(self):
        text = self.text_entry.get()
        if text:
            try:
                translation = self.translator.translate(text, dest='fa')
                self.translation = translation.text
                self.translated_text.config(state=tk.NORMAL)
                self.translated_text.delete(1.0, tk.END)
                self.translated_text.insert(tk.END, self.translation)
                self.translated_text.config(state=tk.DISABLED)
                self.speak_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در ترجمه: {e}")
        else:
            messagebox.showerror("خطا", "لطفاً متنی وارد کنید.")

    def speak_text(self):
        if self.translation:
            try:
                speed = self.voice_speed.get()
                pitch = self.voice_pitch.get()
                # استفاده از espeak برای تبدیل متن به گفتار با تنظیمات صدا
                subprocess.run(['espeak', '-v', 'fa', '-s', str(speed), '-p', str(pitch), self.translation])
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در خواندن متن: {e}")
        else:
            messagebox.showerror("خطا", "متنی برای خواندن وجود ندارد.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslateApp(root)
    root.mainloop()

