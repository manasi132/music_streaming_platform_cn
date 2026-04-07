import os

class AudioPlayer:
    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)

    def play(self):
        print("🎶 Opening in default media player...")
        os.startfile(self.filepath)