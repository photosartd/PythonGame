def draw_text(text, font, color, frame, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    frame.blit(textobj, textrect)  