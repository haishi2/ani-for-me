""" User Input """

import pygame, time, sys
from typing import Optional
# from anime_and_users import User
from screen_elements import Button, InputBox, Text, DropDown


class Form:
    """ Page class """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.canvas = pygame.Surface((800, 600))
        self.actions = {"login": False, "home": False, "rate_anime": False, "add_friend": False, "rank": False,
                        "get_rec" : False}
        self.dt, self.prev_time = 0, 0
        self.running = True
        self.state_stack = []

    def page_loop(self):
        while self._running:
            self.get_events()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                pygame.quit()
                sys.exit()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.canvas)
        # Render current state to the screen
        self.screen.blit(pygame.transform.scale(self.canvas, (800, 600)), (0, 0))
        pygame.display.flip()

    def load_states(self):
        self.login_screen = Login(self)
        self.state_stack.append(self.login_screen)

    def form_loop(self):
        while self.running:
            self.get_dt()
            self.load_states()
            self.get_events()
            self.update()
            self.render()


class State():
    def __init__(self, form):
        self.form = form
        self.prev_state = None

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.form.state_stack) > 1:
            self.prev_state = self.form.state_stack[-1]
        self.form.state_stack.append(self)

    def exit_state(self):
        self.form.state_stack.pop()


class Login(State):

    def __init__(self, form):
        State.__init__(self, form)

    # def update(self, delta_time, actions):
        # if actions["start"]:
        #     new_state = Game_World(self.game)
        #     new_state.enter_state()
        # self.game.reset_keys()

    def render(self, display):
        screen = self.form.canvas
        display.fill((255, 255, 255))
        Text(screen, 20, "Hello, there! Welcome to ", 60, 150).draw()
        Text(screen, 48, "Ani4me", 60, 180, True).draw()
        Text(screen, 20, "Get a recommendation on what to watch next by adding", 60, 250).draw()
        Text(screen, 20, "some of the animes that you have watched so far. Get", 60, 280).draw()
        Text(screen, 20, "started by adding your username.", 60, 310).draw()
        Text(screen, 20, "Username:", 60, 360).draw()

        # need to update input box
        usernamebtn = InputBox(screen, 35, 400, 180, 360, '', (217, 217, 217), (51, 51, 51))

        # need to update button
        loginbtn = Button(screen, 35, 200, (60, 420), "Log-in", (51, 51, 51), (30, 77, 245), (255, 255, 255))
        loginbtn.draw()
        usernamebtn.draw()

        event_list = pygame.event.get()
        for event in event_list:
            usernamebtn.handle_event(event)
            loginbtn.handle_event(event)
        usernamebtn.update()


class HomePage(State):
    def __init__(self, form):
        State.__init__(self, form)

    def render(self, display):
        screen = self.form.canvas
        display.fill((255, 255, 255))
        Text(screen, 48, "Ani4me", 60, 220, True).draw()
        rate_anime_btn = Button(screen, 35, 200, (60, 300), "Rate Anime", (51, 51, 51), (30, 77, 245), (255, 255, 255))
        add_friends_btn = Button(screen, 35, 200, (265, 300), "Add Friends", (51, 51, 51), (30, 77, 245),
                                 (255, 255, 255))
        get_rec_btn = Button(screen, 35, 200, (265, 465), "Get Reccomendations", (51, 51, 51), (30, 77, 245),
                             (255, 255, 255))

        rate_anime_btn.draw()
        add_friends_btn.draw()
        get_rec_btn.draw()


class AddFriendPage(State):
    def __init__(self, form):
        State.__init__(self, form)

    def render(self, display):
        screen = self.form.canvas
        display.fill((255, 255, 255))
        Text(screen, 36, "Add Friend", 60, 230, True).draw()
        add_friend_btn = Button(screen, 35, 200, (60, 370), "Add Friend", (51, 51, 51), (30, 77, 245),
                                (255, 255, 255))
        friend_usernamebtn = InputBox(screen, 35, 400, 140, 300, '', (217, 217, 217), (51, 51, 51))
        Text(screen, 20, "Name:", 60, 300).draw()

        add_friend_btn.draw()
        friend_usernamebtn.draw()


class RankCategoriesPage(State):
    def __init__(self, form):
        State.__init__(self, form)

    def render(self, display):
        screen = self.form.canvas
        display.fill((255, 255, 255))
        Text(screen, 36, "Rank the Categories", 60, 115, True).draw()
        Text(screen, 20, "Story:", 60, 200).draw()
        Text(screen, 20, "Animation:", 60, 250).draw()
        Text(screen, 20, "Sound:", 60, 300).draw()
        Text(screen, 20, "Character:", 60, 350).draw()
        Text(screen, 20, "Enjoyment:", 60, 400).draw()

        rate_btn = Button(screen, 35, 300, (60, 480), "Get Reccomendations", (51, 51, 51), (30, 77, 245),
                          (255, 255, 255))
        rate_btn.draw()

        COLOR_INACTIVE = (217, 217, 217)
        COLOR_ACTIVE = (30, 77, 245)
        values = [range(1, 11)]

        ranking_btn_story = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                     [COLOR_INACTIVE, COLOR_ACTIVE], 200, 200, 400, 30,
                                     pygame.font.SysFont('Arial', 20),
                                     "Rate", values)
        ranking_btn_animation = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                         [COLOR_INACTIVE, COLOR_ACTIVE], 200, 250, 400, 30,
                                         pygame.font.SysFont('Arial', 20),
                                         "Rate", values)
        ranking_btn_sound = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                     [COLOR_INACTIVE, COLOR_ACTIVE], 200, 300, 400, 30,
                                     pygame.font.SysFont('Arial', 20),
                                     "Rate", values)
        ranking_btn_character = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                         [COLOR_INACTIVE, COLOR_ACTIVE], 200, 350, 400, 30,
                                         pygame.font.SysFont('Arial', 20),
                                         "Rate", values)
        ranking_btn_enjoyment = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                         [COLOR_INACTIVE, COLOR_ACTIVE], 200, 400, 400, 30,
                                         pygame.font.SysFont('Arial', 20),
                                         "Rate", values)

        ranking_btn_story.draw(screen)
        ranking_btn_animation.draw(screen)
        ranking_btn_sound.draw(screen)
        ranking_btn_character.draw(screen)
        ranking_btn_enjoyment.draw(screen)


class RateAnimePage(State):
    def __init__(self, form):
        State.__init__(self, form)

    def render(self, display):
        screen = self.form.canvas
        display.fill((255, 255, 255))

        Text(screen, 36, "Rate Anime", 60, 90, True).draw()
        Text(screen, 20, "Name:", 60, 150).draw()
        Text(screen, 20, "Story:", 60, 200).draw()
        Text(screen, 20, "Animation:", 60, 250).draw()
        Text(screen, 20, "Sound:", 60, 300).draw()
        Text(screen, 20, "Character:", 60, 350).draw()
        Text(screen, 20, "Enjoyment:", 60, 400).draw()
        rate_anime_btn = Button(screen, 35, 200, (60, 480), "Rate Anime", (51, 51, 51), (30, 77, 245),
                                (255, 255, 255))
        rate_anime_btn.draw()

        COLOR_INACTIVE = (217, 217, 217)
        COLOR_ACTIVE = (30, 77, 245)
        values = [range(1, 11)]

        anime_dropdown_btn = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                      [COLOR_INACTIVE, COLOR_ACTIVE], 200, 150, 400, 30,
                                      pygame.font.SysFont('Arial', 20), "Select Anime", ['x', 'y'])
        ranking_btn_story = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                     [COLOR_INACTIVE, COLOR_ACTIVE], 200, 200, 400, 30,
                                     pygame.font.SysFont('Arial', 20),
                                     "Rate", values)
        ranking_btn_animation = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                         [COLOR_INACTIVE, COLOR_ACTIVE], 200, 250, 400, 30,
                                         pygame.font.SysFont('Arial', 20),
                                         "Rate", values)
        ranking_btn_sound = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                     [COLOR_INACTIVE, COLOR_ACTIVE], 200, 300, 400, 30,
                                     pygame.font.SysFont('Arial', 20),
                                     "Rate", values)
        ranking_btn_character = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                         [COLOR_INACTIVE, COLOR_ACTIVE], 200, 350, 400, 30,
                                         pygame.font.SysFont('Arial', 20),
                                         "Rate", values)
        ranking_btn_enjoyment = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                                         [COLOR_INACTIVE, COLOR_ACTIVE], 200, 400, 400, 30,
                                         pygame.font.SysFont('Arial', 20),
                                         "Rate", values)

        anime_dropdown_btn.draw(screen)
        ranking_btn_story.draw(screen)
        ranking_btn_animation.draw(screen)
        ranking_btn_sound.draw(screen)
        ranking_btn_character.draw(screen)
        ranking_btn_enjoyment.draw(screen)



if __name__ == "__main__":
    f = Form()
    while f.running:
        f.form_loop()
