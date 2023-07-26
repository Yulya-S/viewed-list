import pygame
from code.data_base import *
from code.coefficients import *


class Content_box():
    def __init__(self, text='', mod='standard', auxiliary_sheet=[], width=300):
        self.text = text
        self.mod = mod
        self.auxiliary_sheet = auxiliary_sheet
        self.width = width
        self.active = False
        self.hovered = False
        self.animation = 0
        self.offset = 0
        self.step = 0
        self.auxiliary_hovered = []

    def draw(self, mouse_pos, coordinates, color_schem):
        rect = pygame.Rect(coordinates[0], coordinates[1], self.width, 50)
        self.hovered = rect.collidepoint(mouse_pos[0], mouse_pos[1])
        outline_color = color_schemes[color_schem][4]
        if self.active:
            outline_color = color_schemes[color_schem][6]
            self.animation += 1
            self.auxiliary(mouse_pos, (coordinates[0], coordinates[1] + 49), color_schem)
        elif self.hovered:
            outline_color = color_schemes[color_schem][5]

        if not self.active or self.animation > 30:
            self.animation = 0

        text = self.text
        if self.mod == 'locked':
            text = ''.join(['*' for _ in range(len(self.text))])

        text, display_offset, self.step = cut_to_size(self.width, text, self.offset)

        draw_text_in_block(text, coordinates, (self.width, 50), outline_color, animation=(self.animation > 15),
                           text_offset=display_offset, dot=False)

        if self.step < 0:
            draw_text('<-', outline_color, (coordinates[0] + 5, coordinates[1] + 5))
        if self.text != text and self.offset:
            draw_text('->', outline_color, (coordinates[0] + self.width - 35, coordinates[1] + 5))

    def auxiliary(self, mouse_pos, coordinates, color_schem):
        auxiliary_sheet = []
        for auxiliary_sheet_index in range(len(self.auxiliary_sheet)):
            index = self.auxiliary_sheet[auxiliary_sheet_index].find(self.text)
            if index != -1:
                auxiliary_sheet.append(auxiliary_sheet_index)
            if len(auxiliary_sheet) > 4:
                break

        self.auxiliary_hovered = []
        for i in range(len(auxiliary_sheet)):
            if pygame.Rect(coordinates[0], coordinates[1] + 39 * i, 300, 40).collidepoint(mouse_pos[0], mouse_pos[1]):
                self.auxiliary_hovered.append(auxiliary_sheet[i])

        if self.hovered or len(self.auxiliary_hovered) != 0:
            coordinates = [coordinates[0], coordinates[1]]
            for i in auxiliary_sheet:
                index = self.auxiliary_sheet[i].find(self.text)
                pygame.draw.rect(screen, color_schemes[color_schem][0], (coordinates[0], coordinates[1], 300, 40))
                pygame.draw.rect(screen, color_schemes[color_schem][4], (coordinates[0], coordinates[1], 300, 40), 1)
                left = font.render(self.auxiliary_sheet[i][:index], True, white).get_width()
                width = font.render(self.text, True, white).get_width()
                pygame.draw.rect(screen, color_schemes[color_schem][2],
                                 (coordinates[0] + left + 10, coordinates[1] + 5, width, 30))
                outline_color = color_schemes[color_schem][4]
                if i in self.auxiliary_hovered:
                    outline_color = color_schemes[color_schem][5]
                draw_text(self.auxiliary_sheet[i], outline_color, (coordinates[0] + 5, coordinates[1] + 20), 290)
                coordinates[1] += 39

    def write(self, event):
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) != 0 and self.offset != len(self.text):
                    self.text = self.text[:len(self.text) - self.offset - 1] + self.text[len(self.text) - self.offset:]
            elif event.key == pygame.K_DELETE:
                if len(self.text) != 0 and self.offset != 0:
                    self.text = self.text[:len(self.text) - self.offset] + self.text[len(self.text) - self.offset + 1:]
                    self.offset -= 1
            elif event.key == pygame.K_LEFT:
                if self.offset != len(self.text):
                    self.offset += 1
            elif event.key == pygame.K_RIGHT:
                if self.offset:
                    self.offset -= 1
            elif (self.mod != 'number' or str(event.unicode) in '0123456789') and \
                    event.mod not in [pygame.KMOD_LCTRL, pygame.KMOD_RCTRL] and event.key != pygame.K_TAB:
                text = self.text[:len(self.text) - self.offset] + str(event.unicode) + \
                       self.text[len(self.text) - self.offset:]
                if self.mod != 'number' and len(text) <= 255:
                    self.text = text
                elif self.mod == 'number' and int(text) < 9223372036854775807:
                    self.text = text

    def press(self, event):
        if event.button == 1 and len(self.auxiliary_hovered) != 0:
            self.text = self.auxiliary_sheet[self.auxiliary_hovered[0]]


class Radio_button():
    def __init__(self, button_names, active=0):
        self.button_names = button_names
        self.active = active
        self.hovered = [False for _ in button_names]

    def draw(self, mouse_pos, coordinates, color_schem):
        cord = [coordinates[0], coordinates[1]]
        for i in range(len(self.button_names)):
            self.hovered[i] = pygame.draw.circle(screen, white, cord, 15, 1).collidepoint(mouse_pos[0], mouse_pos[1])
            color = color_schemes[color_schem][4]
            if self.hovered[i]:
                color = color_schemes[color_schem][5]
            pygame.draw.circle(screen, white, cord, 15)
            pygame.draw.circle(screen, color, cord, 15, 1)
            if i == self.active:
                pygame.draw.circle(screen, color, cord, 8)
            draw_text(self.button_names[i], color, (cord[0] + 20, cord[1] - 2))
            cord[1] += 40
            if i != 0 and i % 4 == 0:
                cord[1] = coordinates[1]
                cord[0] += 190

    @property
    def press(self):
        if True in self.hovered:
            self.active = self.hovered.index(True)


class Cheak_button():
    def __init__(self, button_names, active):
        self.button_names = button_names
        self.active = [False for _ in button_names]
        for i in active:
            self.active[i] = True
        self.hovered = [False for _ in button_names]

    def draw(self, mouse_pos, coordinates, color_schem):
        cord = [coordinates[0], coordinates[1]]
        for i in range(len(self.button_names)):
            rect = pygame.Rect(cord[0], cord[1], 30, 30)
            self.hovered[i] = rect.collidepoint(mouse_pos[0], mouse_pos[1])
            color = color_schemes[color_schem][4]
            if self.hovered[i]:
                color = color_schemes[color_schem][5]
            pygame.draw.rect(screen, white, rect)
            pygame.draw.rect(screen, color, rect, 1)
            if self.active[i]:
                pygame.draw.rect(screen, color, (cord[0] + 5, cord[1] + 5, 20, 20))
            draw_text(self.button_names[i], color, (cord[0] + 35, cord[1] + 13))
            cord[1] += 40
            if i != 0 and i % 4 == 0:
                cord[1] = coordinates[0]
                cord[0] += 100

    def press(self):
        if True in self.hovered:
            self.active[self.hovered.index(True)] = not self.active[self.hovered.index(True)]


class Button():
    def __init__(self, answer, button_name: str, width: int, img=None):
        self.answer = answer
        self.name = button_name
        self.width = width
        self.img = img
        self.hovered = False

    def draw(self, mouse_pos, coordinates, color_schem, bg_color: int, hover_bg_color: int):
        rect = pygame.Rect(coordinates[0], coordinates[1], self.width, 50)
        self.hovered = rect.collidepoint(mouse_pos[0], mouse_pos[1])
        background_color = color_schemes[color_schem][bg_color]
        if self.hovered:
            background_color = color_schemes[color_schem][hover_bg_color]
        draw_text_in_block(self.name, coordinates, (self.width, 50),
                           color_schemes[color_schem][4], background_color, 'center', dot=False)
        if self.img:
            screen.blit(self.img, (coordinates[0] + 5, coordinates[1] + 5))


class Result_names_request():
    def __init__(self, content):
        self.content = []
        for i in content:
            self.content.append(i)
        self.buttons = [Button(None, '-', 20), Button(None, '-', 20), Button(None, '+', 20), Button(None, '+', 20),
                        Button(None, 'X', 50)]
        self.section_content = select_section_by_id(self.content[2])
        self.hovered = False

    def draw(self, mouse_pos, coordinates, color_schem):
        if self.content[4] in [0, 3]:
            self.buttons[4].draw(mouse_pos, (coordinates[0], coordinates[1] + 8), color_schem, 1, 2)
        pygame.draw.rect(screen, color_schemes[color_schem][3], (coordinates[0] + 50, coordinates[1], 1150, 65))
        text = font.render(cut_to_size(420, self.content[3], len(self.content[3]))[0], True, (255, 255, 255))
        text_rect = text.get_rect(center=(0, coordinates[1] + 32))
        text_rect.left = coordinates[0] + 65
        self.hovered = text_rect.collidepoint(mouse_pos[0], mouse_pos[1])

        outline_color = color_schemes[color_schem][4]
        if self.hovered:
            outline_color = color_schemes[color_schem][5]
        draw_text(self.content[3], outline_color, (coordinates[0] + 65, coordinates[1] + 32), 420)

        outline_color = color_schemes[color_schem][4]
        if self.content[4] == 0:
            draw_text('Не начато', outline_color, (coordinates[0] + 600, coordinates[1] + 32))
        elif self.content[4] == 2:
            draw_text('Жду продолжения', outline_color, (coordinates[0] + 600, coordinates[1] + 32))
        elif self.content[4] == 3:
            draw_text('Не понравилось', outline_color, (coordinates[0] + 600, coordinates[1] + 32))
        elif self.content[4] == 4:
            for i in range(5):
                star = silver_star
                if self.content[8] >= i:
                    star = golden_star
                screen.blit(star, (600 + (40 * i), coordinates[1] + 13))
        elif self.content[4] == 1:
            if self.section_content[4] == 0:
                draw_text('В процессе', outline_color, (coordinates[0] + 600, coordinates[1] + 32))
            else:
                x = coordinates[0] + 525
                for button_number in range(2):
                    self.buttons[button_number].draw(mouse_pos, (x, coordinates[1] + 7), color_schem, 1, 2)
                    self.buttons[button_number + 2].draw(mouse_pos, (x + 100, coordinates[1] + 7), color_schem, 1, 2)
                    x += 300
                text = cut_to_size(70, str(self.content[5]), len(str(self.content[5])))
                draw_text_in_block(text[0], (coordinates[0] + 550, coordinates[1] + 7), (70, 50),
                                   outline_color, text_offset=len(str(self.content[5])), dot=False)
                if text[0] != str(self.content[5]):
                    draw_text('->', outline_color, (coordinates[0] + 615, coordinates[1] + 12), mod='right')
                    self.create_hint(str(self.content[5]), mouse_pos,
                                     pygame.Rect(coordinates[0] + 550, coordinates[1] + 7, 70, 50), color_schem)

                text = cut_to_size(70, str(self.content[6]), len(str(self.content[6])))
                draw_text_in_block(text[0], (coordinates[0] + 850, coordinates[1] + 7), (70, 50),
                                   outline_color, text_offset=len(str(self.content[6])), dot=False)
                if text[0] != str(self.content[6]):
                    draw_text('->', outline_color, (coordinates[0] + 915, coordinates[1] + 12), mod='right')
                    self.create_hint(str(self.content[6]), mouse_pos,
                                     pygame.Rect(coordinates[0] + 850, coordinates[1] + 7, 70, 50), color_schem)
                draw_text(self.section_content[2], outline_color, (coordinates[0] + 650, coordinates[1] + 32), 180)
                draw_text(self.section_content[3], outline_color, (coordinates[0] + 950, coordinates[1] + 32), 180)
        else:
            draw_text('Статус не известен!', outline_color, (coordinates[0] + 600, coordinates[1] + 32))

    def create_hint(self, text, mouse_pos, rect, color_schem):
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            draw_text(text, color_schemes[color_schem][6], (rect.x, rect.y + rect.height + 10))

    @property
    def press(self):
        bloc_and_chapter = [self.content[5], self.content[6]]
        for i in range(len(self.buttons)):
            if self.buttons[i].hovered:
                if i == 4:
                    delete_title(self.content[0])
                    return 'delete'
                else:
                    if i != 4:
                        if i // 2 == 0:
                            if bloc_and_chapter[i % 2] - 1 > 0:
                                bloc_and_chapter[i % 2] = bloc_and_chapter[i % 2] - 1
                                if i % 2 == 0:
                                    bloc_and_chapter[1] = 1
                        elif bloc_and_chapter[i % 2] + 1 < 9223372036854775807:
                            bloc_and_chapter[i % 2] = bloc_and_chapter[i % 2] + 1
                            if i % 2 == 0:
                                bloc_and_chapter[1] = 1
                        break
        if self.content[5] != bloc_and_chapter[0] or self.content[6] != bloc_and_chapter[1]:
            for i in range(2):
                self.content[5 + i] = bloc_and_chapter[i]
            update_title(self.content[0], self.section_content[1], self.content[3], self.content[4], self.content[5],
                         self.content[6], self.content[7], self.content[8])


class Query_result_by_section():
    def __init__(self, content):
        self.content = content
        self.can_it_be_deleted = number_of_titles_related_to_section(content[0]) == 0 and \
                                 not find_users_with_section(self.content[0])
        self.button = Button(None, 'X', 50)

    def draw(self, mouse_pos, coordinates, color_schem):
        if self.can_it_be_deleted:
            self.button.draw(mouse_pos, (coordinates[0], coordinates[1] + 8), color_schem, 1, 2)
        outline_color = color_schemes[color_schem][4]
        pygame.draw.rect(screen, color_schemes[color_schem][3], (coordinates[0] + 50, coordinates[1], 1150, 65))
        draw_text(self.content[1], outline_color, (coordinates[0] + 65, coordinates[1] + 32), 420)
        if bool(self.content[4]):
            draw_text(self.content[2], outline_color, (coordinates[0] + 515, coordinates[1] + 32), 250)
            draw_text(self.content[3], outline_color, (coordinates[0] + 800, coordinates[1] + 32), 250)

    @property
    def press(self):
        if self.button.hovered:
            if delete_section(self.content[0]):
                return 'delete'


class Card():
    def objects(self, coordinates):
        self.error_text = ''
        self.show = False
        self.id = None
        self.coordinates = coordinates
        self.buttons = [Button(None, 'Отменить', 300), Button('accept', 'Подтвердить', 300)]
        self.content_boxes = []

    def create_box(self, mouse_pos, color_schem):
        pygame.draw.rect(screen, color_schemes[color_schem][1], (self.coordinates[0], self.coordinates[1], 1000, 600))
        pygame.draw.rect(screen, color_schemes[color_schem][4], (self.coordinates[0], self.coordinates[1],
                                                                 1000, 600), 1)
        pygame.draw.rect(screen, color_schemes[color_schem][0], (self.coordinates[0] + 10, self.coordinates[1] + 10,
                                                                 980, 580))
        draw_text(self.error_text, color_schemes[color_schem][5],
                  (self.coordinates[0] + 980, self.coordinates[1] + 30), mod='right')

        self.buttons[0].draw(mouse_pos, (self.coordinates[0] + 50, self.coordinates[1] + 570), color_schem, 1, 2)
        self.buttons[1].draw(mouse_pos, (self.coordinates[0] + 650, self.coordinates[1] + 570), color_schem, 1, 2)

    @property
    def find_press_content_box(self):
        active_buttons = []
        pressed_button = -1
        for i in range(len(self.content_boxes)):
            active_buttons.append(self.content_boxes[i].active)
            if self.content_boxes[i].hovered:
                pressed_button = i
        if pressed_button >= 0:
            self.content_boxes[pressed_button].active = True
            if True in active_buttons and active_buttons.index(True) != pressed_button:
                self.content_boxes[active_buttons.index(True)].active = False


class Title_card(Card):
    def __init__(self, coordinates):
        self.objects(coordinates)
        self.content_boxes = [Content_box(), Content_box(), Content_box(width=900),
                              Content_box(mod='number', width=70), Content_box(mod='number', width=70)]
        self.radio_button = Radio_button(['Не начато', 'В процессе', 'Жду продолжения',
                                          'Не понравилось', 'Завершено'], 4)
        self.hovered_on_stars = []

    def set_content(self, user_id, title_name='', type='', status=0, bloc='1', chapter='1', note='', star=0, id=None):
        self.id = id
        n = 0
        for i in [title_name, type, note, str(bloc), str(chapter)]:
            self.content_boxes[n].text = i
            n += 1
        if len(select_section_by_pice_of_name()) != 0:
            self.content_boxes[1].auxiliary_sheet = [i[1] for i in select_section_by_pice_of_name()]
        self.radio_button.active = status
        self.star = star
        self.user_id = user_id
        self.error_text = ''
        for i in self.buttons:
            i.hovered = False

    def draw(self, mouse_pos, color_schem):
        self.create_box(mouse_pos, color_schem)
        outline_color = color_schemes[color_schem][4]

        self.radio_button.draw(mouse_pos, (self.coordinates[0] + 150, self.coordinates[1] + 220), color_schem)
        if self.radio_button.active == 1:
            self.content_boxes[3].draw(mouse_pos, (self.coordinates[0] + 400, self.coordinates[1] + 235), color_schem)
            rect = pygame.Rect(self.coordinates[0] + 400, self.coordinates[1] + 235, self.content_boxes[3].width, 50)
            if len(self.content_boxes[3].text) > 4 and rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                draw_text(self.content_boxes[3].text, color_schemes[color_schem][6],
                          (rect.x, rect.y + rect.height + 10))
            draw_text('Блок', outline_color, (self.coordinates[0] + 475, self.coordinates[1] + 260))
            self.content_boxes[4].draw(mouse_pos, (self.coordinates[0] + 570, self.coordinates[1] + 235), color_schem)
            rect = pygame.Rect(self.coordinates[0] + 570, self.coordinates[1] + 235, self.content_boxes[4].width, 50)
            if len(self.content_boxes[4].text) > 4 and rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                draw_text(self.content_boxes[4].text, color_schemes[color_schem][6],
                          (rect.x, rect.y + rect.height + 10))
            draw_text('Часть', outline_color, (self.coordinates[0] + 645, self.coordinates[1] + 260))
        elif self.radio_button.active == 4:
            x = self.coordinates[0] + 420
            self.hovered_on_stars = [False for _ in range(5)]
            for i in range(5):
                self.hovered_on_stars[i] = screen.blit(silver_star, (x, self.coordinates[1] +
                                                                     360)).collidepoint(mouse_pos[0], mouse_pos[1])
                star = silver_star
                if self.star >= i:
                    star = golden_star
                    if self.hovered_on_stars[i]:
                        star = silver_star
                elif self.hovered_on_stars[i]:
                    star = golden_star
                screen.blit(star, (x, self.coordinates[1] + 360))
                x += 40

        draw_text('Название:', outline_color, (self.coordinates[0] + 320, self.coordinates[1] + 85), mod='right')
        draw_text('Раздел:', outline_color, (self.coordinates[0] + 320, self.coordinates[1] + 155), mod='right')

        self.content_boxes[0].draw(mouse_pos, [self.coordinates[0] + 330, self.coordinates[1] + 60], color_schem)
        self.content_boxes[1].draw(mouse_pos, [self.coordinates[0] + 330, self.coordinates[1] + 130], color_schem)

        draw_text('Заметка о тайтле:', outline_color, (self.coordinates[0] + 50, self.coordinates[1] + 440))
        self.content_boxes[2].draw(mouse_pos, (self.coordinates[0] + 50, self.coordinates[1] + 470), color_schem)
        draw_text(f"{len(self.content_boxes[2].text)}/255", outline_color,
                  (self.coordinates[0] + 920, self.coordinates[1] + 530), mod='right')

    def press(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            for content_box in self.content_boxes:
                content_box.write(event)
        else:
            for content_box in self.content_boxes:
                content_box.press(event)
            for button in self.buttons:
                if button.hovered:
                    for content_box in self.content_boxes:
                        content_box.active = False
                    response = (True,)
                    for i in range(5):
                        if button.answer and i != 2 and self.content_boxes[i].text == '':
                            response = (False, 'Все поля должны быть заполнены!')
                    if not exceeding_number_of_records("titles"):
                        response = (False, 'Извините, добавить новый тайтл невозможно, лимит превышен!')
                    if response[0] and button.answer:
                        if not self.id:
                            response = append_title(self.user_id, self.content_boxes[1].text,
                                                    self.content_boxes[0].text, self.radio_button.active,
                                                    int(self.content_boxes[3].text), int(self.content_boxes[4].text),
                                                    self.content_boxes[2].text, self.star)
                        else:
                            response = update_title(self.id, self.content_boxes[1].text,
                                                    self.content_boxes[0].text, self.radio_button.active,
                                                    int(self.content_boxes[3].text), int(self.content_boxes[4].text),
                                                    self.content_boxes[2].text, self.star)
                    if response[0]:
                        self.show = False
                    else:
                        self.error_text = response[1]
                    return True
            self.radio_button.press
            if True in self.hovered_on_stars:
                self.star = self.hovered_on_stars.index(True)
            self.find_press_content_box


class Section_card(Card):
    def __init__(self, coordinates):
        self.objects(coordinates)
        self.content_boxes = [Content_box(), Content_box(), Content_box()]
        self.buttons = [Button(None, 'Отменить', 300), Button('accept', 'Подтвердить', 300)]
        self.cheak_button = Cheak_button(['Отображать?'], [])

    def set_content(self, section_name='', bloc_name='', chapter_name='', display=True, user_id=None):
        self.content_boxes[0].text = section_name
        self.content_boxes[1].text = bloc_name
        self.content_boxes[2].text = chapter_name
        self.cheak_button.active[0] = display
        for i in self.buttons:
            i.hovered = False

    def draw(self, mouse_pos, color_schem):
        self.create_box(mouse_pos, color_schem)
        outline_color = color_schemes[color_schem][4]

        draw_text('Название:', outline_color, (self.coordinates[0] + 200, self.coordinates[1] + 165))
        self.content_boxes[0].draw(mouse_pos, [self.coordinates[0] + 330, self.coordinates[1] + 140], color_schem)

        self.cheak_button.draw(mouse_pos, (self.coordinates[0] + 150, self.coordinates[1] + 250), color_schem)
        if self.cheak_button.active[0]:
            draw_text('Название Блока:', outline_color,
                      (self.coordinates[0] + 320, self.coordinates[1] + 355), mod='right')
            draw_text('Название Части:', outline_color,
                      (self.coordinates[0] + 320, self.coordinates[1] + 415), mod='right')
            self.content_boxes[1].draw(mouse_pos, [self.coordinates[0] + 330, self.coordinates[1] + 330], color_schem)
            self.content_boxes[2].draw(mouse_pos, [self.coordinates[0] + 330, self.coordinates[1] + 390], color_schem)

    def press(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            for content_box in self.content_boxes:
                content_box.write(event)
        else:
            for content_box in self.content_boxes:
                content_box.press(event)
            self.cheak_button.press()
            for button in self.buttons:
                if button.hovered:
                    for content_box in self.content_boxes:
                        content_box.active = False
                    response = (True,)
                    if button.answer:
                        if self.content_boxes[0].text == '' or \
                                (self.cheak_button.active[0] and self.content_boxes[1].text == '' and
                                 self.content_boxes[2].text == ''):
                            response = (False, 'Поле названия должно быть не пусто!')
                        elif exceeding_number_of_records('sections'):
                            response = add_section(self.content_boxes[0].text, self.content_boxes[1].text,
                                                   self.content_boxes[2].text, int(self.cheak_button.active[0]))
                        else:
                            response = (False, 'Извините, создать новый раздел невозможно, лимит превышен!')
                    if response[0]:
                        self.show = False
                        return True
                    else:
                        self.error_text = response[1]
            self.find_press_content_box


class Settings_card(Card):
    def __init__(self, coordinates, content):
        self.objects(coordinates)
        self.id = content[0]
        self.content = content
        self.color_schem = content[4]
        self.content_boxes = [Content_box(select_section_by_id(self.content[3])[1])]
        self.buttons = [Button(None, 'Отменить', 300), Button('accept', 'Подтвердить', 300)]
        self.radio_buttons = [Radio_button(color_names, self.color_schem - 1),
                              Radio_button(['Алфавиту', 'Дате добавления'], self.content[-1])]
        self.create_auxiliary_sheet

    @property
    def create_auxiliary_sheet(self):
        if len(select_section_by_pice_of_name()) != 0:
            self.content_boxes[0].auxiliary_sheet = [i[1] for i in select_section_by_pice_of_name()]

    def draw(self, mouse_pos):
        self.create_box(mouse_pos, self.color_schem)
        outline_color = color_schemes[self.color_schem][4]

        draw_text('Цветовая гамма:', outline_color, (self.coordinates[0] + 80, self.coordinates[1] + 130))
        self.radio_buttons[0].draw(mouse_pos, (self.coordinates[0] + 120, self.coordinates[1] + 180), self.color_schem)
        draw_text('Сортировать по:', outline_color, (self.coordinates[0] + 80, self.coordinates[1] + 400))
        self.radio_buttons[1].draw(mouse_pos, (self.coordinates[0] + 120, self.coordinates[1] + 450), self.color_schem)
        draw_text('Приоритетный раздел:', outline_color,
                  (self.coordinates[0] + 340, self.coordinates[1] + 85), mod='right')
        self.content_boxes[0].draw(mouse_pos, (self.coordinates[0] + 350, self.coordinates[1] + 60), self.color_schem)

    def press(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            self.content_boxes[0].write(event)
        else:
            for content_box in self.content_boxes:
                content_box.press(event)
            for i in self.radio_buttons:
                i.press
            if self.radio_buttons[0].active != self.color_schem - 1:
                self.color_schem = self.radio_buttons[0].active + 1
            for button in self.buttons:
                if button.hovered:
                    for content_box in self.content_boxes:
                        content_box.active = False
                    response = (True,)
                    if button.answer:
                        if self.content_boxes[0].text == '':
                            response = (False, 'Поле названия раздела должно быть не пусто!')
                        else:
                            response = update_user(self.content[0], self.content_boxes[0].text,
                                                   self.color_schem, self.radio_buttons[1].active)
                    if response[0]:
                        self.show = False
                        if button.answer:
                            return self.color_schem
                        self.color_schem = self.content[4]
                        self.radio_buttons[0].active = self.content[4] - 1
                        return True
                    else:
                        self.error_text = response[1]
            self.find_press_content_box


class Hints(Card):
    def __init__(self):
        self.show = False
        self.hint_number = 0
        self.hint_names = ['Окно тайтлов', 'Создание тайтлов', 'Настройки', 'Окно разделов']
        self.hints = [pygame.image.load('./images/hints/hint_1.jpg'), pygame.image.load('./images/hints/hint_2.jpg'),
                      pygame.image.load('./images/hints/hint_3.jpg'), pygame.image.load('./images/hints/hint_4.jpg')]

    def draw(self, color_schem):
        screen.fill(color_schemes[color_schem][0])
        screen.blit(self.hints[self.hint_number], [100, 50])
        pygame.draw.rect(screen, color_schemes[color_schem][4], (100, 50, 1000, 600), 1)
        draw_text("Нажмите ESC чтобы закрыть подсказки", color_schemes[color_schem][4], (1180, 20), mod='right')
        draw_text("Используйте стрелочки для смены подсказки", color_schemes[color_schem][4], (10, 20))
        draw_text(self.hint_names[self.hint_number], color_schemes[color_schem][4], (600, 670), mod='center')
        draw_text(f"{self.hint_number + 1}/{len(self.hints)}", color_schemes[color_schem][4], (600, 700), mod='center')

    def press(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show = False
                self.hint_number = 0
            elif event.key == pygame.K_LEFT and self.hint_number > 0:
                self.hint_number -= 1
            elif event.key == pygame.K_RIGHT and self.hint_number < len(self.hints) - 1:
                self.hint_number += 1


class Select_box():
    def objects(self, coordinates):
        self.coordinates = coordinates
        self.content_box = []
        self.result_boxes = []
        self.button = Button(None, 'Применить', 250)
        self.step = 0
        self.card = None

    def create_box(self, mouse_pos, color_schem):
        for i in range(len(self.result_boxes)):
            if i >= self.step:
                self.result_boxes[i].draw(mouse_pos, [0, self.coordinates[1] + 129 + 80 * (i - self.step)], color_schem)
            if i - self.step > 7:
                break
        if len(self.result_boxes) - self.step > 6:
            screen.blit(pygame.transform.rotate(arrow, 180), (1160, 680))
        if self.step:
            screen.blit(arrow, (1160, 200))
        pygame.draw.rect(screen, color_schemes[color_schem][2], (self.coordinates[0], self.coordinates[1], 1200, 129))
        self.hover_over_content = self.coordinates[1] + 129 < mouse_pos[1]
        self.button.draw(mouse_pos, (self.coordinates[0] + 10 + (310 * 3), self.coordinates[1] + 49), color_schem, 1, 3)


class Titles_select_box(Select_box):
    def __init__(self, coordinates, user_id):
        self.objects(coordinates)
        self.content_boxes = [Content_box(), Content_box(), Content_box('Все')]
        self.content_boxes[2].auxiliary_sheet = ['Все', 'Не начато', 'Начато', 'Жду продолжения',
                                                 'Не понравилось', 'Завершено']
        self.card = Title_card((100, 60))
        self.take_results(user_id)

    def take_results(self, user_id):
        results = []
        content = select_user_by_id(user_id)
        if not select_section_by_title(self.content_boxes[0].text):
            self.content_boxes[0].text = select_section_by_id(content[3])[1]
        if content:
            results = select_titles(user_id, self.content_boxes[0].text, "", None, 1)
        self.content_boxes[1].auxiliary_sheet = [x[3] for x in results[1]]
        self.content_boxes[0].auxiliary_sheet = [x[0] for x in get_section_names()]
        results = select_titles(user_id, self.content_boxes[0].text, self.content_boxes[1].text,
                                self.content_boxes[2].text, content[-1])
        self.result_boxes = []
        for i in results[1]:
            self.result_boxes.append(Result_names_request(i))

    def draw(self, mouse_pos, color_schem):
        self.create_box(mouse_pos, color_schem)
        texts = ['Раздел', 'Фрагмент названия', 'Статус']
        y = self.coordinates[1] + 20
        for i in range(3):
            draw_text(texts[i], color_schemes[color_schem][4], (self.coordinates[0] + 10 + (310 * i), y))
            self.content_boxes[i].draw(mouse_pos, (self.coordinates[0] + 10 + (310 * i), y + 29), color_schem)

    def press(self, event, user_id):
        if self.card.show:
            self.card.press(event)
            if not self.card.show:
                self.take_results(user_id)
        else:
            if event.type != pygame.MOUSEBUTTONDOWN:
                for content_box in self.content_boxes:
                    content_box.write(event)
            else:
                for content_box in self.content_boxes:
                    content_box.press(event)
                if event.button == 1:
                    for i in self.result_boxes:
                        response = i.press
                        if response == 'delete':
                            self.take_results(user_id)
                        elif i.hovered:
                            self.card.set_content(user_id, i.content[3], i.section_content[1], i.content[4],
                                                  i.content[5],
                                                  i.content[6], i.content[7], i.content[8], i.content[0])
                            self.card.show = True
                            return True
                    if self.button.hovered:
                        for content_box in self.content_boxes:
                            content_box.active = False
                        self.take_results(user_id)
                    else:
                        active_buttons = []
                        pressed_button = -1
                        for i in range(len(self.content_boxes)):
                            active_buttons.append(self.content_boxes[i].active)
                            if self.content_boxes[i].hovered:
                                pressed_button = i
                        if pressed_button >= 0:
                            self.content_boxes[pressed_button].active = True
                            if True in active_buttons and active_buttons.index(True) != pressed_button:
                                self.content_boxes[active_buttons.index(True)].active = False
                elif self.hover_over_content and event.button in [5, 4]:
                    if event.button == 5 and len(self.result_boxes) - self.step > 6:
                        self.step += 1
                    if event.button == 4 and self.step > 0:
                        self.step -= 1


class Section_select_box(Select_box):
    def __init__(self, coordinates):
        self.objects(coordinates)
        self.content_boxes = [Content_box()]
        self.card = Section_card((100, 60))
        self.take_results(0)

    def take_results(self, user_id=None):
        self.content_boxes[0].auxiliary_sheet = [i[0] for i in get_section_names()]
        results = select_section_by_pice_of_name(self.content_boxes[0].text)
        self.result_boxes = []
        for i in results:
            self.result_boxes.append(Query_result_by_section(i))

    def draw(self, mouse_pos, color_schem):
        self.create_box(mouse_pos, color_schem)
        draw_text('Фрагмент названия', color_schemes[color_schem][4],
                  (self.coordinates[0] + 10, self.coordinates[1] + 20))
        self.content_boxes[0].draw(mouse_pos, (self.coordinates[0] + 10, self.coordinates[1] + 49), color_schem)

    def press(self, event, user_id):
        if self.card.show:
            self.card.press(event)
            if not self.card.show:
                self.take_results()
        else:
            if event.type != pygame.MOUSEBUTTONDOWN:
                self.content_boxes[0].write(event)
            else:
                self.content_boxes[0].press(event)
                if event.button == 1:
                    for result_box in self.result_boxes:
                        response = result_box.press
                        if response == 'delete':
                            self.take_results()
                    if self.button.hovered:
                        self.content_boxes[0].active = False
                        self.take_results()
                    elif self.content_boxes[0].hovered:
                        self.content_boxes[0].active = True
                elif self.hover_over_content and event.button in [5, 4]:
                    if event.button == 5 and len(self.result_boxes) - self.step > 6:
                        self.step += 1
                    if event.button == 4 and self.step > 0:
                        self.step -= 1


class Menu():
    def __init__(self):
        self.exit

    @property
    def exit(self):
        self.user_id = None
        self.content = []
        self.content_boxes = [Content_box(), Content_box(mod='locked')]
        self.buttons = [Button(append_user, 'Регистрация', 300), Button(select_user, 'Войти', 300),
                        Button(delete_user, 'Удалить пользователя', 300)]
        self.error_text = ''

    def login(self, content):
        self.user_id = content[0]
        self.content = [x for x in content]
        self.buttons = [Button('exit', 'Выйти', 100), Button('setting', '', 50, gear),
                        Button('sections', 'К разделам', 200), Button('hints', '', 50, question)]
        self.select_box = Titles_select_box([0, 69], content[0])
        self.setting_card = Settings_card((100, 60), content)
        self.hints_card = Hints()

    def draw(self, mouse_pos):
        if not self.user_id:
            self.register(mouse_pos)
        else:
            screen.fill(color_schemes[self.content[4]][0])
            self.select_box.draw(mouse_pos, self.content[4])
            outline_color = color_schemes[self.content[4]][4]
            pygame.draw.rect(screen, color_schemes[self.content[4]][1], (0, 0, 1200, 70))
            draw_text(self.content[1], outline_color, (1070, 30), mod='right')
            self.buttons[0].draw(mouse_pos, (1080, 10), self.content[4], 2, 3)
            self.buttons[3].draw(mouse_pos, (10, 10), self.content[4], 2, 3)
            self.buttons[1].draw(mouse_pos, (70, 10), self.content[4], 2, 3)
            self.buttons[2].draw(mouse_pos, (130, 10), self.content[4], 2, 3)

            circle = pygame.draw.circle(screen, white, [1100, 650], 40)
            self.plus_circle_hovered = circle.collidepoint(mouse_pos[0], mouse_pos[1])
            color = color_schemes[self.content[4]][1]
            if self.plus_circle_hovered:
                color = color_schemes[self.content[4]][2]
            pygame.draw.circle(screen, color, [1100, 650], 40)
            draw_text('+', outline_color, [1100, 650], mod='center')
            if self.select_box.card.show:
                self.select_box.card.draw(mouse_pos, self.content[4])
            if self.setting_card.show:
                self.setting_card.draw(mouse_pos)
            if self.hints_card.show:
                self.hints_card.draw(self.content[4])

    def register(self, mouse_pos):
        screen.fill((235, 244, 233))

        self.content_boxes[0].draw(mouse_pos, (450, 250), 0)
        self.content_boxes[1].draw(mouse_pos, (450, 325), 0)
        draw_text('Логин:', color_schemes[0][4], (440, 200 + 75), mod='right')
        draw_text('Пароль:', color_schemes[0][4], (440, 275 + 75), mod='right')
        self.buttons[0].draw(mouse_pos, (300 - 15, 450), 0, 1, 2)
        self.buttons[1].draw(mouse_pos, (600 + 15, 450), 0, 1, 2)
        self.buttons[2].draw(mouse_pos, (10, 10), 0, 1, 2)
        draw_text('Версия: 1.0', color_schemes[0][2], (10, 660))
        draw_text('Автор: Yunabi', color_schemes[0][2], (10, 690))
        draw_text(self.error_text, color_schemes[0][-1], [1190, 10], mod='right')

    def press(self, event):
        if not self.user_id:
            if event.type != pygame.MOUSEBUTTONDOWN:
                for content_box in self.content_boxes:
                    content_box.write(event)
            elif event.button == 1:
                for button in self.buttons:
                    response = (False,)
                    if button.hovered:
                        if self.content_boxes[0].text == '' or self.content_boxes[1].text == '':
                            response = (False, 'Все поля должны быть заполнены!')
                        else:
                            response = button.answer(self.content_boxes[0].text, self.content_boxes[1].text)
                    if response[0]:
                        self.login(select_user(self.content_boxes[0].text, self.content_boxes[1].text)[1])
                        self.error_text = ''
                        return True
                    elif len(response) != 1:
                        self.error_text = response[1]
                        if button.answer == delete_user:
                            for content_box in self.content_boxes:
                                content_box.text = ''
                active_buttons = []
                pressed_button = -1
                for i in range(len(self.content_boxes)):
                    active_buttons.append(self.content_boxes[i].active)
                    if self.content_boxes[i].hovered:
                        pressed_button = i
                if pressed_button >= 0:
                    self.content_boxes[pressed_button].active = True
                    if True in active_buttons and active_buttons.index(True) != pressed_button:
                        self.content_boxes[active_buttons.index(True)].active = False
        else:
            if self.hints_card.show:
                self.hints_card.press(event)
            elif self.setting_card.show:
                response = self.setting_card.press(event)
                if type(response) == int:
                    self.content[4] = response
                    self.content[3] = select_section_by_title(self.setting_card.content_boxes[0].text)[0]
                    self.select_box.take_results(user_id=self.user_id)
                elif response:
                    self.setting_card.content_boxes[0].text = select_section_by_id(self.content[3])[1]
                    self.setting_card.radio_buttons[0].active = self.content[4] - 1
                    self.setting_card.radio_buttons[1].active = self.content[5]
                    self.setting_card.color_schem = self.content[4]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.plus_circle_hovered:
                self.select_box.card.set_content(user_id=self.user_id)
                for content_box in self.select_box.content_boxes:
                    content_box.active = False
                self.select_box.card.show = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.hovered:
                        for content_box in self.select_box.content_boxes:
                            content_box.active = False
                        if button.answer == 'exit':
                            self.exit
                        elif button.answer == 'setting':
                            self.setting_card.create_auxiliary_sheet
                            self.setting_card.show = True
                        elif button.answer == 'sections':
                            self.buttons[2].answer = 'titles'
                            self.buttons[2].name = 'К тайтлам'
                            self.select_box = Section_select_box([0, 69])
                        elif button.answer == 'titles':
                            self.buttons[2].answer = 'sections'
                            self.buttons[2].name = 'К разделам'
                            self.select_box = Titles_select_box([0, 69], self.user_id)
                        elif button.answer == 'hints':
                            self.hints_card.show = True
            if not self.setting_card.show:
                self.select_box.press(event, self.user_id)
