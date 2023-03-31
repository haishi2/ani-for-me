""" Form that allows the user to input their favorite anime """

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
FONT = pygame.font.Font(None, 32)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

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
        btn_rect = pygame.Rect(self._position, (self._width, self._height))
        pygame.draw.rect(self._screen, self._colour, btn_rect)

        word_surf = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        font = pygame.font.SysFont('candara', int(self._height * 0.5), bold=True)
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

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
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


def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    btn = Button(screen, 10, 10, (10, 10), 'hi', (0, 255, 255), (255, 215, 0), (255, 215, 0))
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
    pygame.quit()
