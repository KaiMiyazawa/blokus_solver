from __future__ import annotations
import asyncio
import websockets

from enum import Enum
from typing import Any

import numpy as np

import random
import sys

class PlayerClient:
    def __init__(self, player_number: int, socket: websockets.WebSocketClientProtocol, loop: asyncio.AbstractEventLoop):
        self._loop = loop

        #ソケット(出入り口)
        #ここから入力し、ここに出力するイメージ。使い方の詳細はもともとのプログラム参照。もしくはドキュメント。
        self._socket = socket

        # 先行の場合は1, 後攻の場合は2 ??
        # 要確認。説明スライドではスライドではこう言ってただけ。
        self._player_number = player_number

        # テストケースの手番。
        #ランダムではなく、最初に置くべきマス(5,5) (A,A)を満たした良いテストケース。
        #self.p1Actions = ['U034', 'B037', 'J266', 'M149', 'O763', 'R0A3', 'F0C6', 'K113', 'T021', 'L5D2', 'G251', 'E291', 'D057', 'A053']
        #self.p2Actions = ['A0AA', 'B098', 'N0A5', 'L659', 'K33B', 'J027', 'E2B9', 'C267', 'U07C', 'M3AD', 'O2BB', 'R41C']

        #お互いが何回打ったかをカウントしている変数。
        #仕様として残す必要もないが、考え方としては重要なので理解しておくべき
        self.p1turn = 0
        self.p2turn = 0

        self.my_hands = [chr(ord("A")+i) for i in range(21)]
        self.ene_hands = [chr(ord("A")+i) for i in range(21)]

    @property
    def player_number(self) -> int:
        return self._player_number

    async def close(self):
        await self._socket.close()

    async def play(self):
        while True:
            board = await self._socket.recv()
            action = self.create_action(board)
            await self._socket.send(action)
            if action == 'X000':
                raise SystemExit

    def create_action(self, board):
        #ピースの形状を定義するクラス ==========================done
        class BlockType(Enum):
            A = 'A'
            B = 'B'
            C = 'C'
            D = 'D'
            E = 'E'
            F = 'F'
            G = 'G'
            H = 'H'
            I = 'I'
            J = 'J'
            K = 'K'
            L = 'L'
            M = 'M'
            N = 'N'
            O = 'O'
            P = 'P'
            Q = 'Q'
            R = 'R'
            S = 'S'
            T = 'T'
            U = 'U'
            X = 'X'

            @property
            def block_map(self) -> np.ndarray[Any, np.dtype[int]]:
                if self == BlockType.A:
                    '''
                    type A:
                    ■
                    corner:4
                    '''
                    return np.array([[1]])
                elif self == BlockType.B:
                    '''
                    type B:
                    ■
                    ■
                    corner: 4
                    '''
                    return np.array([[1], [1]])
                elif self == BlockType.C:
                    '''
                    type C:
                    ■
                    ■
                    ■
                    corner: 4
                    '''
                    return np.array([[1], [1], [1]])
                elif self == BlockType.D:
                    '''
                    type D:
                    ■
                    ■ ■
                    corner: 5
                    '''
                    return np.array([[1, 0], [1, 1]])
                elif self == BlockType.E:
                    '''
                    type E:
                    ■
                    ■
                    ■
                    ■
                    corner: 4
                    '''
                    return np.array([[1], [1], [1], [1]])
                elif self == BlockType.F:
                    '''
                    type F:
                      ■
                      ■
                    ■ ■
                    corner: 5
                    '''
                    return np.array([[0, 1], [0, 1], [1, 1]])
                elif self == BlockType.G:
                    '''
                    type G:
                    ■
                    ■ ■
                    ■
                    corner: 6
                    '''
                    return np.array([[1, 0], [1, 1], [1, 0]])
                elif self == BlockType.H:
                    '''
                    type H:
                    ■ ■
                    ■ ■
                    corner: 4
                    '''
                    return np.array([[1, 1], [1, 1]])
                elif self == BlockType.I:
                    '''
                    type I:
                    ■ ■
                      ■ ■
                    corner: 6
                    '''
                    return np.array([[1, 1, 0], [0, 1, 1]])
                elif self == BlockType.J:
                    '''
                    type J:
                    ■
                    ■
                    ■
                    ■
                    ■
                    corner: 4
                    '''
                    return np.array([[1], [1], [1], [1], [1]])
                elif self == BlockType.K:
                    '''
                    type K:
                      ■
                      ■
                      ■
                    ■ ■
                    corner: 5
                    '''
                    return np.array([[0, 1], [0, 1], [0, 1], [1, 1]])
                elif self == BlockType.L:
                    '''
                    type L:
                      ■
                      ■
                    ■ ■
                    ■
                    corner: 6
                    '''
                    return np.array([[0, 1], [0, 1], [1, 1], [1, 0]])
                elif self == BlockType.M:
                    '''
                    type M:
                      ■
                    ■ ■
                    ■ ■
                    corner: 5
                    '''
                    return np.array([[0, 1], [1, 1], [1, 1]])
                elif self == BlockType.N:
                    '''
                    type N:
                    ■ ■
                      ■
                    ■ ■

                    '''
                    return np.array([[1, 1], [0, 1], [1, 1]])
                elif self == BlockType.O:
                    '''
                    type O:
                    ■
                    ■ ■
                    ■
                    ■
                    corner: 6
                    '''
                    return np.array([[1, 0], [1, 1], [1, 0], [1, 0]])
                elif self == BlockType.P:
                    '''
                    type P:
                      ■
                      ■
                    ■ ■ ■
                    corner: 6
                    '''
                    return np.array([[0, 1, 0], [0, 1, 0], [1, 1, 1]])
                elif self == BlockType.Q:
                    '''
                    type Q:
                    ■
                    ■
                    ■ ■ ■
                    corner: 5
                    '''
                    return np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]])
                elif self == BlockType.R:
                    '''
                    type R:
                    ■ ■
                      ■ ■
                        ■
                    corner: 7
                    '''
                    return np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
                elif self == BlockType.S:
                    '''
                    type S:
                    ■
                    ■ ■ ■
                        ■
                    corner: 6
                    '''
                    return np.array([[1, 0, 0], [1, 1, 1], [0, 0, 1]])
                elif self == BlockType.T:
                    '''
                    type T:
                    ■
                    ■ ■ ■
                      ■
                    corner: 7
                    '''
                    return np.array([[1, 0, 0], [1, 1, 1], [0, 1, 0]])
                elif self == BlockType.U:
                    '''
                    type U:
                      ■
                    ■ ■ ■
                      ■
                    corner: 8
                    '''
                    return np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
                elif self == BlockType.X:
                    '''
                    type X:パスをする時用



                    '''
                    return np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

                else:
                    raise NotImplementedError
        # ========================================================

        # もらった盤面を2次元配列に変換する ==================done
        def make_matrix(board):
            l = 0
            new = ""
            for char in board:
                if char in ('.', 'o', 'x', '\n'):
                    new += str(char)
            if new.startswith('\n'):
                new = new[1:]
            if new.endswith('\n'):
                new = new[:-1]
            board_list = new.split(sep = '\n')
            board_matrix = [[char for char in string] for string in board_list]
            return board_matrix
        # ===============================================

        # 反則でない手を全列挙する関数 ===============================
        # 長いので階層構造に注意して読んでください。
        def get_ok_cases(next_grid) -> list[str]:
            #置けるますに対して、置ける手を全列挙する。
            #反則でないもののみをlistにappendしていく。
            #そのリストを返す。

            # 反則判定の関数 ========================================
            # 完全に反則でない手の場合のみ、Trueを返す関数
            # もちろん、反則はFalseを返す。
            def is_ok(next_grid, piece_map, i, j, a, b) -> bool:

                # ===== ピースの重なり判定=========================
                # y or z なのは、next_grid[i][j]。
                # y or z と piece_map[a][b] が重なるかどうかを判定する。
                # 要は、
                # piece_map[0][0] は、next_grid[i-a][j-b] と重なるように置かれる。
                # この時、piece_mapの中で1が立っているマスについて、
                # すでに置かれているマスと重なるように置かれていないかどうかを判定する。
                def is_dup(next_grid, piece_map, i, j, a, b) -> bool:
                    for p in range(piece_map.shape[0]):
                        for q in range(piece_map.shape[1]):
                            if piece_map[p][q] == 1:
                                if next_grid[i-a+p][j-b+q] == 'o' or next_grid[i-a+p][j-b+q] == 'x':
                                    return True

                # ===============================================

                # ===== ピースの盤面外判定 ========================
                def is_out(next_grid, piece_map, i, j, a, b) -> bool:
                    for p in range(piece_map.shape[0]):
                        for q in range(piece_map.shape[1]):
                            if piece_map[p][q] == 1:
                                if i-a+p < 0 or i-a+p > 13 or j-b+q < 0 or j-b+q > 13:
                                    return True
                # ===============================================

                # ===== ピースの隣接判定 ==========================yet
                def is_neighbor(next_grid, piece_map, i, j, a, b) -> bool:
                    if self.player_number == 1:
                        block = 'o'
                    else:
                        block = 'x'

                    grid_size = len(next_grid)
                    for p in range(piece_map.shape[0]):
                        for q in range(piece_map.shape[1]):
                            if piece_map[p][q] == 1:
                                r = i - a + p
                                c = j - b + q

                                # Skip if r or c is out of the grid bounds
                                if r < 0 or r >= grid_size or c < 0 or c >= grid_size:
                                    continue

                                # Check corners and edges separately
                                if r == 0 and c == 0:
                                    if next_grid[r+1][c] == block or next_grid[r][c+1] == block:
                                        return True
                                elif r == 0 and c == grid_size - 1:
                                    if next_grid[r+1][c] == block or next_grid[r][c-1] == block:
                                        return True
                                elif r == grid_size - 1 and c == 0:
                                    if next_grid[r-1][c] == block or next_grid[r][c+1] == block:
                                        return True
                                elif r == grid_size - 1 and c == grid_size - 1:
                                    if next_grid[r-1][c] == block or next_grid[r][c-1] == block:
                                        return True
                                elif r == 0:
                                    if next_grid[r][c+1] == block or next_grid[r+1][c] == block or next_grid[r][c-1] == block:
                                        return True
                                elif r == grid_size - 1:
                                    if next_grid[r-1][c] == block or next_grid[r][c+1] == block or next_grid[r][c-1] == block:
                                        return True
                                elif c == 0:
                                    if next_grid[r-1][c] == block or next_grid[r][c+1] == block or next_grid[r+1][c] == block:
                                        return True
                                elif c == grid_size - 1:
                                    if next_grid[r-1][c] == block or next_grid[r+1][c] == block or next_grid[r][c-1] == block:
                                        return True
                                else:
                                    if next_grid[r-1][c] == block or next_grid[r][c+1] == block or next_grid[r+1][c] == block or next_grid[r][c-1] == block:
                                        return True

                    return False
                # ===============================================

        # 以下、この関数のフロー
                # 最初に盤面外判定をしておかないと、他の場面で安心して検証ができない。
                # next_grid をインデックスアウトしないようにするために。
                if is_out(next_grid, piece_map, i, j, a, b): #盤面外判定 = 置こうとしているマス ひとつづつについて、盤面外に出ていないかどうか
                    return False
                if is_dup(next_grid, piece_map, i, j, a, b): #重複判定 = すでに置かれているマスと重なるようにおこうとしてしまっているかどうか
                    # 敵のピースでも自分のピースでも、重なってはいけないべき であることに注意
                    return False
                if is_neighbor(next_grid, piece_map, i, j, a, b): #隣接判定 = すでに置かれている　”自分の” ピースと隣接してしまっているかどうか
                    return False

                return True
                # ===============================================

            # 情報から、手の文字列を生成する関数 =======================yet
            # i, j と、本当に報告すべき座標は異なる。計算が必要。
            def get_ok_string(piece, rf, i, j, a, b) -> str:
                I = i-a+1
                J = j-b+1
                if I >= 10:
                    I = chr(ord('A') + I - 10)
                if J >= 10:
                    J = chr(ord('A') + J - 10)
                return (piece + str(rf) + str(J) + str(I))

            # =====================================================

            def is_corner(i, j) -> bool:
                if self._player_number == 1:
                    block = 'o'
                else:
                    block = 'x'
                if i == 0 and j == 0:
                    if next_grid[1][1] == block:
                        return True
                    return False
                if i == 0 and j == 13:
                    if next_grid[1][12] == block:
                        return True
                    return False
                if i == 13 and j == 0:
                    if next_grid[12][1] == block:
                        return True
                    return False
                if i == 13 and j == 13:
                    if next_grid[12][12] == block:
                        return True
                    return False

                if i == 0:
                    if next_grid[1][j-1] == block or next_grid[1][j+1] == block:
                        return True
                    return False
                if i == 13:
                    if next_grid[12][j-1] == block or next_grid[12][j+1] == block:
                        return True
                    return False
                if j == 0:
                    if next_grid[i-1][1] == block or next_grid[i+1][1] == block:
                        return True
                    return False
                if j == 13:
                    if next_grid[i-1][12] == block or next_grid[i+1][12] == block:
                        return True
                    return False

                if next_grid[i-1][j-1] == block or next_grid[i-1][j+1] == block or next_grid[i+1][j-1] == block or next_grid[i+1][j+1] == block:
                    return True
                return False

            ok_cases = []
            tmp = []

            for i in range(14):
                for j in range(14):
                    cell = next_grid[i][j]
                    #一つずつマスを見ていく
                    #もし置けるマスであれば、そのマスに対して全ての手を試す
                    if is_corner(i, j) or (self._player_number == 1 and self.p1turn == 0 and i == 4 and j == 4) or (self._player_number == 2 and self.p2turn == 0 and i == 9 and j == 9):
                        for piece in self.my_hands:
                            for rf in range(8): # rotate & flip
                                piece_map_origin = BlockType(piece)
                                piece_map = piece_map_origin.block_map
                                if rf == 0 or rf == 1:
                                    pass
                                elif rf == 2 or rf == 3:
                                    piece_map = np.rot90(piece_map, 3).copy()
                                elif rf == 4 or rf == 5:
                                    piece_map = np.rot90(piece_map, 2).copy()
                                elif rf == 6 or rf == 7:
                                    piece_map = np.rot90(piece_map, 1).copy()
                                if rf % 2 == 1:
                                    piece_map = np.fliplr(piece_map)
                                for a in range(piece_map.shape[0]):
                                    for b in range(piece_map.shape[1]):
                                        if piece_map[a][b] == 1:
                                            if is_ok(next_grid, piece_map, i, j, a, b):
                                                ok_cases.append(get_ok_string(piece, rf, i, j, a, b))
                                                tmp.append([get_ok_string(piece, rf, i, j, a, b), piece, rf, i, j, a, b, piece_map])

            return ok_cases, tmp

        # ===============================================
        # FIXME: 人力でベストらしい選択をしているだけ
        def nearest_piece(ok_cases) -> str:
            if (self.p1turn == 0 and self.player_number == 1):
                node = 'R455'
            elif (self.p2turn == 0 and self.player_number == 2):
                node = 'R488'
            else:
                return ok_cases
            if node in ok_cases:
                return [node]
            else:
                return ok_cases

        # NOTE: 相手の置ける場所を潰す
        def jamming_piece(board_matrix, ok_cases) -> str:
            # step1 : 相手の置ける場所をマトリックスに表示する -> get_next_gridの応用
            def is_valid_position(matrix, r, c, block, rows, cols):
                if r < 0 or rows <= r:
                    return True
                if c < 0 or cols <= c:
                    return True
                if matrix[r][c] != block:
                    return True
                return False

            def check_upper_right(matrix, r, c, block, rows, cols):
                return (is_valid_position(matrix, r-1, c, block, rows, cols) and
                        is_valid_position(matrix, r, c+1, block, rows, cols) and
                        is_valid_position(matrix, r-1, c+2, block, rows, cols) and
                        is_valid_position(matrix, r-2, c+1, block, rows, cols) and
                        is_valid_position(matrix, r-1, c+1, block, rows, cols))

            def check_lower_right(matrix, r, c, block, rows, cols):
                return (is_valid_position(matrix, r+1, c, block, rows, cols) and
                        is_valid_position(matrix, r, c+1, block, rows, cols) and
                        is_valid_position(matrix, r+1, c+2, block, rows, cols) and
                        is_valid_position(matrix, r+2, c+1, block, rows, cols) and
                        is_valid_position(matrix, r+1, c+1, block, rows, cols))

            def check_lower_left(matrix, r, c, block, rows, cols):
                return (is_valid_position(matrix, r+1, c, block, rows, cols) and
                        is_valid_position(matrix, r, c-1, block, rows, cols) and
                        is_valid_position(matrix, r+1, c-2, block, rows, cols) and
                        is_valid_position(matrix, r+2, c-1, block, rows, cols) and
                        is_valid_position(matrix, r+1, c-1, block, rows, cols))

            def check_upper_left(matrix, r, c, block, rows, cols):
                return (is_valid_position(matrix, r-1, c, block, rows, cols) and
                        is_valid_position(matrix, r, c-1, block, rows, cols) and
                        is_valid_position(matrix, r-1, c-2, block, rows, cols) and
                        is_valid_position(matrix, r-2, c-1, block, rows, cols) and
                    is_valid_position(matrix, r-1, c-1, block, rows, cols))

            def get_opp_positions(board_matrix):

                if self.player_number == 1:
                    block = 'x'
                else:
                    block = 'o'

                p = 'z'
                rows = len(board_matrix)
                cols = len(board_matrix[0])

                # 新しい行列を作成
                new_matrix = [row[:] for row in board_matrix]

                # ブロックの位置を記録するリスト
                block_positions = []

                # ブロックの位置を探して記録
                for r in range(rows):
                    for c in range(cols):
                        if board_matrix[r][c] == block:
                            block_positions.append((r, c))

                # 'block' の位置を基に対角線上の位置を 'p' に置き換え
                for r, c in block_positions:
                    # 右上の座標 (r-1, c+1)
                    if r > 0 and c < cols - 1 and check_upper_right(board_matrix, r, c, block, rows, cols):
                        new_matrix[r-1][c+1] = p

                    # 右下の座標 (r+1, c+1)
                    if r < rows - 1 and c < cols - 1 and check_lower_right(board_matrix, r, c, block, rows, cols):
                        new_matrix[r+1][c+1] = p

                    # 左下の座標 (r+1, c-1)
                    if r < rows - 1 and c > 0 and check_lower_left(board_matrix, r, c, block, rows, cols):
                        new_matrix[r+1][c-1] = p

                    # 左上の座標 (r-1, c-1)
                    if r > 0 and c > 0 and check_upper_left(board_matrix, r, c, block, rows, cols):
                        new_matrix[r-1][c-1] = p

                return new_matrix

            # step2 : ベターな置き方のリストを（それぞれ比較しながら）作る
            def better_jammers(opponent_start_positions, ok_cases):
                #   a : 置き方一つが何個の置ける場所と重なっているかカウントする
                # NOTE: 辞書型で{case: z_count}を持つことにする
                better_cases_w_count = {}

                for cs in ok_cases:
                    # NOTE: pieceを正しい向きで取得する
                    piece = str(cs[0])
                    rf = int(cs[1])
                    if cs[2] in ['A', 'B', 'C', 'D', 'E']:
                        j = ord(cs[2]) - 55 - 1
                    else:
                        j = int(cs[2]) - 1
                    if cs[3] in ['A', 'B', 'C', 'D', 'E']:
                        i = ord(cs[3]) - 55 - 1
                    else:
                        i = int(cs[3]) - 1
                    piece_map_origin = BlockType(piece)
                    piece_map = piece_map_origin.block_map
                    if rf == 0 or rf == 1:
                        pass
                    elif rf == 2 or rf == 3:
                        piece_map = np.rot90(piece_map, 3).copy()
                    elif rf == 4 or rf == 5:
                        piece_map = np.rot90(piece_map, 2).copy()
                    elif rf == 6 or rf == 7:
                        piece_map = np.rot90(piece_map, 1).copy()
                    if rf % 2 == 1:
                        piece_map = np.fliplr(piece_map)

                    z_count = 0
                    for p in range(piece_map.shape[0]):
                        for q in range(piece_map.shape[1]):
                            if piece_map[p][q] == 1:
                                if opponent_start_positions[i+p][j+q] == 'z':
                                    z_count += 1
                    better_cases_w_count[cs] = z_count
                max_value = max(better_cases_w_count.values())

                # 最大値を持つキーのリストを作成する
                return [k for k, v in better_cases_w_count.items() if v == max_value]

            opponent_start_positions = get_opp_positions(board_matrix)

            better_cases = better_jammers(opponent_start_positions, ok_cases)
            return better_cases

        # NOTE: ピースの大きさを優先する
        def big_piece(better_cases) -> str:
            better_cases_w_size = {}

            for cs in better_cases:
                # NOTE: pieceを正しい向きで取得する
                piece = str(cs[0])
                rf = int(cs[1])
                if cs[2] in ['A', 'B', 'C', 'D', 'E']:
                    j = ord(cs[2]) - 55 - 1
                else:
                    j = int(cs[2]) - 1
                if cs[3] in ['A', 'B', 'C', 'D', 'E']:
                    i = ord(cs[3]) - 55 - 1
                else:
                    i = int(cs[3]) - 1
                piece_map_origin = BlockType(piece)
                piece_map = piece_map_origin.block_map
                if rf == 0 or rf == 1:
                    pass
                elif rf == 2 or rf == 3:
                    piece_map = np.rot90(piece_map, 3).copy()
                elif rf == 4 or rf == 5:
                    piece_map = np.rot90(piece_map, 2).copy()
                elif rf == 6 or rf == 7:
                    piece_map = np.rot90(piece_map, 1).copy()
                if rf % 2 == 1:
                    piece_map = np.fliplr(piece_map)
                size_count = 0
                for p in range(piece_map.shape[0]):
                    for q in range(piece_map.shape[1]):
                        if piece_map[p][q] == 1:
                            size_count += 1
                better_cases_w_size[cs] = size_count
            max_value = max(better_cases_w_size.values())

            # 最大値を持つキーのリストを作成する
            return [k for k, v in better_cases_w_size.items() if v == max_value]

        # TODO: 次に置ける角の数を優先
        def more_corner_piece(better_cases):
            # 新しいリストを初期化
            selected_cases = []

            # better_cases内の各要素をチェック
            for case in better_cases:
                # もし文字列内に 'U' が含まれていれば、新しいリストに追加
                if 'U' in case:
                    selected_cases.append(case)

            # 新しいリストを返す
            return selected_cases
        def more_corner_piece(better_cases) -> str:
            selected_cases = [case for case in better_cases if 'U' in case]
            if len(selected_cases) > 0:
                return selected_cases
            selected_cases.extend([case for case in better_cases if 'T' in case or 'R' in case])
            if len(selected_cases) > 0:
                return selected_cases
            selected_cases.extend([case for case in better_cases if 'S' in case or 'P' in case or 'O' in case or 'I' in case or 'L' in case or 'G' in case])
            if len(selected_cases) > 0:
                return selected_cases
            selected_cases.extend([case for case in better_cases if 'Q' in case or 'N' in case or 'M' in case or 'K' in case or 'F' in case or 'D' in case])
            if len(selected_cases) > 0:
                return selected_cases

            return better_cases

        # ヒューリスティックに良い手を選ぶ関数 ==================yet
        def dicide_hand(board_matrix, ok_cases, tmp) -> str:
            better_cases_1 = []
            better_cases_2 = []
            better_cases_3 = []
            better_cases_4 = []

            better_cases_1 = nearest_piece(ok_cases)
            better_cases_2 = jamming_piece(board_matrix, better_cases_1)
            better_cases_3 = big_piece(better_cases_2)
            better_cases_4 = more_corner_piece(better_cases_3)

            id = random.randrange(len(better_cases_4))
            return better_cases_4[id]


        # 以下、==========================================
        # 処理のフロー ====================================

        # 文字列から2次元配列に変換する
        next_grid = make_matrix(board)

        #反則を無視して可能な手を全列挙するフェーズ
        #反則の手を潰すフェーズ
        #ふたつまとめてget_ok_cases
        ok_cases, tmp = get_ok_cases(next_grid)
        # ok_cases == 反則ではない手のリスト
        # ["A000", "A004", ........ "U0DD"] みたいな感じ

        #反則を無視して可能な手がない場合は、パスの手(X000)を返す
        if len(ok_cases) == 0:
            self.p1turn += 1
            self.p2turn += 1
            return 'X000'

        # ここからヒューリスティックに良い手を選ぶ
        #以降、OKケースの中からヒューリスティックに良い手を探索。以下は現状上がってる選別法
            #相手が置けるマスをより多く潰す手を選ぶ
            #選ぶピースの大きさが大きいものを優先する
            #次の自分のターンで、置けるようになるマスの多さ　＝　置くピースの角の多さ
                #相手のピースの位置も見て、その角が有効かどうかの判定もあるとなおよし
            # 選別を経て複数の手が残った場合は、ランダム
        this_turn_hand = dicide_hand(next_grid, ok_cases, tmp)

        #選択した手を手札から削除
        self.my_hands.remove(this_turn_hand[0])

        #次の手番に備えて、手番を進める
        self.p1turn += 1
        self.p2turn += 1

        return this_turn_hand

    @staticmethod
    async def create(url: str, loop: asyncio.AbstractEventLoop) -> PlayerClient:
        socket = await websockets.connect(url)
        print('PlayerClient: connected')
        player_number = await socket.recv()
        print(f'player_number: {player_number}')
        return PlayerClient(int(player_number), socket, loop)
