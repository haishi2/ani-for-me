"""
CSC111 Project: Main Program

This module contains the necessary code to run the program from start to finish.

This file is Copyright (c) 2023 Hai Shi, Liam Alexander Maguire, Amelia Wu, and Sanya Chawla.
"""
import pygame
import sys
from ui.ui_classes import AnimeSpotlight, RecommendationDisplay, PreferenceMeterDisplay, Button, AirDateFilterDisplay, Text, InputBox2, DropDown2
from classes.anime_and_users import Anime, User
from classes.graph import ReccomenderGraph, read_file, save_profile, import_profile, import_profile_to_user, Review
import datetime

Coord = int | float
Colour = tuple[int, int, int]

# Start on log in

game_state = 'main'

rec_graph = read_file(['csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/anime_formatted_no_duplicates.csv', 
                       'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/\
                       profiles_formatted_no_duplicates.csv', 
                       'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/\
                       reviews_formatted_no_duplicates.csv'])

# Screen Constants
# 46, 81, 162
# 37, 65, 130

SCREEN_SIZE = (800, 600)
FONT_STYLE = 'dm sans'
BACKGROUND_COLOUR = (255, 255, 255)
SECTION_TITLE_COLOUR = (46, 81, 162)

# Top Bar Constants

TOP_BAR_BACKGROUND_COLOUR = (46, 81, 162)
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

# TODO
def get_user(username: str) -> None:
    """Sets global user to user login"""
    global user
    filename = f"users/{username}.csv"
    user = import_profile_to_user(filename, rec_graph)


def add_anime(anime_name: int, ratings: list[int]) -> None:
    """Add anime review to user"""
    global user
    anime = rec_graph.animes[anime_name]
    overall = sum(ratings) // 5
    ratings.append(overall)
    r_type = ['story', 'animation', 'sound', 'character', 'enjoyment', 'overall']
    ratings = {r_type[i]: ratings[i] for i in range(6)}
    review = Review(user, anime, ratings)
    user.reviews[anime] = review
    
    save_user_profile(user)
#  reviews: dict[Anime, g.Review]


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
    """Draws the top bar of the pygame screen.
    """
    height = screen.get_height() * height_percentage
    width = screen.get_width()
    top_bar_rect = pygame.Rect((0, 0), (width, height))
    pygame.draw.rect(screen, background_colour, top_bar_rect)


def draw_account_button(screen: pygame.Surface) -> Button:
    """Draws the account button of the pygame screen.
    """
    back_arrow = pygame.image.load('ui/arrow-back-32x32.png')
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


def create_profile(username: str, fav_animes: set[Anime]):
    global user
    user = User(
        username=username,
        fav_animes=fav_animes,
        favorite_era=(datetime.date(1961, 1, 1), datetime.date(2021, 1, 1)),
        review=None,
        friend_list=[],
        priority= {'story': 1, 'animation': 1, 'sound': 1, 'character': 1}
    )
    filename = f"users/{username}.csv"
    save_profile(user, filename)
    
    
def save_user_profile(user: User):
    filename = f"users/{user.username}.csv"
    save_profile(user, filename)


def run_reccomendations(screen: pygame.Surface) -> None:
    """Visualize the project"""
    recommendations = {}
    global game_state
    screen.fill((255, 255, 255))
    draw_top_bar(screen, TOP_BAR_BACKGROUND_COLOUR, TOP_BAR_HEIGHT_PERCENTAGE)
    account_button = draw_account_button(screen)
    anime_spotlight = draw_anime_spotlight(screen)
    recommendation_display = draw_recommendation_display(screen)
    preference_display = draw_preference_display(screen)
    generate_button = recommendation_display.generate_button
    # episode_range_filter = draw_episode_range_filter(screen)
    year_filter = draw_year_filter(screen)


    # Import user into graph
    import_profile(f"users/{user.username}.csv", rec_graph)
    
    rec = rec_graph.get_all_path_scores(user)
    rec_anime = [anime[0] for anime in rec]
    # TODO PUT GENERATION HERE 
    recommendations = recommendation_display.update(rec_anime, anime_spotlight)

    while True:
        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)
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

        generate_button.update_colour(mouse_pos)
        if generate_button.is_clicked(is_clicking, mouse_pos):
            if year_filter.input_box_start.is_active:
                year_filter.input_box_start.update_activity()
            if year_filter.input_box_end.is_active:
                year_filter.input_box_end.update_activity()
            # Testing fileter exports
            # TODO UPDATE PROFILE
            new_rec_graph = read_file(['csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/anime_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/reviews_formatted_no_duplicates.csv'])
            d1 = datetime.date(year_filter.get_year_range()[0], 1, 1)
            d2 = datetime.date(year_filter.get_year_range()[1], 1, 1)
            date_range = (d1, d2)
            user.favorite_era = date_range
            prio = preference_display.get_preferences()
            user.priorities = prio
            save_profile(user, f"users/{user.username}.csv")
            import_profile(f"users/{user.username}.csv", new_rec_graph)
            rec = new_rec_graph.get_all_path_scores(user)
            rec_anime = [anime[0] for anime in rec]
            recommendations = recommendation_display.update(rec_anime, anime_spotlight)

        # Account button
        if account_button.update_colour(mouse_pos):
            fill_img(account_button.image, BACK_ARROW_HOVER_COLOUR)
        else:
            fill_img(account_button.image, BACK_ARROW_COLOUR)
        if account_button.is_clicked(is_clicking, mouse_pos):
            game_state = 'home'

        for recommendation in recommendations:
            # Update spotlight on button press
            if recommendations[recommendation][1].is_clicked(is_clicking, mouse_pos):
                if year_filter.input_box_start.is_active:
                    year_filter.input_box_start.update_activity()
                if year_filter.input_box_end.is_active:
                    year_filter.input_box_end.update_activity()
                anime_spotlight.update(recommendations[recommendation][0])
            # Update button colour on hover
            recommendations[recommendation][1].update_colour(mouse_pos)

        # Update Preference Meters
        for meter in preference_display.meters:
            curr_meter = preference_display.meters[meter]
            if curr_meter.is_clicked(is_clicking, mouse_pos):
                if year_filter.input_box_start.is_active:
                    year_filter.input_box_start.update_activity()
                if year_filter.input_box_end.is_active:
                    year_filter.input_box_end.update_activity()
                curr_meter.update(mouse_pos)

        # Year Filter
        if year_filter.input_box_start.is_clicked(is_clicking, mouse_pos):
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

        if year_filter.input_box_end.is_clicked(is_clicking, mouse_pos):
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
            sys.exit()

        if game_state != 'get_rec':
            break


def run_login(screen: pygame.Surface) -> None:
    """ Log-in Page """
    global game_state
    global curr_user
    
    Text(screen, 48, "Ani-4-me", 60, 180).draw()
    Text(screen, 30, "Get a recommendation on what to watch next by adding", 60, 230).draw()
    Text(screen, 30, "some of the animes that you have watched so far. Get", 60, 260).draw()
    Text(screen, 30, "started by adding your username.", 60, 290).draw()
    Text(screen, 30, "Username:", 60, 340).draw()
    username_btn = InputBox2(175, 335, 400, 32)
    login_btn = Button(screen, 35, 200, (60, 415), "Log-in", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))
    create_btn = Button(screen, 35, 200, (280, 415), "Create Account", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))

    login_btn.draw()
    create_btn.draw()
    fav_animes = set()
    while True:
        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        for event in events:
            username_btn.handle_event(event)

        pygame.draw.rect(screen, (255, 255, 255), (175, 335, 400, 32))
        username_btn.draw(screen)
        login_btn.update_colour(mouse_pos)
        create_btn.update_colour(mouse_pos)

        if login_btn.is_clicked(is_clicking, mouse_pos):
            get_user(username_btn.text)
            game_state = 'home'

        if create_btn.is_clicked(is_clicking, mouse_pos):
            game_state = 'sign-in'

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if game_state != 'main':
            break


def run_home(screen: pygame.Surface):

    global game_state
    screen.fill((255, 255, 255))
    Text(screen, 48, "Ani-4-me", 310, 240).draw()
    rate_btn = Button(screen, 35, 200, (180, 300), "Rate Anime", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))
    add_friends = Button(screen, 35, 200, (390, 300), "Add Friends", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))
    get_reccomendations = Button(screen, 35, 410, (180, 350), "Get Reccomendations", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))

    rate_btn.draw()
    add_friends.draw()
    get_reccomendations.draw()

    while True:
        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        rate_btn.update_colour(mouse_pos)
        add_friends.update_colour(mouse_pos)
        get_reccomendations.update_colour(mouse_pos)

        if rate_btn.is_clicked(is_clicking, mouse_pos):
            game_state = 'rate'

        if add_friends.is_clicked(is_clicking, mouse_pos):
            game_state = 'add_friends'

        if get_reccomendations.is_clicked(is_clicking, mouse_pos):
            game_state = 'get_rec'

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()

        if game_state != 'home':
            break


def run_add_friends(screen: pygame.Surface):
    global game_state
    global curr_user
    screen.fill((255, 255, 255))
    Text(screen, 36, "Add Friend", 60, 230).draw()
    Text(screen, 30, "Username:", 60, 300).draw()
    username_btn = InputBox2(175, 295, 400, 32)
    add_friend_btn = Button(screen, 35, 200, (60, 370), "Add Friend", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))
    add_friend_btn.draw()

    while True:
        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        for event in events:
            username_btn.handle_event(event)

        pygame.draw.rect(screen, (255, 255, 255), (175, 295, 400, 32))
        username_btn.draw(screen)

        add_friend_btn.update_colour(mouse_pos)
        if add_friend_btn.is_clicked(is_clicking, mouse_pos):
            friend_username = username_btn.text
            friend_user = get_user(friend_username)
            curr_user.friends_list.append(friend_user)

            game_state = 'home'

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()
            pygame.quit()
            sys.exit()

        if game_state != 'add_friends':
            break


def run_sign_in(screen: pygame.Surface):
    global game_state

    COLOR_INACTIVE = (217, 217, 217)
    COLOR_ACTIVE = (46, 81, 162)

    username_btn = InputBox2(175, 245, 400, 32)
    fav_anime_btn = InputBox2(175, 305, 400, 32)

    create_account_btn = Button(screen, 35, 200, (60, 370), "Create Account", (51, 51, 51), SECTION_TITLE_COLOUR,
                            (255, 255, 255))
    fav_animes = set()
    while True:
        # UI Elements
        Text(screen, 36, "Create Account", 60, 170).draw()
        Text(screen, 30, "Username:", 60, 250).draw()
        Text(screen, 30, "Fav Anime:", 60, 310).draw()
        create_account_btn.draw()

        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        for event in events:
            username_btn.handle_event(event)
            anime = fav_anime_btn.handle_event(event)
            if anime is not None:
                fav_animes.add(rec_graph.animes[int(anime)])

        create_account_btn.update_colour(mouse_pos)
        if create_account_btn.is_clicked(is_clicking, mouse_pos):
            create_profile(username_btn.text, fav_animes)
            game_state = 'home'

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (255, 255, 255), (175, 305, 400, 32))
        username_btn.draw(screen)

        pygame.draw.rect(screen, (255, 255, 255), (175, 295, 400, 32))
        fav_anime_btn.draw(screen)

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()
            pygame.quit()
            sys.exit()

        if game_state != 'sign-in':
            break


def run_rate_anime(screen: pygame.Surface):
    global game_state

    COLOR_INACTIVE = (217, 217, 217)
    COLOR_ACTIVE = (46, 81, 162)
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    anime_name_btn = InputBox2(200, 20, 400, 32)

    rank_story_btn = DropDown2([COLOR_INACTIVE, COLOR_ACTIVE],
                               [COLOR_INACTIVE, COLOR_ACTIVE], 200, 70, 400, 30,
                               pygame.font.SysFont('dm sans', 20), "Rank Story", values)
    rank_animation_btn = DropDown2([COLOR_INACTIVE, COLOR_ACTIVE],
                               [COLOR_INACTIVE, COLOR_ACTIVE], 200, 120, 400, 30,
                               pygame.font.SysFont('dm sans', 20), "Rank Animation", values)
    rank_sound_btn = DropDown2([COLOR_INACTIVE, COLOR_ACTIVE],
                                   [COLOR_INACTIVE, COLOR_ACTIVE], 200, 170, 400, 30,
                                   pygame.font.SysFont('dm sans', 20), "Rank Sound", values)
    rank_character_btn = DropDown2([COLOR_INACTIVE, COLOR_ACTIVE],
                                   [COLOR_INACTIVE, COLOR_ACTIVE], 200, 220, 400, 30,
                                   pygame.font.SysFont('dm sans', 20), "Rank Character", values)
    rank_enjoyment_btn = DropDown2([COLOR_INACTIVE, COLOR_ACTIVE],
                                   [COLOR_INACTIVE, COLOR_ACTIVE], 200, 270, 400, 30,
                                   pygame.font.SysFont('dm sans', 20), "Rank Enjoyment", values)

    rate_anime_btn = Button(screen, 35, 400, (200, 350), "Rate Anime", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))
    ratings = [0, 0, 0, 0, 0]
    # TODO
    while True:
        Text(screen, 20, "Anime Name:", 90, 30).draw()
        rate_anime_btn.draw()
        rank_enjoyment_btn.draw(screen)
        rank_character_btn.draw(screen)
        rank_sound_btn.draw(screen)
        rank_animation_btn.draw(screen)
        rank_story_btn.draw(screen)

        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        for event in events:
            anime_name_btn.handle_event(event)

        rate_anime_btn.update_colour(mouse_pos)

        if rate_anime_btn.is_clicked(is_clicking, mouse_pos):
            anime_name = int(anime_name_btn.text)
            add_anime(anime_name, ratings)
            game_state = 'home'


        selected_story = rank_story_btn.update(events)
        if selected_story >= 0:
            rank_story_btn.main = rank_story_btn.options[selected_story]

        selected_animation = rank_animation_btn.update(events)
        if selected_animation >= 0:
            rank_animation_btn.main = rank_animation_btn.options[selected_animation]

        selected_sound = rank_sound_btn.update(events)
        if selected_sound >= 0:
            rank_sound_btn.main = rank_sound_btn.options[selected_sound]

        selected_char = rank_character_btn.update(events)
        if selected_char >= 0:
            rank_character_btn.main = rank_character_btn.options[selected_char]

        selected_enjoyment = rank_enjoyment_btn.update(events)
        if selected_enjoyment >= 0:
            rank_enjoyment_btn.main = rank_enjoyment_btn.options[selected_enjoyment]

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (255, 255, 255), (200, 20, 400, 32))
        anime_name_btn.draw(screen)

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()
            pygame.quit()
            sys.exit()

        if game_state != 'rate':
            break


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



def run_project() -> None:
    screen = initialize_screen(SCREEN_SIZE, BACKGROUND_COLOUR)
    while True:
        if game_state == 'main':
            run_login(screen)
        elif game_state == 'home':
            run_home(screen)
        elif game_state == 'sign-in':
            run_sign_in(screen)
        elif game_state == 'rate':
            run_rate_anime(screen)
        elif game_state == 'add_friends':
            run_add_friends(screen)
        elif game_state == 'get_rec':
            run_reccomendations(screen)


if __name__ == "__main__":
    run_project()
