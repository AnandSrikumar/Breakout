import pygame

def set_circle_background(background_image: str,
                          radius: float|int):
    img = pygame.image.load(background_image).convert_alpha()
    img = pygame.transform.scale(img, (radius * 2, radius * 2))
    return img

def set_rect_background(img: str, width: int, height: int):
    background_image = pygame.image.load(img)
    background_image = pygame.transform.scale(
        background_image, (width, height)
    )
    return background_image

def draw_text(text: str, center: tuple, screen: pygame.Surface):
    font = pygame.font.Font(None, 24)  # Use default font, size 50
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(topleft=center)
    screen.blit(text_surface, text_rect)