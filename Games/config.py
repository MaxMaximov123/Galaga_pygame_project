K = 0.75  # коэффициент размера
HEIGHT = round(1080 * K)  # ВыСОТА ЭКРАНА
WIDTH = round(1920 * K)  # ШИРИНА ЭКРАНА


FPS = 240  # fps ����

GAMES_NAMES = ['GALAGA', 'Танки']
SIZE_BOARD_FOR_TANKS = 16, 9
TILE_SIZE = HEIGHT // SIZE_BOARD_FOR_TANKS[1]
INDENT_SIZE = TILE_SIZE