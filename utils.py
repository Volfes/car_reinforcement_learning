import pygame

#resize images
def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


# new_rect allows to stay image rectangle stay on center after rotation 
# of image
def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(
        topleft = top_left).center)
    screen.blit(rotated_image, new_rect.topleft)