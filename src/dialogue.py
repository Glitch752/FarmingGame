import pygame
from audio import AudioManager, SoundType
from constants import WIDTH
from graphics import small_font_render, normal_font_render
from items import ITEM_SLOT_BORDER_RADIUS, SLOT_BACKGROUND

class DialogueManager:
    queue: list[list[str]]
    lines: list[str]
    
    current_char: int
    current_line: int
    timer: float
    done: bool
    time_per_letter: float
    
    def __init__(self) -> None:
        self.queue = []
        self.lines = []
        self.current_char = 0
        self.current_line = 0
        self.timer = 0
        self.done = False
        self.time_per_letter = 0.05

    def queue_dialogue(self, lines: list[str]):
        self.queue.append(lines)
    
    def on_confirm(self):
        if not self.done and len(self.lines):
            self.current_line = len(self.lines) - 1
            self.current_char = len(self.lines[self.current_line])
            self.done = True
        else:
            self.done = False
            self.current_char = 0
            self.current_line = 0
            self.lines.clear()
            if len(self.queue):
                self.lines = self.queue.pop(0)
    
    def is_shown(self):
        return len(self.lines)
    
    def is_active(self):
        return len(self.lines) and not self.done
    
    def update(self, delta: float, audio_manager: AudioManager):
        if not self.is_active():
            return
        
        self.timer += delta

        if self.timer > self.time_per_letter:
            self.timer -= self.time_per_letter

            self.current_char += 1

            if self.current_char == len(self.lines[self.current_line]):
                self.current_line += 1

                if self.current_line > len(self.lines) - 1:
                    self.current_line = len(self.lines) - 1
                    self.done = True
                    return
                
                self.current_char = 0
            elif self.lines[self.current_line][self.current_char] != " ":
                audio_manager.play_sound(SoundType.SPEAKING_SOUND)

    def draw(self, win: pygame.Surface):
        if len(self.lines):
            pygame.draw.rect(
                win,
                SLOT_BACKGROUND,
                pygame.Rect(WIDTH // 2 - 300, 20, 600, len(self.lines) * 30 + 20),
                border_radius=ITEM_SLOT_BORDER_RADIUS
            )

            y = 25

            for i, line in enumerate(self.lines):
                if i <= self.current_line:
                    if i == 0:
                        t = normal_font_render(line if i != self.current_line else line[:self.current_char], 'white')
                    else:
                        t = small_font_render(line if i != self.current_line else line[:self.current_char], 'white')

                    win.blit(t, (16 + WIDTH // 2 - 295, 16 + y))
                    
                    y += t.get_height() + 5