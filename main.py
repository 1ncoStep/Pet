import json
import random
import pygame as pg

pg.init()


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

IMAGE_SIZE = 80
PADDING = 5

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 45

DOG_WIDTH = 310
DOG_HEIGHT = 500

FOOD_SIZE = 200

TOY_SIZE = 100

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130


def download(name, width, height):
    image = pg.image.load(name)
    image = pg.transform.scale(image, (width, height))

    return image


def text_render(text, font_size=40, color='black'):
    font = pg.font.Font(None, font_size)

    return font.render(str(text), True, color)


class Button:
    def __init__(self, x, y, text, text_size=40, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, func=None):
        self.width = width
        self.height = height
        self.idle_image = download('images/button.png', width, height)
        self.pressed_image = download('images/button_clicked.png', width, height)
        self.image = self.idle_image
        self.button_rect = self.image.get_rect()
        self.button_rect.topleft = (x, y)
        self.func = func
        self.text_size = text_size
        self.text = text_render(text, self.text_size)
        self.text_rect = self.text.get_rect(center=self.button_rect.center)

        self.is_pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.button_rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()

        if self.button_rect.collidepoint(mouse_pos):
            if self.is_pressed == False:
                self.image = self.idle_image

            else:
                self.image = self.pressed_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.is_pressed = False


class Items:
    def __init__(self, name, price, png, is_using, is_bought):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_using

        self.png = png
        self.image = download(png, DOG_WIDTH / 1.7, DOG_HEIGHT / 1.7)
        self.full_image = download(png, DOG_WIDTH, DOG_HEIGHT)


class ClothesMenu:
    def __init__(self, game, data, current_item):
        self.game = game
        self.menu_page = download('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = download('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = download('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = download('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = download('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = []

        for item in data:
            self.items.append(Items(*item.values()))

        self.current_item = current_item

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.next_button = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Вперёд',
                                  width=int(BUTTON_WIDTH / 1.2), height=int(BUTTON_HEIGHT / 1.2), func=self.__to_next)
        self.back_button = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 1.63, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Назад',
                                  width=int(BUTTON_WIDTH / 1.2), height=int(BUTTON_HEIGHT / 1.2), func=self.__back)

        self.is_put_on_button = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 1.63, SCREEN_HEIGHT - MENU_NAV_YPAD - BUTTON_HEIGHT, 'Надеть',
                                  width=int(BUTTON_WIDTH / 1.2), height=int(BUTTON_HEIGHT / 1.2), func=self.__put_on)

        self.buy_button = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 3.322,
                                       SCREEN_HEIGHT - MENU_NAV_YPAD - BUTTON_HEIGHT, 'Купить',
                                       width=int(BUTTON_WIDTH / 1.2), height=int(BUTTON_HEIGHT / 1.2),
                                       func=self.__buy)

    def __to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        else:
            self.current_item = 0

    def __back(self):
        if self.current_item > 0:
            self.current_item -= 1

        else:
            self.current_item = len(self.items) - 1

    def __buy(self):
        if self.game.coins >= self.items[self.current_item].price:
            if self.items[self.current_item].is_bought is False:
                self.game.coins -= self.items[self.current_item].price

                self.items[self.current_item].is_bought = True

    def __put_on(self):
        if self.items[self.current_item].is_bought is True:
            self.items[self.current_item].is_put_on = True

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        screen.blit(text_render(self.items[self.current_item].price), (SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 4,
                                       SCREEN_HEIGHT - MENU_NAV_YPAD - BUTTON_HEIGHT - SCREEN_HEIGHT / 2.6))
        screen.blit(text_render(self.items[self.current_item].name),
                    (SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 1.65,
                     SCREEN_HEIGHT - MENU_NAV_YPAD - BUTTON_HEIGHT - SCREEN_HEIGHT / 2))

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_off, (0, 0))

        else:
            screen.blit(self.bottom_label_on, (0, 0))

        if self.items[self.current_item].is_put_on:
            for check in self.items:
                if check.name != self.items[self.current_item].name and check.is_put_on is True:
                    check.is_put_on = False

            screen.blit(self.top_label_off, (0, 0))

        else:
            screen.blit(self.top_label_on, (0, 0))

        screen.blit(text_render('Надето'), (647, 113))
        screen.blit(text_render('Куплено'), (642, 181))

        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.is_put_on_button.draw(screen)
        if self.items[self.current_item].is_bought is False:
            self.buy_button.draw(screen)

    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.is_put_on_button.update()
        if self.items[self.current_item].is_bought is False:
            self.buy_button.update()

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.__back()

        if keys[pg.K_RIGHT]:
            self.__to_next()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.is_put_on_button.is_clicked(event)
        if self.items[self.current_item].is_bought is False:
            self.buy_button.is_clicked(event)


class Eat:
    def __init__(self, name, image, price, satiety, med_power=0):
        self.name = name
        self.image = download(image, FOOD_SIZE, FOOD_SIZE)
        self.price = price
        self.satiety = satiety
        self.med_power = med_power


class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = download('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = download('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = download('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = download('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = download('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.food = [
            Eat('Яблоко', 'images/food/apple.png', 50, 1),
            Eat('Кость', 'images/food/bone.png', 200, 5),
            Eat('Корм', 'images/food/dog food.png', 250, 7),
            Eat('Элитный корм', 'images/food/dog food elite.png', 1000, 10),
            Eat('Мясо', 'images/food/meat.png', 1200, 15),
            Eat('Лекарство', 'images/food/medicine.png', 10000, 0, 1),

        ]

        self.current_food = 0

        self.food_rect = self.food[0].image.get_rect()
        self.food_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.next_button = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Вперёд',
                                  width=int(BUTTON_WIDTH / 1.2), height=int(BUTTON_HEIGHT / 1.2), func=self.__to_next)
        self.back_button = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 1.63, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Назад',
                                  width=int(BUTTON_WIDTH / 1.2), height=int(BUTTON_HEIGHT / 1.2), func=self.__back)

        self.eat_button = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 3.322,
                                       SCREEN_HEIGHT - MENU_NAV_YPAD - BUTTON_HEIGHT, 'Съесть',
                                       width=int(BUTTON_WIDTH / 1.2), height=int(BUTTON_HEIGHT / 1.2),
                                       func=self.__eat_and_health)

    def __to_next(self):
        if self.current_food != len(self.food) - 1:
            self.current_food += 1

        else:
            self.current_food = 0

    def __eat_and_health(self):
        if self.game.coins >= self.food[self.current_food].price:
            self.game.coins -= self.food[self.current_food].price

        if self.game.satiety + self.food[self.current_food].satiety > 100:
            self.game.satiety = 100

        else:
            self.game.satiety += self.food[self.current_food].satiety

        if self.game.health + self.food[self.current_food].med_power > 100:
            self.game.health = 100

        else:
            self.game.health += self.food[self.current_food].med_power

    def __back(self):
        if self.current_food != 0:
            self.current_food -= 1

        else:
            self.current_food = len(self.food) - 1

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.food[self.current_food].image, self.food_rect)
        screen.blit(text_render(self.food[self.current_food].price), (SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 4,
                                       SCREEN_HEIGHT - MENU_NAV_YPAD - BUTTON_HEIGHT - SCREEN_HEIGHT / 2.6))
        screen.blit(text_render(self.food[self.current_food].name), (SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - SCREEN_WIDTH / 1.65,
                                       SCREEN_HEIGHT - MENU_NAV_YPAD - BUTTON_HEIGHT - SCREEN_HEIGHT / 2))

        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.eat_button.draw(screen)

    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.eat_button.update()

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.__back()

        if keys[pg.K_RIGHT]:
            self.__to_next()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.eat_button.is_clicked(event)


class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.red_bone = download('images/toys/red bone.png', TOY_SIZE, TOY_SIZE)
        self.blue_bone = download('images/toys/blue bone.png', TOY_SIZE, TOY_SIZE)
        self.ball = download('images/toys/ball.png', TOY_SIZE, TOY_SIZE)
        self.toys = [self.blue_bone, self.red_bone, self.ball]

        self.image = random.choice(self.toys)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(105, 700)
        self.rect.y = 5

    def update(self):
        self.rect.y += 1

        if self.rect.y > 445:
            self.kill()


class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = download('images/dog.png', DOG_WIDTH / 2, DOG_HEIGHT / 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (380, 284)

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and self.rect.x > 88:
            self.rect.left -= 2

        if keys[pg.K_RIGHT] and self.rect.x < 770 - TOY_SIZE:
            self.rect.left += 2


class MiniGame:
    def __init__(self, game):
        self.game = game

        self.background = download('images/game_background.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 15000

    def new_game(self):
        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 15000

    def update(self):
        self.dog.update()
        self.toys.update()

        if random.randint(0, 75) == 0:
            self.toys.add(Toy())

        hits = pg.sprite.spritecollide(self.dog, self.toys, True)
        self.score += len(hits)

        if pg.time.get_ticks() - self.start_time > self.interval:
            if self.game.mode == 'game':
                if self.game.happiness + self.score > 100:
                    self.game.happiness = 100

                else:
                    self.game.happiness += int(self.score) // 2

            self.game.mode = 'menu'

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        screen.blit(self.dog.image, self.dog.rect)

        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))

        self.toys.draw(screen)


class Game:
    def __init__(self):

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        self.background = download(r'images\background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.happiness_icon = download('images/happiness.png', IMAGE_SIZE, IMAGE_SIZE)
        self.satiety_icon = download('images/satiety.png', IMAGE_SIZE, IMAGE_SIZE)
        self.health_icon = download('images/health.png', IMAGE_SIZE, IMAGE_SIZE)
        self.coin_icon = download('images/money.png', IMAGE_SIZE, IMAGE_SIZE)
        self.puppy = download('images/dog.png', DOG_WIDTH, DOG_HEIGHT)

        self.happy_face = download('images/happy_face.png', DOG_WIDTH, DOG_HEIGHT)
        self.sad_face = download('images/sad_face.png', DOG_WIDTH, DOG_HEIGHT)
        self.sick_face = download('images/sick_face.png', DOG_WIDTH, DOG_HEIGHT)

        with open('game_settings.json', encoding="utf-8") as jsn:
            data = json.load(jsn)

        self.happiness = data["happiness"]
        self.satiety = data["satiety"]
        self.health = data["health"]
        self.coins = data["money"]

        self.button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING
        self.button_y = PADDING + IMAGE_SIZE

        self.clothes_menu = ClothesMenu(self, data["clothes"], data["current item"])
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)

        self.mode = 'menu'

        self.upgrades = {}

        for key, value in data["upgrades"].items():
            self.upgrades[int(key)] = value

        self.coins_per_second = data["coins_per_second"]

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 2000)

        self.DECREASE_STATS = pg.USEREVENT + 2
        pg.time.set_timer(self.DECREASE_STATS, 100000)

        self.eat_button = Button(self.button_x, self.button_y, 'Еда', func=self.food_menu_on)
        self.clothes_button = Button(self.button_x, self.button_y + 50, 'Одежда', func=self.clothes_menu_on)
        self.games_button = Button(self.button_x, self.button_y + 100, 'Игры', func=self.game_on)
        self.upgrade_button = Button(640, 10, 'Улучшить', 25,  BUTTON_WIDTH / 1.5, BUTTON_HEIGHT / 1.5, func=self.increase_money)
        self.buttons = [self.eat_button, self.clothes_button, self.games_button, self.upgrade_button]

        self.run()

    def increase_money(self):
        if self.upgrade_button.is_pressed is True:
            for prices, is_bought in self.upgrades.items():
                if is_bought is False and prices <= self.coins:
                    self.coins_per_second += 1
                    self.coins -= prices
                    self.upgrades[prices] = True

                    break

    def clothes_menu_on(self):
        self.mode = 'clothes'

    def food_menu_on(self):
        self.mode = 'food'

    def game_on(self):
        self.mode = 'game'
        self.mini_game.new_game()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.increase_money()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == 'game over':
                    default_data = {
                        "happiness": 100,
                        "satiety": 100,
                        "health": 100,
                        "money": 0,
                        "coins_per_second": 1,
                        "upgrades": {
                            "100": False,
                            "1000": False,
                            "5000": False,
                            "10000": False,
                            "100000": False
                        },
                        "current item": 0,
                        "clothes": [
                            {"name": "Синяя футболка", "price": 100, "image": "images/items/blue t-shirt.png",
                             "is_bought": False, "is_put_on": False},
                            {"name": "Красная футболка", "price": 100, "image": "images/items/red t-shirt.png",
                             "is_bought": False, "is_put_on": False},
                            {"name": "Ботинки", "price": 200, "image": "images/items/boots.png", "is_bought": False,
                             "is_put_on": False},
                            {"name": "Бант", "price": 75, "image": "images/items/bow.png", "is_bought": False,
                             "is_put_on": False},
                            {"name": "Каска", "price": 225, "image": "images/items/cap.png", "is_bought": False,
                             "is_put_on": False},
                            {"name": "Шляпа", "price": 300, "image": "images/items/hat.png", "is_bought": False,
                             "is_put_on": False},
                            {"name": "Солнцезащитные очки", "price": 500, "image": "images/items/sunglasses.png",
                             "is_bought": False, "is_put_on": False},
                            {"name": "Серебрянная цепь", "price": 1000, "image": "images/items/silver chain.png",
                             "is_bought": False, "is_put_on": False},
                            {"name": "Золотая цепь", "price": 10000, "image": "images/items/gold chain.png",
                             "is_bought": False, "is_put_on": False}
                        ]
                    }

                    with open('game_settings.json', 'w', encoding='utf-8') as new_jsn:
                        json.dump(default_data, new_jsn, ensure_ascii=False)

                else:
                    rerun_data = {
                          "happiness": self.happiness,
                          "satiety": self.satiety,
                          "health": self.health,
                          "money": self.coins,
                          "coins_per_second": self.coins_per_second,
                          "upgrades": self.upgrades,
                          "current item": self.clothes_menu.current_item,
                          "clothes": []
                        }

                    for item in self.clothes_menu.items:
                        rerun_data["clothes"].append({
                            "name": item.name,
                            "price": item.price,
                            "image": item.png,
                            "is_bought": item.is_bought,
                            "is_put_on": item.is_put_on
                        })

                    with open('game_settings.json', 'w', encoding='utf-8') as new_jsn:
                        json.dump(rerun_data, new_jsn, ensure_ascii=False)

                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = 'menu'

            if self.mode == 'menu':
                for click in self.buttons:
                    click.is_clicked(event)

            if event.type == self.INCREASE_COINS:
                self.coins += self.coins_per_second

            if event.type == self.DECREASE_STATS:
                stat = random.randint(1, 100)

                if stat in range(1, 50):
                    self.satiety -= 1

                elif stat in range(51, 89):
                    self.happiness -= 1

                else:
                    self.health -= 1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.coins += 1

            if pg.sprite.spritecollide(self.mini_game.dog, self.mini_game.toys, True):
                self.mini_game.score += 1

            self.clothes_menu.is_clicked(event)
            self.food_menu.is_clicked(event)

    def update(self):
        for up in self.buttons:
            up.update()

        if self.mode == 'clothes':
            self.clothes_menu.update()

        elif self.mode == 'food':
            self.food_menu.update()

        elif self.mode == 'game':
            self.mini_game.update()

    def draw(self):
        if self.health == 0 or self.happiness == 0 or self.satiety == 0:
            self.mode = 'game over'

        if self.mode != 'game over':
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.happiness_icon, (PADDING, PADDING))
            self.screen.blit(self.satiety_icon, (PADDING, PADDING * 2 + IMAGE_SIZE))
            self.screen.blit(self.health_icon, (PADDING, PADDING * 4 + IMAGE_SIZE * 2))
            self.screen.blit(self.coin_icon, (SCREEN_WIDTH - PADDING * 17, PADDING))
            self.screen.blit(self.puppy, (SCREEN_WIDTH / 2 - 155, SCREEN_HEIGHT / 2 - 250))

            self.screen.blit(text_render(self.happiness), (PADDING + IMAGE_SIZE, PADDING * 6))
            self.screen.blit(text_render(self.satiety), (PADDING + IMAGE_SIZE, PADDING * 23))
            self.screen.blit(text_render(self.health), (PADDING + IMAGE_SIZE, PADDING * 40))
            self.screen.blit(text_render(self.coins), (770, PADDING * 6))

            if self.health < 50 or self.satiety < 50:
                self.screen.blit(self.sick_face, (SCREEN_WIDTH / 2 - 155, SCREEN_HEIGHT / 2 - 250))

            elif self.happiness == 100:
                self.screen.blit(self.happy_face, (SCREEN_WIDTH / 2 - 155, SCREEN_HEIGHT / 2 - 250))

            elif self.happiness < 50:
                self.screen.blit(self.sad_face, (SCREEN_WIDTH / 2 - 155, SCREEN_HEIGHT / 2 - 250))

            if self.clothes_menu.items[self.clothes_menu.current_item].is_put_on is True:
                self.screen.blit(self.clothes_menu.items[self.clothes_menu.current_item].full_image, (SCREEN_WIDTH / 2 - 155, SCREEN_HEIGHT / 2 - 250))

            else:
                for item in self.clothes_menu.items:
                    if item.is_put_on is True:
                        self.screen.blit(item.full_image, (SCREEN_WIDTH / 2 - 155, SCREEN_HEIGHT / 2 - 250))

            for draw_buttons in self.buttons:
                draw_buttons.draw(self.screen)

            if self.mode == 'clothes':
                self.clothes_menu.draw(self.screen)

            if self.mode == 'food':
                self.food_menu.draw(self.screen)

            if self.mode == 'game':
                self.mini_game.draw(self.screen)
                self.mini_game.update()

        else:
            pg.draw.rect(self.screen, 'black', pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

            last_text = text_render('ИГРА ОКОНЧЕНА', 145, 'white')
            last_text_rect = last_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(last_text, last_text_rect)

        pg.display.flip()


if __name__ == "__main__":
    Game()