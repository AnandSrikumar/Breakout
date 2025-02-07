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