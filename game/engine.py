import pygame
import time
import random
from pathlib import Path
from game.board import Board
from game.piece import Piece
from game.renderer import Renderer
from game.score_manager import ScoreManager
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT


class TetrisPy:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TetrisPy")

        self.board = Board()
        self.renderer = Renderer(self.screen)

        self.gameState = 0
        self.running = True
        self.gameOver = False
        self.player_name = ""
        self.score = 0

        self.bag = []
        self.current_piece = None
        self.next_piece = self.pick_new_piece()
        self.hold_piece = None
        self.can_hold = True

        self.score_manager = ScoreManager()
        self.global_champ = {"name": "None", "score": 0}
        self.personal_best = 0

        self.fall_delay = 0.7
        self.last_fall = time.perf_counter()
        self.load_sounds()

    def load_sounds(self):
        pygame.mixer.init()
        path = Path(__file__).resolve().parent.parent / "assets" / "sounds"
        self.sounds = {}
        names = [
            "4Lines",
            "Drop",
            "GameOver",
            "HardDrop",
            "Hold",
            "Move",
            "OneLine",
            "Rotate",
            "SoftDrop",
        ]
        for n in names:
            try:
                self.sounds[n] = pygame.mixer.Sound(str(path / f"{n}.wav"))
            except:
                self.sounds[n] = None
        try:
            pygame.mixer.music.load(str(path / "Game.wav"))
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1)
        except:
            pass

    def play_snd(self, name):
        if self.sounds.get(name):
            self.sounds[name].play()

    def pick_new_piece(self) -> Piece:
        """Selects the next figure"""
        if not self.bag:
            self.bag = list(range(7))
            random.shuffle(self.bag)
        return Piece(self.bag.pop())

    def get_ghost_offset(self) -> int:
        """Calculate the maximum vertical drop distance for the current piece."""
        if not self.current_piece:
            return 0
        offset = 0
        while not self.board.check_collision(
            [[c[0] + offset + 1, c[1]] for c in self.current_piece.cells]
        ):
            offset += 1
        return offset

    def reset_game(self):
        self.board = Board()
        self.score = 0
        self.gameOver = False
        self.hold_piece = None
        self.spawn_piece()

    def spawn_piece(self):
        """Spawns the next piece onto the board and checks for Game Over."""
        self.current_piece = self.next_piece
        self.next_piece = self.pick_new_piece()
        self.can_hold = True
        if self.board.check_collision(self.current_piece.cells):
            self.gameOver = True
            self.play_snd("GameOver")

            self.score_manager.save_result(self.player_name, self.score)

            # обновляем данные после сохранения
            data = self.score_manager.load_player_data(self.player_name)
            self.global_champ = data["global"]
            self.personal_best = data["personal_best"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            if self.gameState == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.player_name:
                        data = self.score_manager.load_player_data(self.player_name)
                        self.global_champ = data["global"]
                        self.personal_best = data["personal_best"]

                        self.gameState = 1
                        self.reset_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.unicode.isprintable() and len(self.player_name) < 15:
                        self.player_name += event.unicode
            else:
                if self.gameOver:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        if event.key == pygame.K_m:
                            self.gameState = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if not self.board.check_collision(
                            [[c[0], c[1] - 1] for c in self.current_piece.cells]
                        ):
                            self.current_piece.move(0, -1)
                            self.play_snd("Move")
                    elif event.key == pygame.K_d:
                        if not self.board.check_collision(
                            [[c[0], c[1] + 1] for c in self.current_piece.cells]
                        ):
                            self.current_piece.move(0, 1)
                            self.play_snd("Move")
                    elif event.key == pygame.K_q:
                        rot = self.current_piece.get_rotated_cells(False)
                        if not self.board.check_collision(rot):
                            self.current_piece.cells = rot
                            self.play_snd("Rotate")
                    elif event.key == pygame.K_e:
                        rot = self.current_piece.get_rotated_cells(True)
                        if not self.board.check_collision(rot):
                            self.current_piece.cells = rot
                            self.play_snd("Rotate")
                    elif event.key == pygame.K_c and self.can_hold:
                        self.play_snd("Hold")
                        if not self.hold_piece:
                            self.hold_piece = Piece(self.current_piece.type)
                            self.spawn_piece()
                        else:
                            curr_type = self.current_piece.type
                            self.current_piece = Piece(self.hold_piece.type)
                            self.hold_piece = Piece(curr_type)
                        self.can_hold = False
                    elif event.key in [pygame.K_SPACE, pygame.K_z]:
                        off = self.get_ghost_offset()
                        self.current_piece.move(off, 0)
                        self.score += off * 2
                        self.play_snd("HardDrop")
                        self.lock_and_spawn()

    def lock_and_spawn(self):
        """Locks the current piece onto the board and triggers line clearing."""
        self.board.lock_piece(self.current_piece)
        self.play_snd("Drop")
        lines = self.board.clear_lines()
        if lines > 0:
            self.play_snd("4Lines" if lines == 4 else "OneLine")
            self.score += {1: 100, 2: 300, 3: 700, 4: 1500}.get(lines, 0)
        self.score += 10
        self.spawn_piece()

    def run(self):
        clock = pygame.time.Clock()
        frames = 0
        while self.running:
            self.handle_events()

            if self.gameState == 1 and not self.gameOver:
                keys = pygame.key.get_pressed()
                delay = (
                    0.05
                    if (keys[pygame.K_s] or keys[pygame.K_DOWN])
                    else self.fall_delay
                )
                if time.perf_counter() - self.last_fall >= delay:
                    if not self.board.check_collision(
                        [[c[0] + 1, c[1]] for c in self.current_piece.cells]
                    ):
                        self.current_piece.move(1, 0)
                        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                            self.score += 1
                            self.play_snd("SoftDrop")
                    else:
                        self.lock_and_spawn()
                    self.last_fall = time.perf_counter()

            self.renderer.draw_background()
            if self.gameState == 0:
                self.renderer.draw_menu(self.player_name, frames)
            else:
                ghost = self.get_ghost_offset() if not self.gameOver else 0
                self.renderer.draw_board(self.board, self.current_piece, ghost)
                self.renderer.draw_ui(
                    self.score,
                    self.next_piece,
                    self.hold_piece,
                    self.global_champ,
                    self.personal_best,
                )
                if self.gameOver:
                    self.renderer.draw_game_over(self.score)

            pygame.display.flip()
            frames += 1
            clock.tick(60)
        pygame.quit()
