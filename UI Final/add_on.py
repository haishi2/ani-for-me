# Create Account:
# Use input box for favorite anime
# Everytime the user hits enter, favorite anime is added

# Rate Anime:
# Make the select Anime box an input text box



import pygame, sys
from ui_classes import AnimeSpotlight, RecommendationDisplay, PreferenceMeterDisplay, EpisodeRangeFilterDisplay, \
    GenreFilterDisplay, Button, AirDateFilterDisplay, Text, TextInputBox, InputBox2, DropDown2
from other_classes import Anime
from graph import ReccomenderGraph
from anime_and_users import Anime, User

Coord = int | float
Colour = tuple[int, int, int]

game_state = 'main'
curr_user = None

# Screen Constants
# 46, 81, 162
# 37, 65, 130

SCREEN_SIZE = (800, 600)
FONT_STYLE = 'dm sans'
BACKGROUND_COLOUR = (255, 255, 255)
SECTION_TITLE_COLOUR = (46, 81, 162)


def get_user(username: str) -> User:
    graph = ReccomenderGraph()
    user = graph.users[username]
    return user


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
        elif game_state == 'rank-pref':
            run_rank_preferences(screen)


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
            # curr_user = get_user(username_btn.text)
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
            game_state = 'rank-pref'

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()

        if game_state != 'home':
            break


def run_add_friends(screen: pygame.Surface):
    global game_state
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
            game_state = 'home'
            # append friends

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
    create_account_btn = Button(screen, 35, 200, (60, 370), "Create Account", (51, 51, 51), SECTION_TITLE_COLOUR,
                            (255, 255, 255))
    anime_dropdown_btn = DropDown2([COLOR_INACTIVE, COLOR_ACTIVE],
                                   [COLOR_INACTIVE, COLOR_ACTIVE], 175, 305, 400, 30,
                                   pygame.font.SysFont('dm sans', 20), "Select Anime", ['x', 'y'])

    while True:
        # UI Elements
        Text(screen, 36, "Create Account", 60, 170).draw()
        Text(screen, 30, "Username:", 60, 250).draw()
        Text(screen, 30, "Fav Anime:", 60, 310).draw()
        create_account_btn.draw()
        anime_dropdown_btn.draw(screen)

        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        for event in events:
            username_btn.handle_event(event)

        create_account_btn.update_colour(mouse_pos)
        if create_account_btn.is_clicked(is_clicking, mouse_pos):
            game_state = 'home'

        selected_option = anime_dropdown_btn.update(events)
        if selected_option >= 0:
            anime_dropdown_btn.main = anime_dropdown_btn.options[selected_option]

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (255, 255, 255), (175, 295, 400, 32))
        username_btn.draw(screen)

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

    anime_dropdown_btn = DropDown2([COLOR_INACTIVE, COLOR_ACTIVE],
                                   [COLOR_INACTIVE, COLOR_ACTIVE], 200, 20, 400, 30,
                                   pygame.font.SysFont('dm sans', 20), "Select Anime", ['x', 'y'])
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

    rate_anime_btn = Button(screen, 35, 400, (200, 350), "Get Reccomendations", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))


    while True:
        rate_anime_btn.draw()
        rank_enjoyment_btn.draw(screen)
        rank_character_btn.draw(screen)
        rank_sound_btn.draw(screen)
        rank_animation_btn.draw(screen)
        rank_story_btn.draw(screen)
        anime_dropdown_btn.draw(screen)

        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        rate_anime_btn.update_colour(mouse_pos)

        if rate_anime_btn.is_clicked(is_clicking, mouse_pos):
            # curr_user = get_user(username_btn.text)
            game_state = 'home'

        selected_option = anime_dropdown_btn.update(events)
        if selected_option >= 0:
            anime_dropdown_btn.main = anime_dropdown_btn.options[selected_option]

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

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()
            pygame.quit()
            sys.exit()

        if game_state != 'rate':
            break


def run_rank_preferences(screen: pygame.Surface):
    global game_state

    COLOR_INACTIVE = (217, 217, 217)
    COLOR_ACTIVE = (46, 81, 162)
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

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

    get_rec_btn = Button(screen, 35, 400, (200, 350), "Get Reccomendations", (51, 51, 51), SECTION_TITLE_COLOUR, (255, 255, 255))


    while True:
        get_rec_btn.draw()
        rank_enjoyment_btn.draw(screen)
        rank_character_btn.draw(screen)
        rank_sound_btn.draw(screen)
        rank_animation_btn.draw(screen)
        rank_story_btn.draw(screen)

        pygame.display.flip()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        is_clicking = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        get_rec_btn.update_colour(mouse_pos)

        if get_rec_btn.is_clicked(is_clicking, mouse_pos):
            # curr_user = get_user(username_btn.text)
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

        if any(event.type == pygame.QUIT for event in events):
            pygame.display.quit()
            pygame.quit()
            pygame.quit()
            sys.exit()

        if game_state != 'rank-pref':
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


if __name__ == "__main__":
    run_project()
