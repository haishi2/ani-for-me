import pygame
from ui_classes import AnimeSpotlight, RecommendationDisplay, PreferenceMeterDisplay, EpisodeRangeFilterDisplay, \
    GenreFilterDisplay, Button, AirDateFilterDisplay
from other_classes import Anime
import time

Coord = int | float
Colour = tuple[int, int, int]

# Start on log in

game_state = 'main'


# Screen Constants
# 46, 81, 162
# 37, 65, 130

SCREEN_SIZE = (800, 600)
FONT_STYLE = 'dm sans'
BACKGROUND_COLOUR = (255, 255, 255)
SECTION_TITLE_COLOUR = (46, 81, 162)


# Top Bar Constants

TOP_BAR_BACKGROUND_COLOUR = (226, 240, 255)
TOP_BAR_BACKGROUND_COLOUR = (46, 81, 162) # TODO
TOP_BAR_HEIGHT_PERCENTAGE = 0.15


# Anime Spotlight Constants

ANIME_SPOTLIGHT_BACKGROUND_COLOUR = (255, 255, 255)
ANIME_SPOTLIGHT_TITLE_COLOUR = (0, 0, 0)
ANIME_SPOTLIGHT_WIDTH_PERCENTAGE = 0.4
GRAPH_COLOUR_ONE = (88, 116, 181)
GRAPH_COLOUR_TWO = (67, 98, 171)
GRAPH_DOT_COLOUR = (23, 41, 81)
GRAPH_LINE_COLOUR = (23, 41, 81)
GRAPH_COLOUR = (151, 168, 209, 120)
GRAPH_RATING_ALPHA = 120
ANIME_SPOTLIGHT_TITLE_FONT_SIZE = 48


# Recommendation Display Constants

RECOMMENDATION_DISPLAY_WIDTH_PERCENTAGE = 1 - ANIME_SPOTLIGHT_WIDTH_PERCENTAGE
RECOMMENDATION_BUTTON_COLOUR = (255, 255, 255)
RECOMMENDATION_BUTTON_HOVER_COLOUR = (220, 220, 220)
RECOMMENDATION_BUTTON_TEXT_COLOUR = (0, 0, 0)
GENERATE_BUTTON_TEXT_COLOUR = (255, 255, 255)
GENERATE_BUTTON_COLOUR = (46, 81, 162)
GENERATE_BUTTON_HOVER_COLOUR = (37, 65, 130)


# Preference Display Constants

PREFERENCE_DISPLAY_OFFSET_X = 0.1
METER_BACK_COLOUR = (255, 255, 255)
METER_BORDER_COLOUR = (255, 255, 255)
METER_VALUE_COLOUR = (60, 60, 60)
METER_TITLE_COLOUR = (255, 255, 255)


# Episode Filter Display Constants

EPISODE_RANGE_DISPLAY_PERCENTAGE_X = 0.4
RANGE_COLOUR = (255, 255, 255)
BUTTON_RADIUS = 15
RADIAL_BUTTON_COLOUR = (255, 255, 255)
RADIAL_BUTTON_BORDER_COLOUR = (255, 255, 255)
RADIAL_BUTTON_FILLED_COLOUR = (60, 60, 60)
EPISODE_COUNT_TITLE_COLOUR = (255, 255, 255)


# Genre Filter Constants

MENU_OPEN_BUTTON_COLOUR = (255, 255, 255)
MENU_OPEN_BUTTON_HOVER_COLOUR = (220, 220, 220)
MENU_OPEN_BUTTON_TEXT_COLOUR = (46, 81, 162)
GENRE_FILTER_DISPLAY_OFFSET_X_PERCENTAGE = 0.7
GENRE_TEXT_COLOUR = (46, 81, 162)
GENRE_BUTTON_COLOUR = (255, 255, 255)
GENRE_BUTTON_FILLED_COLOUR = (220, 220, 220)
GENRE_BUTTON_BORDER_COLOUR = (255, 255, 255)
GENRE_BUTTON_HOVER_COLOUR = (220, 220, 220)


# Year Filter Display Constants

ALLOWED_YEAR_INPUT_BOX_INPUTS = '1234567890'
YEAR_FILTER_DISPLAY_OFFSET_X_PERCENTAGE = 0.7
YEAR_FILTER_BORDER_COLOUR = (255, 255, 255)
YEAR_FILTER_INPUT_TEXT_COLOUR = (255, 255, 255)
YEAR_FILTER_INPUT_PASSIVE_COLOUR = (255, 255, 255)
YEAR_FILTER_INPUT_ACTIVE_COLOUR = (192, 203, 227)
YEAR_RANGE_TITLE_COLOUR = (255, 255, 255)


# Account Button Constants

BUTTON_WIDTH_PERCENTAGE = 0.05
BUTTON_HEIGHT_PERCENTAGE = 0.8
ACCOUNT_BUTTON_MARGIN = 0.1
ACCOUNT_BUTTON_COLOUR = (255, 255, 255)
BACK_ARROW_COLOUR = (46, 81, 162)
BACK_ARROW_HOVER_COLOUR = (255, 255, 255)
ACCOUNT_BUTTON_HOVER_COLOUR = (46, 81, 162)
ACCOUNT_BUTTON_TEXT_COLOUR = (0, 0, 0)
ACCOUNT_BUTTON_BORDER_COLOUR = (255, 255, 255)
SINGLE_BUTTON_BORDER_RADIUS = 10


def fill_img(image: pygame.Surface, colour: Colour) -> None:
    """Mutates the surface filling its colour"""
    width, height = image.get_size()
    r, g, b = colour
    for x in range(width):
        for y in range(height):
            a = image.get_at((x, y))[3]
            image.set_at((x, y), pygame.Color(r, g, b, a))


def draw_top_bar(screen: pygame.Surface,
                 background_colour: tuple[int, int, int],
                 height_percentage: float) -> None:
    height = screen.get_height() * height_percentage
    width = screen.get_width()
    top_bar_rect = pygame.Rect((0, 0), (width, height))
    pygame.draw.rect(screen, background_colour, top_bar_rect)


def draw_account_button(screen: pygame.Surface) -> Button:
    back_arrow = pygame.image.load('arrow-back-32x32.png')
    fill_img(back_arrow, BACK_ARROW_COLOUR)
    account_button = Button(screen,
                            screen.get_width() * BUTTON_WIDTH_PERCENTAGE,
                            screen.get_width() * BUTTON_WIDTH_PERCENTAGE,
                            (screen.get_width() * BUTTON_WIDTH_PERCENTAGE / 2, 
                             screen.get_width() * BUTTON_WIDTH_PERCENTAGE / 2),
                            '',
                            ACCOUNT_BUTTON_COLOUR,
                            ACCOUNT_BUTTON_HOVER_COLOUR,
                            ACCOUNT_BUTTON_TEXT_COLOUR,
                            border_colour=ACCOUNT_BUTTON_BORDER_COLOUR,
                            border_radius=SINGLE_BUTTON_BORDER_RADIUS,
                            image=back_arrow)
    account_button.draw()
    return account_button


def draw_recommendation_display(screen) -> RecommendationDisplay:
    recommendation_display = RecommendationDisplay(screen,
                                                   TOP_BAR_HEIGHT_PERCENTAGE,
                                                   RECOMMENDATION_DISPLAY_WIDTH_PERCENTAGE,
                                                   RECOMMENDATION_BUTTON_COLOUR,
                                                   RECOMMENDATION_BUTTON_HOVER_COLOUR,
                                                   GENERATE_BUTTON_TEXT_COLOUR,
                                                   GENERATE_BUTTON_COLOUR,
                                                   GENERATE_BUTTON_HOVER_COLOUR,
                                                   RECOMMENDATION_BUTTON_TEXT_COLOUR,
                                                   FONT_STYLE,
                                                   SECTION_TITLE_COLOUR)
    recommendation_display.draw()
    return recommendation_display


def draw_anime_spotlight(screen: pygame.Surface) -> AnimeSpotlight:
    anime_spotlight = AnimeSpotlight(screen,
                                     ANIME_SPOTLIGHT_BACKGROUND_COLOUR,
                                     TOP_BAR_HEIGHT_PERCENTAGE,
                                     ANIME_SPOTLIGHT_WIDTH_PERCENTAGE,
                                     ANIME_SPOTLIGHT_TITLE_COLOUR,
                                     GRAPH_COLOUR_ONE,
                                     GRAPH_COLOUR_TWO,
                                     GRAPH_DOT_COLOUR,
                                     GRAPH_LINE_COLOUR,
                                     GRAPH_COLOUR,
                                     GRAPH_RATING_ALPHA,
                                     FONT_STYLE,
                                     ANIME_SPOTLIGHT_TITLE_FONT_SIZE)
    anime_spotlight.draw()
    return anime_spotlight


def draw_preference_display(screen: pygame.Surface) -> PreferenceMeterDisplay:
    preference_meter_display = PreferenceMeterDisplay(screen,
                                                      TOP_BAR_HEIGHT_PERCENTAGE,
                                                      PREFERENCE_DISPLAY_OFFSET_X,
                                                      METER_BACK_COLOUR,
                                                      METER_BORDER_COLOUR,
                                                      METER_VALUE_COLOUR,
                                                      METER_TITLE_COLOUR,
                                                      FONT_STYLE)
    preference_meter_display.draw_display()
    return preference_meter_display


def draw_episode_range_filter(screen: pygame.Surface) -> EpisodeRangeFilterDisplay:
    episode_range_filter_display = EpisodeRangeFilterDisplay(screen,
                                                             EPISODE_RANGE_DISPLAY_PERCENTAGE_X,
                                                             TOP_BAR_HEIGHT_PERCENTAGE,
                                                             RANGE_COLOUR,
                                                             EPISODE_COUNT_TITLE_COLOUR,
                                                             BUTTON_RADIUS,
                                                             RADIAL_BUTTON_COLOUR,
                                                             RADIAL_BUTTON_FILLED_COLOUR,
                                                             RADIAL_BUTTON_BORDER_COLOUR,
                                                             FONT_STYLE)
    episode_range_filter_display.draw()
    return episode_range_filter_display


def draw_genre_filter_display(screen: pygame.Surface) -> GenreFilterDisplay:
    genre_filter_display = GenreFilterDisplay(screen,
                                              GENRE_FILTER_DISPLAY_OFFSET_X_PERCENTAGE,
                                              TOP_BAR_HEIGHT_PERCENTAGE,
                                              GENRE_TEXT_COLOUR,
                                              SECTION_TITLE_COLOUR,
                                              GENRE_BUTTON_COLOUR,
                                              GENRE_BUTTON_FILLED_COLOUR,
                                              GENRE_BUTTON_BORDER_COLOUR,
                                              MENU_OPEN_BUTTON_COLOUR,
                                              MENU_OPEN_BUTTON_HOVER_COLOUR,
                                              MENU_OPEN_BUTTON_TEXT_COLOUR,
                                              GENRE_BUTTON_HOVER_COLOUR,
                                              FONT_STYLE)
    genre_filter_display.draw()
    return genre_filter_display


def hide_drop_down(screen: pygame.Surface, episode_range_filter_display: EpisodeRangeFilterDisplay,
                   recommendation_display: RecommendationDisplay, preference_display: PreferenceMeterDisplay,
                   genre_filter_display: GenreFilterDisplay, year_filter: AirDateFilterDisplay, back_button: Button,
                   anime_spotlight: AnimeSpotlight) -> None:
    # Top section
    draw_top_bar(screen, TOP_BAR_BACKGROUND_COLOUR, TOP_BAR_HEIGHT_PERCENTAGE)
    back_button.draw()
    clicked_buttons = episode_range_filter_display.radial_button_collection.clicked_buttons
    episode_range_filter_display.draw()
    preference_display.draw_meter_titles()
    for meter in preference_display.meters.values():
        meter.draw()
    genre_filter_display.draw()
    year_filter.draw()
    year_filter.input_box_start.update_text()
    year_filter.input_box_end.update_text()

    # Recommendation section
    for clicked_button in clicked_buttons:
        episode_range_filter_display.radial_button_collection.draw(clicked_button)
    recommendation_display_bg_rect = pygame.Rect(recommendation_display.position[0], recommendation_display.position[1],
                                                 recommendation_display.width, recommendation_display.height)
    pygame.draw.rect(screen, BACKGROUND_COLOUR, recommendation_display_bg_rect)
    recommendation_display.draw()
    
    anime_spotlight.redraw()
    


def draw_year_filter(screen: pygame.Surface) -> AirDateFilterDisplay:
    air_date_filter_display = AirDateFilterDisplay(screen,
                                                   TOP_BAR_HEIGHT_PERCENTAGE,
                                                   YEAR_FILTER_DISPLAY_OFFSET_X_PERCENTAGE,
                                                   YEAR_FILTER_INPUT_TEXT_COLOUR,
                                                   YEAR_FILTER_INPUT_PASSIVE_COLOUR,
                                                   YEAR_FILTER_INPUT_ACTIVE_COLOUR,
                                                   TOP_BAR_BACKGROUND_COLOUR,
                                                   YEAR_RANGE_TITLE_COLOUR,
                                                   FONT_STYLE,
                                                   YEAR_FILTER_BORDER_COLOUR)
    air_date_filter_display.draw()
    return air_date_filter_display

# For testing purposes

from random import randint, shuffle


def testing():
    animes = [
        Anime('Tensei Kizoku no Isekai Boukenroku: Jichou wo Shiranai Kamigami no Shito',
              [randint(5, 10) for _ in range(6)]),
        Anime('RIck and Morty adventures for 100 years 100 seasons', [randint(5, 10) for _ in range(6)]),
        Anime('Your lie in April Your lie in April Your lie in April Your lie in April Your lie in April', [randint(5, 10) for _ in range(6)]),
        Anime('Sword Art Online', [randint(5, 10) for _ in range(6)]),
        Anime('Jobless Reincarnation', [randint(5, 10) for _ in range(6)]),
        Anime('Bluelock', [randint(5, 10) for _ in range(6)]),
        Anime('Assassination Clas sroom', [randint(5, 10) for _ in range(6)]),
        Anime('Bocchi the Rock', [randint(5, 10) for _ in range(6)]),
        Anime('Toopy and Binoo', [randint(5, 10) for _ in range(6)]),
        Anime('Barnie', [randint(5, 10) for _ in range(6)])
    ]
    # shuffle(animes)
    anime_ranked = [(100, anime) for anime in animes]
    return anime_ranked


def run_main(screen: pygame.Surface) -> None:
    """Visualize the project"""
    global game_state
    recommendations = {}
    draw_top_bar(screen, TOP_BAR_BACKGROUND_COLOUR, TOP_BAR_HEIGHT_PERCENTAGE)
    account_button = draw_account_button(screen)
    anime_spotlight = draw_anime_spotlight(screen)
    recommendation_display = draw_recommendation_display(screen)
    preference_display = draw_preference_display(screen)
    generate_button = recommendation_display.generate_button
    episode_range_filter = draw_episode_range_filter(screen)
    genre_filter_display = draw_genre_filter_display(screen)
    year_filter = draw_year_filter(screen)

    anime_ranked = testing()
    recommendations = recommendation_display.update(anime_ranked, anime_spotlight)

    while True:
        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)
        drop_down_menu = genre_filter_display.drop_down_menu
        is_key_down = any(event.type == pygame.KEYDOWN for event in events)
        pressed_key = None
        is_backspace_pressed = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.unicode in ALLOWED_YEAR_INPUT_BOX_INPUTS:
                    pressed_key = event.unicode
                if event.key == pygame.K_BACKSPACE:
                    is_backspace_pressed = True
        # GENERATE BUTTON
        if not drop_down_menu.is_deployed:
            generate_button.update_colour(mouse_pos)
        if generate_button.is_clicked(is_clicking, mouse_pos) and not drop_down_menu.is_deployed:
            if year_filter.input_box_start.is_active:
                year_filter.input_box_start.update_activity()
            if year_filter.input_box_end.is_active:
                year_filter.input_box_end.update_activity()
            # Testing fileter exports
            print(f"genres: {genre_filter_display.get_selected_genres()}")
            print(f"episode: {episode_range_filter.get_episode_ranges()}")
            print(f"preferences: {[(name, value.value) for name, value in preference_display.meters.items()]}")
            print(f"year range: {year_filter.get_year_range()}")
            anime_ranked = testing()
            recommendations = recommendation_display.update(anime_ranked, anime_spotlight)

        # Account button
        if not drop_down_menu.is_deployed:
            if account_button.update_colour(mouse_pos):
                fill_img(account_button._image, BACK_ARROW_HOVER_COLOUR)
            else:
                fill_img(account_button._image, BACK_ARROW_COLOUR)
        if account_button.is_clicked(is_clicking, mouse_pos) and not drop_down_menu.is_deployed:
            game_state = 'account'


        for recommendation in recommendations:
            # Update spotlight on button press
            if recommendations[recommendation][1].is_clicked(is_clicking, mouse_pos) and not drop_down_menu.is_deployed:
                if year_filter.input_box_start.is_active:
                    year_filter.input_box_start.update_activity()
                if year_filter.input_box_end.is_active:
                    year_filter.input_box_end.update_activity()
                anime_spotlight.update(recommendations[recommendation][0])
            # Update button colour on hover
            if not drop_down_menu.is_deployed:
                recommendations[recommendation][1].update_colour(mouse_pos)

        # Update Preference Meters
        for meter in preference_display.meters:
            curr_meter = preference_display.meters[meter]
            if curr_meter.is_clicked(is_clicking, mouse_pos) and not drop_down_menu.is_deployed:
                if year_filter.input_box_start.is_active:
                    year_filter.input_box_start.update_activity()
                if year_filter.input_box_end.is_active:
                    year_filter.input_box_end.update_activity()
                curr_meter.update(mouse_pos)

        # Update Episode Range Display
        ep_button_collection = episode_range_filter.radial_button_collection.button_collection
        for ep_range in ep_button_collection:
            button = ep_button_collection[ep_range]
            if button.is_clicked(is_clicking, mouse_pos) and not drop_down_menu.is_deployed:
                if year_filter.input_box_start.is_active:
                    year_filter.input_box_start.update_activity()
                if year_filter.input_box_end.is_active:
                    year_filter.input_box_end.update_activity()
                episode_range_filter.update(ep_range)

        # Genre button hover
        genre_filter_display.menu_open_button.update_colour(mouse_pos)
            
        # Update Drop Down Menu
        if genre_filter_display.menu_open_button.is_clicked(is_clicking, mouse_pos) or drop_down_menu.clicked_off(is_clicking, mouse_pos):
            if year_filter.input_box_start.is_active:
                year_filter.input_box_start.update_activity()
            if year_filter.input_box_end.is_active:
                year_filter.input_box_end.update_activity()
            drop_down_menu.update()
            if drop_down_menu.is_deployed:
                drop_down_menu.draw_menu(screen, genre_filter_display.menu_base_pos, genre_filter_display.menu_size,
                                         GENRE_BUTTON_COLOUR)
            else:
                hide_drop_down(screen, episode_range_filter, recommendation_display, preference_display,
                               genre_filter_display, year_filter, account_button, anime_spotlight)


        if drop_down_menu.is_deployed:
            for genre, button in drop_down_menu.button_collection.items():
                button.update_colour(mouse_pos)
                # Update Genres
                if button.is_clicked(is_clicking, mouse_pos):
                    genre_filter_display.add_genre(genre)

        # Year Filter
        if year_filter.input_box_start.is_clicked(is_clicking, mouse_pos) and not drop_down_menu.is_deployed:
            year_filter.input_box_start.update_activity()
            if year_filter.input_box_end.is_active:
                year_filter.input_box_end.update_activity()

        if year_filter.input_box_start.is_active and is_key_down and (pressed_key is not None or is_backspace_pressed):
            if is_backspace_pressed:
                year_filter.input_box_start.input_text = year_filter.input_box_start.input_text[:-1]
                year_filter.input_box_start.update_text()
            elif len(year_filter.input_box_start.input_text) < 4:
                year_filter.input_box_start.input_text += pressed_key
                year_filter.input_box_start.update_text()

        if year_filter.input_box_end.is_clicked(is_clicking, mouse_pos) and not drop_down_menu.is_deployed:
            year_filter.input_box_end.update_activity()
            if year_filter.input_box_start.is_active:
                year_filter.input_box_start.update_activity()

        if year_filter.input_box_end.is_active and is_key_down and (pressed_key is not None or is_backspace_pressed):
            if is_backspace_pressed:
                year_filter.input_box_end.input_text = year_filter.input_box_end.input_text[:-1]
                year_filter.input_box_end.update_text()
            elif len(year_filter.input_box_end.input_text) < 4:
                year_filter.input_box_end.input_text += pressed_key
                year_filter.input_box_end.update_text()

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()
            
        if game_state != 'main':
            break


def run_account(screen: pygame.Surface) -> None:
    while True:
        pygame.display.flip()
        events = pygame.event.get()
        screen.fill((0, 0, 0))
        
        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()


def run_project() -> None:
    screen = initialize_screen(SCREEN_SIZE, BACKGROUND_COLOUR)
    while True:
        if game_state == 'main':
            run_main(screen)
        elif game_state == 'account':
            run_account(screen)


def initialize_screen(screen_size: tuple[int, int], background_colour: tuple[int, int, int]) -> pygame.Surface:
    """Initialize pygame and the display window.

    This is a helper function for the "visualize_graph" functions above.
    You can safely ignore this function.
    """
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption('Ani-4-me')
    screen = pygame.display.set_mode(screen_size)
    screen.fill(background_colour)

    return screen


if __name__ == "__main__":
    run_project()
