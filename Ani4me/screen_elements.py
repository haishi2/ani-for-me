import pygame
import sys
from typing import Optional

Coord = int | float
Position = tuple[Coord, Coord]
Colour = tuple[int, int, int]

class Button:
    """Button class"""
    _screen: pygame.Surface
    _height: Coord
    _width: Coord
    _position: Position
    _text: str
    _colour: Colour
    _hover_colour: Colour
    _text_colour: Colour

    def __init__(self, screen: pygame.surface, height: Coord, width: Coord, position: Position, text: str,
                 colour: Colour, hover_colour: Colour, text_colour: Colour):
        self._screen = screen
        self._height = height
        self._width = width
        self._position = position
        self._text = text
        self._colour = colour
        self._hover_colour = hover_colour
        self._text_colour = text_colour

    def draw(self) -> None:
        """Draw button on the screen"""
        btn_rect = pygame.Rect(self._position, (self._width, self._height))
        pygame.draw.rect(self._screen, self._colour, btn_rect)

        word_surf = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        font = pygame.font.SysFont('Arial', 20, bold=True)
        img = font.render(self._text, True, self._text_colour)
        word_surf.blit(img, ((word_surf.get_width() - img.get_width()) / 2,
                             (word_surf.get_height() - img.get_height()) / 2))
        self._screen.blit(word_surf, self._position)

    def _is_hovered(self, mouse_pos: Position) -> bool:
        """Return whether the button is being hovered"""
        is_hover_x = self._position[0] < mouse_pos[0] < self._position[0] + self._width
        is_hover_y = self._position[1] < mouse_pos[1] < self._position[1] + self._height
        return is_hover_y and is_hover_x

    def is_clicked(self, is_mouse_down: bool, mouse_pos: Position):
        """Return whether the button is clicked"""
        return self._is_hovered(mouse_pos) and is_mouse_down

    def handle_event(self, event):
        """ If button is clicked..."""

        if event.type == pygame.MOUSEBUTTONDOWN: #is_hovered
            # If the user clicked on the input_box rect.
            print('click')

        if self._is_hovered(pygame.mouse.get_pos()):
            btn_rect = pygame.Rect(self._position, (self._width, self._height))
            pygame.draw.rect(self._screen, self._hover_colour, btn_rect)

            word_surf = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
            font = pygame.font.SysFont('Arial', 20, bold=True)
            img = font.render(self._text, True, self._text_colour)
            word_surf.blit(img, ((word_surf.get_width() - img.get_width()) / 2,
                                 (word_surf.get_height() - img.get_height()) / 2))
            self._screen.blit(word_surf, self._position)


class InputBox:
    """Input Box class"""

    _screen: pygame.Surface
    _height: Coord
    _width: Coord
    _position: Position
    _text: str
    _colour: Colour
    _text_colour: Colour

    def __init__(self, screen: pygame.surface, height: Coord, width: Coord, x: Coord, y: Coord, text: str,
                 colour: Colour, text_colour: Colour):
        self._screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = colour
        self.text = text
        self.txt_surface = pygame.font.Font(None, 20).render(text, False, self.color)
        self.active = False
        self._text_colour = text_colour

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 20).render(self.text, True, self._text_colour)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        self._screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(self._screen, self.color, self.rect, 2)


class Text:
    """ Add Text To Screen Class"""

    _size: int
    _text: str
    _x: Coord
    _y: Coord
    _bold: False

    def __init__(self, screen: pygame.surface,  size: int, text: str, x: Coord, y: Coord, bold: Optional[bool] = False):
        self._size = size
        self._text = text
        self._x = x
        self._y = y
        self._bold = bold
        self._screen = screen

    def draw(self) -> None:
        font = pygame.font.SysFont("Arial", self._size, bold=self._bold)
        txtsurf = font.render(self._text, True, (51, 51, 51))
        self._screen.blit(txtsurf, (self._x, self._y))


class DropDown:
    """ Drow Down Button Class """

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1
