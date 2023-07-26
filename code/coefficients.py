import pygame

pygame.init()
pygame.display.set_caption('What am I watching?')
pygame.display.set_icon(pygame.image.load('./images/icon.png'))

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 720), pygame.SCALED)
font = pygame.font.SysFont('Comic Sans MS', 25)

arrow = pygame.image.load('./images/arrow.png')
arrow = pygame.transform.rotozoom(arrow, 0, 1.3)

golden_star = pygame.image.load('./images/golden_star.png')
silver_star = pygame.image.load('./images/silver_star.png')
gear = pygame.image.load('./images/gear.png')
question = pygame.image.load('./images/question.png')
white = (255, 255, 255)

color_names = ['Красный', 'Оранжевый', 'Жёлтый', 'Зелёный', 'Синий', 'Фиолетовый', 'Серый',
               'Оранжевый + Зелёный', 'Розовый']
color_schemes = {
    0: ((226, 243, 141), (207, 144, 209), (173, 182, 125), white, (104, 31, 106), (121, 84, 123), (140, 158, 46)),
    # red
    1: ((255, 245, 243), (173, 138, 140), (226, 189, 190), (245, 214, 216), (84, 14, 18), (184, 10, 20), (34, 0, 0)),
    # orange
    2: ((237, 215, 206), (181, 140, 125), (217, 177, 154), (235, 201, 188), (79, 40, 27), (126, 61, 36), (51, 20, 19)),
    # yellow
    3: ((253, 253, 241), (178, 178, 141), (216, 216, 178), (228, 228, 197), (98, 98, 0), (155, 155, 5), (34, 34, 0)),
    # green
    4: ((239, 250, 222), (154, 180, 132), (190, 214, 170), (206, 225, 190), (44, 104, 0), (52, 151, 0), (0, 49, 0)),
    # blue
    5: ((238, 248, 255), (161, 161, 198), (201, 201, 241), (222, 222, 255), (22, 22, 129), (48, 48, 248), (0, 0, 70)),
    # purple
    6: ((228, 218, 235), (148, 134, 158), (182, 161, 204), (199, 174, 216), (61, 40, 89), (87, 42, 115), (43, 40, 54)),
    # grey
    7: ((217, 217, 217), (191, 130, 131), (165, 165, 165), (184, 184, 184), (107, 54, 54), (128, 41, 44), (41, 20, 20)),
    # Orange + Green
    8: ((235, 250, 245), (255, 158, 109), (130, 228, 196), (242, 219, 208), (1, 71, 66), (166, 79, 36), (0, 20, 19)),
    # pink
    9: ((255, 251, 255), (238, 190, 241), (237, 240, 223), (255, 255, 204), (117, 48, 122), (150, 165, 65), (10, 4, 10))
}


# Функция обрезает текст до заданного размера
def cut_to_size(width, text, offset):
    step = 0
    copy_text = text
    while font.render(copy_text, True, white).get_width() > width - 10:
        if step - offset > 0:
            copy_text = text[step - offset:len(text) - offset]
        else:
            copy_text = text[0: len(text) - step]
        step += 1
    difference = offset - step
    if offset - step < 0:
        offset = 0
    elif step != 0:
        offset = (step - offset - 1) * -1
    return copy_text, offset, difference


def draw_text(text, color, coordinates, width=0, mod='left', dot=True):
    if width and dot:
        new_text = cut_to_size(width - 20, text, len(text) - 1)[0]
        if new_text != text:
            text = new_text + '...'
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(coordinates[0] + width / 2, coordinates[1]))
    if mod == 'left':
        text_rect.left = coordinates[0] + 5
    elif mod == 'right':
        text_rect.right = coordinates[0]
    screen.blit(text, text_rect)


def draw_text_in_block(text, coordinates, rect_size, outline_color, background_color=white, mod='left', animation=False,
                       text_offset=0, dot=True):
    pygame.draw.rect(screen, background_color, (coordinates[0], coordinates[1], rect_size[0], rect_size[1]))
    pygame.draw.rect(screen, outline_color, (coordinates[0], coordinates[1], rect_size[0], rect_size[1]), 1)
    if animation:
        left = font.render(text[:len(text) - text_offset], True, white).get_width()
        pygame.draw.rect(screen, outline_color, (coordinates[0] + left + 5, coordinates[1] + 10, 2, 30))
    draw_text(text, outline_color, (coordinates[0], coordinates[1] + rect_size[1] / 2), rect_size[0], mod, dot)
