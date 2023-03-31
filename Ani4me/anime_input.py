""" Home Page """

import pygame
from typing import Optional
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
FONT = pygame.font.Font(None, 32)


watched_anime = ['x', 'y', 'z']
anime_data = ['x', 'y', 'z']
values = [range(1, 11)]

user_priorities = {'story': 0, 'animation': 0, 'sound': 0, 'character': 0}
user_rankings = {'story': 0, 'animation': 0, 'sound': 0, 'character': 0}

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            print('click')
        elif self._is_hovered(pygame.mouse.get_pos()):
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
        self.txt_surface = FONT.render(text, False, self.color)
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
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Text:
    """ Add Text To Screen Class"""

    _size: int
    _text: str
    _x: Coord
    _y: Coord
    _bold: False

    def __init__(self, size: int, text: str, x: Coord, y: Coord, bold: Optional[bool] = False):
        self._size = size
        self._text = text
        self._x = x
        self._y = y
        self._bold = bold

    def draw(self) -> None:
        font = pygame.font.SysFont("Arial", self._size, bold=self._bold)
        txtsurf = font.render(self._text, True, (51, 51, 51))
        screen.blit(txtsurf, (self._x, self._y))


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


# Home Page
def home_page():
    add_anime_btn = Button(screen, 35, 200, (60, 270), "Add Anime", (51, 51, 51), (30, 77, 245), (255, 255, 255))
    add_friend_btn = Button(screen, 35, 200, (280, 270), "Add Friend", (51, 51, 51), (30, 77, 245), (255, 255, 255))
    get_rec_btn = Button(screen, 35, 420, (60, 320), "Get Reccomendations", (51, 51, 51), (30, 77, 245),
                         (255, 255, 255))

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                exit()

            add_friend_btn.handle_event(event)

        screen.fill((255, 255, 255))
        Text(20, "Hello, there! Welcome to ", 60, 80).draw()
        Text(48, "Ani4me", 60, 120, True).draw()
        Text(20, "Get a recommendation on what to watch next by adding", 60, 190).draw()
        Text(20, "some of the animes that you have watched so far.", 60, 220).draw()
        add_anime_btn.draw()
        add_friend_btn.draw()
        get_rec_btn.draw()
        Text(20, "Watched List", 60, 410).draw()
        y = 410
        for anime in watched_anime:
            y = y + 30
            Text(20, anime, 70, y).draw()
        pygame.display.flip()


def add_anime_page():

    done = False
    COLOR_INACTIVE = (217, 217, 217)
    COLOR_ACTIVE = (30, 77, 245)

    anime_dropdown_btn = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_INACTIVE, COLOR_ACTIVE], 200, 150, 400, 30, pygame.font.SysFont('Arial', 20),  "Select Anime", anime_data)
    ranking_btn_story = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                  [COLOR_INACTIVE, COLOR_ACTIVE], 200, 200, 400, 30, pygame.font.SysFont('Arial', 20),
                                  "Rate", user_rankings)
    ranking_btn_animation = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                 [COLOR_INACTIVE, COLOR_ACTIVE], 200, 250, 400, 30, pygame.font.SysFont('Arial', 20),
                                 "Rate", user_rankings)
    ranking_btn_sound = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                 [COLOR_INACTIVE, COLOR_ACTIVE], 200, 300, 400, 30, pygame.font.SysFont('Arial', 20),
                                 "Rate", user_rankings)
    ranking_btn_character = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                 [COLOR_INACTIVE, COLOR_ACTIVE], 200, 350, 400, 30, pygame.font.SysFont('Arial', 20),
                                 "Rate", user_rankings)
    ranking_btn_enjoyment = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                 [COLOR_INACTIVE, COLOR_ACTIVE], 200, 400, 400, 30, pygame.font.SysFont('Arial', 20),
                                 "Rate", user_rankings)
    while not done:
        event_list = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))

        selected_anime = anime_dropdown_btn.update(event_list)
        if selected_anime >= 0:
            anime_dropdown_btn.main = anime_dropdown_btn.options[selected_anime]
            print(anime_dropdown_btn.options[selected_anime])

        Text(36, "Add Anime", 60, 90, True).draw()

        Text(20, "Name:", 60, 150).draw()
        Text(20, "Story:", 60, 200).draw()
        Text(20, "Animation:", 60, 250).draw()
        Text(20, "Sound:", 60, 300).draw()
        Text(20, "Character:", 60, 350).draw()
        Text(20, "Enjoyment:", 60, 400).draw()
        anime_dropdown_btn.draw(screen)
        pygame.display.flip()



if __name__ == '__main__':
    add_anime_page()
