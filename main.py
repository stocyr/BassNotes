from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.clock import Clock
from random import choice
from math import floor
from kivy.core.audio import SoundLoader


class BassNotes(BoxLayout):

    notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Ab', 'Bb', 'Db', 'Eb', 'Gb', 'A#', 'C#', 'D#', 'F#', 'G#']
    sounding = True
    sound_delay = 0.15

    def __init__(self):
        super(BassNotes, self).__init__()
        self.beat = 0
        self.next_note = choice(self.notes)
        self.sound_high = SoundLoader.load('metronome_click.ogg')
        self.sound_low = SoundLoader.load('metronome_click_low.ogg')
        self.on_beat()

    def on_beat(self, *args):
        beat_duration = 60.0 / self.ids.bpm_slider.value

        # Update beat
        if self.beat == 4:
            self.beat = 1
            self.next_note = choice(self.notes)
        else:
            self.beat += 1
        Clock.schedule_once(self.update_beat_text, self.sound_delay)

        # Play sound
        if self.ids.sound.state == 'down':
            if self.beat == 1:
                self.sound_high.play()
            else:
                self.sound_low.play()

        # Calculate when to show next note
        if self.beat == floor(self.ids.show_slider.value):
            # We must display the next note within *this* beat.
            delay = beat_duration * (self.ids.show_slider.value - self.beat)
            Clock.schedule_once(self.update_note, delay + self.sound_delay)

        # Re-schedule next beat
        Clock.schedule_once(self.on_beat, beat_duration)

    def update_beat_text(self, *args):
        self.ids.beat.text = str(int(round(self.beat)))

    def update_note(self, *args):
        self.ids.note.text = self.next_note

class BassNotesApp(App):
    title = 'Bass Notes'
    def build(self):
       return BassNotes()

if __name__ == '__main__':
    BassNotesApp().run()
