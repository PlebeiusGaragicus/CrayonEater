import pygame
import textwrap

class AbstractConsole:
    def __init__(self, screen, font_size=20, font_name='monospace', text_color=(255, 255, 255), bg_color=(0, 0, 0)):
        self.screen = screen
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.line_height = font_size + 2
        self.console_width = screen.get_width()
        self.max_lines = screen.get_height() // self.line_height - 1
        # self.buffer = [""] * self.max_lines
        self.buffer = [""]
        self.current_line = ""

    def add_line(self, text):
        wrapped_text = textwrap.wrap(text, width=self.console_width // self.font.size(' ')[0])
        for line in wrapped_text:
            self.buffer.append(line)  # Add new line at the end of the buffer
            if len(self.buffer) > self.max_lines:
                self.buffer.pop(0)  # Remove the first line

    def add_text(self, text):
        # Add text to the current line buffer and wrap if necessary
        for char in text:
            self.current_line += char
            if char == '\n' or self.font.size(self.current_line)[0] > self.console_width:
                self._flush_current_line()

    def _flush_current_line(self):
        # Add the current line to the buffer and handle wrapping
        wrapped_lines = textwrap.wrap(self.current_line, width=self.console_width // self.font.size(' ')[0])
        for line in wrapped_lines[:-1]:  # Add all but the last wrapped line
            self.buffer.append(line)
            if len(self.buffer) > self.max_lines:
                self.buffer.pop(0)

        self.current_line = wrapped_lines[-1] if wrapped_lines else ""


    def draw(self):
        self.screen.fill(self.bg_color)
        y = 0
        for line in self.buffer[-self.max_lines:]:
            text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (0, y))
            y += self.line_height
        
        if self.current_line:
            text_surface = self.font.render(self.current_line, True, self.text_color)
            self.screen.blit(text_surface, (0, y))

        # pygame.display.flip()
