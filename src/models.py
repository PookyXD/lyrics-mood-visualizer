class LyricLine:
    def __init__(self, text, section):
        self.text = text
        self.section = section
        self.emotion = "neutral"
        self.positive = 0.0
        self.negative = 0.0
        self.neutral = 0.0
        self.compound = 0.0

    def __repr__(self):
        return f"LyricLine(section='{self.section}', text='{self.text[:30]}...', compound{self.compound})"
    
class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.lines = []

    def add_line(self, lyric_line):
        self.lines.append(lyric_line)

    def __repr__(self):
        return f"Song(title='{self.title}', artist='{self.artist}', lines={len(self.lines)})"
