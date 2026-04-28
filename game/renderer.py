import pygame
import random
import math
from game.config import *
from game.utils import get_shape_color


class VolumeSlider:
    def __init__(self, x, y, w, h, initial_val=0.5):
        self.rect = pygame.Rect(x, y, w, h)
        self.handle_rect = pygame.Rect(x + (w * initial_val) - 5, y - 5, 10, h + 10)
        self.volume = initial_val
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_x = max(self.rect.left, min(event.pos[0], self.rect.right))
                self.handle_rect.centerx = new_x
                self.volume = (new_x - self.rect.x) / self.rect.width
                pygame.mixer.music.set_volume(self.volume)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_sm = pygame.font.SysFont("Consolas", 18, bold=True)
        self.font_md = pygame.font.SysFont("Consolas", 25, bold=True)
        self.font_lg = pygame.font.SysFont("Consolas", 50, bold=True)

        random.seed(42)
        self.stars = [
            (
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.randint(1, 3),
            )
            for _ in range(100)
        ]

    def draw_block(self, x, y, color, is_wall=False, alpha=255):
        rect_size = TILE_SIZE - 2
        surf = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)
        pygame.draw.rect(
            surf,
            (*color, alpha),
            (0, 0, rect_size, rect_size),
            border_radius=int(rect_size * ROUNDNESS),
        )

        shine = (
            (150, 150, 150, int(alpha * 0.4))
            if is_wall
            else (255, 255, 255, int(alpha * 0.85))
        )
        pygame.draw.rect(
            surf,
            shine,
            (4, 3, rect_size - 8, rect_size // 3),
            border_radius=int(rect_size * 0.2),
        )
        pygame.draw.rect(
            surf,
            (0, 0, 0, int(alpha * 0.5)),
            (0, 0, rect_size, rect_size),
            1,
            border_radius=int(rect_size * ROUNDNESS),
        )
        self.screen.blit(surf, (x, y))

    def draw_background(self):
        self.screen.fill((10, 11, 30))
        for x, y, size in self.stars:
            pygame.draw.circle(self.screen, (200, 200, 200, 50), (x, y), size / 2)

    def draw_menu(self, player_name, frames):
        cx = SCREEN_WIDTH // 2
        t1 = self.font_lg.render("TetrisPy", True, (255, 203, 0))
        self.screen.blit(t1, (cx - t1.get_width() // 2, 80))

        lbl = self.font_sm.render("ENTER YOUR NAME:", True, (130, 130, 130))
        self.screen.blit(lbl, (cx - 150, 210))

        input_rect = pygame.Rect(cx - 150, 240, 300, 50)
        pygame.draw.rect(self.screen, (24, 24, 24), input_rect, border_radius=6)
        pygame.draw.rect(self.screen, (255, 203, 0), input_rect, 2, border_radius=6)

        name_surf = self.font_md.render(player_name, True, (245, 245, 245))
        self.screen.blit(name_surf, (input_rect.x + 15, input_rect.y + 12))

        if ((frames // 30) % 2) == 0:
            cursor_x = input_rect.x + 18 + name_surf.get_width()
            pygame.draw.rect(
                self.screen, (255, 203, 0), (cursor_x, input_rect.y + 12, 12, 25)
            )

        controls = [
            "CONTROLS:",
            "- A / D : Move Left/Right",
            "- Q / E : Rotate Figure",
            "- S / DOWN : Soft Drop",
            "- SPACE / Z : Hard Drop",
            "- C : Hold Figure",
            "- ESC : Exit Game",
        ]
        for i, text in enumerate(controls):
            color = (130, 130, 130) if i == 0 else (200, 200, 200)
            txt_surf = self.font_sm.render(text, True, color)
            self.screen.blit(txt_surf, (cx - 150, 350 + i * 28))

        if player_name:
            alpha = int((math.sin(frames * 0.07) + 1) / 2 * 255)
            msg = self.font_sm.render("PRESS [ENTER] TO START", True, (0, 228, 48))
            msg_surf = pygame.Surface(msg.get_size(), pygame.SRCALPHA)
            msg_surf.blit(msg, (0, 0))
            msg_surf.set_alpha(alpha)
            self.screen.blit(msg_surf, (cx - msg.get_width() // 2, 650))

    def draw_board(self, board, current_piece, ghost_y_offset=0):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                px, py = GRID_X + (j * TILE_SIZE), GRID_Y + (i * TILE_SIZE)
                cell = board.grid[i][j]
                if cell == "*":
                    self.draw_block(px, py, (45, 45, 45), is_wall=True)
                elif cell != " ":
                    self.draw_block(px, py, get_shape_color(int(cell)))
                else:
                    pygame.draw.rect(
                        self.screen, (18, 18, 18), (px, py, TILE_SIZE, TILE_SIZE), 1
                    )

        if current_piece:
            for r, c in current_piece.cells:
                self.draw_block(
                    GRID_X + c * TILE_SIZE,
                    GRID_Y + (r + ghost_y_offset) * TILE_SIZE,
                    get_shape_color(current_piece.type),
                    alpha=60,
                )
            for r, c in current_piece.cells:
                self.draw_block(
                    GRID_X + c * TILE_SIZE,
                    GRID_Y + r * TILE_SIZE,
                    get_shape_color(current_piece.type),
                )

    def draw_ui(self, score, next_fig, hold_fig, global_champ, personal_best):
        uiX = GRID_X + (MAP_WIDTH * TILE_SIZE) + 40
        self.screen.blit(self.font_sm.render("SCORE", True, (130, 130, 130)), (uiX, 50))
        self.screen.blit(
            self.font_md.render(str(score), True, (255, 203, 0)), (uiX, 75)
        )
        self._draw_preview_box(uiX, 180, "NEXT", next_fig)
        self._draw_preview_box(uiX, 350, "HOLD [C]", hold_fig)

        self.screen.blit(
            self.font_sm.render("PERSONAL BEST", True, (130, 130, 130)),
            (uiX, 120),
        )
        self.screen.blit(
            self.font_sm.render(str(personal_best), True, (0, 228, 48)),
            (uiX, 145),
        )

        self.screen.blit(
            self.font_sm.render("CHAMPION", True, (130, 130, 130)),
            (uiX, 500),
        )
        self.screen.blit(
            self.font_sm.render(global_champ["name"], True, (255, 203, 0)),
            (uiX, 525),
        )
        self.screen.blit(
            self.font_sm.render(str(global_champ["score"]), True, (255, 203, 0)),
            (uiX, 550),
        )

    def _draw_preview_box(self, x, y, label, fig):
        self.screen.blit(self.font_sm.render(label, True, (130, 130, 130)), (x, y))
        box_rect = pygame.Rect(x, y + 25, 120, 100)
        pygame.draw.rect(self.screen, (20, 20, 25), box_rect, border_radius=8)
        if fig:
            coords = ALL_SHAPES[fig.type]
            min_r, max_r = min(c[0] for c in coords), max(c[0] for c in coords)
            min_c, max_c = min(c[1] for c in coords), max(c[1] for c in coords)
            fw, fh = (max_c - min_c + 1) * TILE_SIZE, (max_r - min_r + 1) * TILE_SIZE
            offX, offY = x + (120 - fw) // 2, y + 25 + (100 - fh) // 2
            for r, c in coords:
                self.draw_block(
                    offX + (c - min_c) * TILE_SIZE,
                    offY + (r - min_r) * TILE_SIZE,
                    get_shape_color(fig.type),
                )

    def draw_game_over(self, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        t_go = self.font_lg.render("GAME OVER", True, (230, 41, 55))
        s_txt = self.font_md.render(f"SCORE: {score}", True, (255, 203, 0))
        self.screen.blit(t_go, (cx - t_go.get_width() // 2, cy - 100))
        self.screen.blit(s_txt, (cx - s_txt.get_width() // 2, cy - 20))
        opts = [
            ("PRESS [R] TO RESTART", (255, 255, 255)),
            ("PRESS [M] FOR MENU", (255, 203, 0)),
            ("PRESS [ESC] FOR EXIT", (255, 151, 0)),
        ]
        for i, (txt, col) in enumerate(opts):
            surf = self.font_sm.render(txt, True, col)
            self.screen.blit(surf, (cx - surf.get_width() // 2, cy + 60 + i * 40))

    def draw_volume_control(self, slider):
        mid_y = slider.rect.y + slider.rect.height // 2
        icon_x = slider.rect.x - 32
        icon_col = (130, 130, 130)

        spk_w, spk_h = 6, 6
        pygame.draw.rect(self.screen, icon_col, (icon_x, mid_y - spk_h // 2, spk_w, spk_h))

        bell_w, bell_h = 7, 12
        points = [
            (icon_x + spk_w, mid_y - spk_h // 2),
            (icon_x + spk_w + bell_w, mid_y - bell_h // 2),
            (icon_x + spk_w + bell_w, mid_y + bell_h // 2),
            (icon_x + spk_w, mid_y + spk_h // 2)
        ]
        pygame.draw.polygon(self.screen, icon_col, points)

        if slider.volume == 0:
            center_icon_x = icon_x + (spk_w + bell_w) // 2
            cs = 5
            pygame.draw.line(self.screen, (230, 41, 55), (center_icon_x - cs, mid_y - cs),
                             (center_icon_x + cs, mid_y + cs), 2)
            pygame.draw.line(self.screen, (230, 41, 55), (center_icon_x - cs, mid_y + cs),
                             (center_icon_x + cs, mid_y - cs), 2)

        pygame.draw.rect(self.screen, (40, 40, 45), slider.rect, border_radius=4)
        fill_w = max(0, (slider.handle_rect.centerx - slider.rect.x) - 2)
        if fill_w > 0:
            active_rect = pygame.Rect(slider.rect.x, slider.rect.y, fill_w, slider.rect.height)
            pygame.draw.rect(self.screen, (255, 203, 0), active_rect, border_radius=4)

        pygame.draw.circle(self.screen, (245, 245, 245),
                           (slider.handle_rect.centerx, mid_y), 8)
