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
        self.p1Actions = ['U034', 'B037', 'J266', 'M149', 'O763', 'R0A3', 'F0C6', 'K113', 'T021', 'L5D2', 'G251', 'E291', 'D057', 'A053']
        self.p2Actions = ['A0AA', 'B098', 'N0A5', 'L659', 'K33B', 'J027', 'E2B9', 'C267', 'U07C', 'M3AD', 'O2BB', 'R41C']

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
                    '''
                    return np.array([[1]])
                elif self == BlockType.B:
                    '''
                    type B:
                    ■
                    ■
                    '''
                    return np.array([[1], [1]])
                elif self == BlockType.C:
                    '''
                    type C:
                    ■
                    ■
                    ■
                    '''
                    return np.array([[1], [1], [1]])
                elif self == BlockType.D:
                    '''
                    type D:
                    ■
                    ■ ■
                    '''
                    return np.array([[1, 0], [1, 1]])
                elif self == BlockType.E:
                    '''
                    type E:
                    ■
                    ■
                    ■
                    ■
                    '''
                    return np.array([[1], [1], [1], [1]])
                elif self == BlockType.F:
                    '''
                    type F:
                      ■
                      ■
                    ■ ■
                    '''
                    return np.array([[0, 1], [0, 1], [1, 1]])
                elif self == BlockType.G:
                    '''
                    type G:
                    ■
                    ■ ■
                    ■
                    '''
                    return np.array([[1, 0], [1, 1], [1, 0]])
                elif self == BlockType.H:
                    '''
                    type H:
                    ■ ■
                    ■ ■
                    '''
                    return np.array([[1, 1], [1, 1]])
                elif self == BlockType.I:
                    '''
                    type I:
                    ■ ■
                      ■ ■
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
                    '''
                    return np.array([[1], [1], [1], [1], [1]])
                elif self == BlockType.K:
                    '''
                    type K:
                      ■
                      ■
                      ■
                    ■ ■
                    '''
                    return np.array([[0, 1], [0, 1], [0, 1], [1, 1]])
                elif self == BlockType.L:
                    '''
                    type L:
                      ■
                      ■
                    ■ ■
                    ■
                    '''
                    return np.array([[0, 1], [0, 1], [1, 1], [1, 0]])
                elif self == BlockType.M:
                    '''
                    type M:
                      ■
                    ■ ■
                    ■ ■
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
                    '''
                    return np.array([[1, 0], [1, 1], [1, 0], [1, 0]])
                elif self == BlockType.P:
                    '''
                    type P:
                      ■
                      ■
                    ■ ■ ■
                    '''
                    return np.array([[0, 1, 0], [0, 1, 0], [1, 1, 1]])
                elif self == BlockType.Q:
                    '''
                    type Q:
                    ■
                    ■
                    ■ ■ ■
                    '''
                    return np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]])
                elif self == BlockType.R:
                    '''
                    type R:
                    ■ ■
                      ■ ■
                        ■
                    '''
                    return np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
                elif self == BlockType.S:
                    '''
                    type S:
                    ■
                    ■ ■ ■
                        ■
                    '''
                    return np.array([[1, 0, 0], [1, 1, 1], [0, 0, 1]])
                elif self == BlockType.T:
                    '''
                    type T:
                    ■
                    ■ ■ ■
                      ■
                    '''
                    return np.array([[1, 0, 0], [1, 1, 1], [0, 1, 0]])
                elif self == BlockType.U:
                    '''
                    type U:
                      ■
                    ■ ■ ■
                      ■
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

        # もらった盤面に、次打てるマスを追加して返す関数 ==================done
        def __get_start_grid(matrix, player):
            if player == 1:
                matrix[4][4] = 'y'
            else:
                matrix[9][9] = 'z'
            return matrix

        def get_next_grid(matrix, player):

            new_matrix = matrix
            ## 最初の置く位置の指定
            #if (self.p1turn == 0 and player == 1):
            #    return (__get_start_grid(matrix, player=1))
            #elif self.p2turn == 0 and player == 2 :
            #    return (__get_start_grid(matrix, player=2))

            #if player == 1:
            #    block = 'o'
            #    p = 'y'
            #else:
            #    block = 'x'
            #    p = 'z'

            #rows = len(matrix)
            #cols = len(matrix[0])

            ## 新しい行列を作成
            #new_matrix = [row[:] for row in matrix]

            ## ブロックの位置を記録するリスト
            #block_positions = []

            ## ブロックの位置を探して記録
            #for r in range(rows):
            #    for c in range(cols):
            #        if matrix[r][c] == block:
            #            block_positions.append((r, c))

            ## 'block' の位置を基に対角線上の位置を 'p' に置き換え
            #for r, c in block_positions:
            #    # 右上の座標 (r-1, c+1)
            #    if r > 0 and c < cols - 1:
            #        if matrix[r-1][c] != block and matrix[r][c+1] != block and matrix[r-1][c+2] != block and matrix[r-2][c+1] != block and matrix[r-1][c+1] == '.':
            #            new_matrix[r-1][c+1] = p
            #    # 右下の座標 (r+1, c+1)
            #    if r < rows - 1 and c < cols - 1:
            #        if matrix[r+1][c] != block and matrix[r][c+1] != block and matrix[r+1][c+2] != block and matrix[r+2][c+1] != block and matrix[r+1][c+1] == '.':
            #            new_matrix[r+1][c+1] = p
            #    # 左下の座標 (r+1, c-1)
            #    if r < rows - 1 and c > 0:
            #        if matrix[r+1][c] != block and matrix[r][c-1] != block and matrix[r+1][c-2] != block and matrix[r+2][c-1] != block and matrix[r+1][c-1] == '.':
            #            new_matrix[r+1][c-1] = p
            #    # 左上の座標 (r-1, c-1)
            #    if r > 0 and c > 0:
            #        if matrix[r-1][c] != block and matrix[r][c-1] != block and matrix[r-1][c-2] != block and matrix[r-2][c-1] != block and matrix[r-1][c-1] == '.':
            #            new_matrix[r-1][c-1] = p

            return new_matrix
        # ===============================================

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
                # TODO: 未test
                def is_out(next_grid, piece_map, i, j, a, b) -> bool:
                    for p in range(piece_map.shape[0]):
                        for q in range(piece_map.shape[1]):
                            if piece_map[p][q] == 1:
                                if i-a+p < 0 or i-a+p > 13 or j-b+q < 0 or j-b+q > 13:
                                    return True
                # ===============================================

                # ===== ピースの隣接判定 ==========================yet
                # TODO: 未test
                # TODO: 未test
                def is_neighbor(next_grid, piece_map, i, j, a, b) -> bool:
                    for p in range(piece_map.shape[0]):
                        for q in range(piece_map.shape[1]):
                            if piece_map[p][q] == 1:
                                r = i-a+p
                                c = j-b+q

                                if r-1 < 0 or r+1 > 13 or c-1 < 0 or c+1 > 13:
                                    continue
                                # FIXME: プレイヤーナンバーごとに隣接チェック対象の文字を変える
                                block = 'o' if self._player_number == 1 else 'x'
                                if (next_grid[r-1][c] == block or next_grid[r][c+1] == block or next_grid[r+1][c] == block or next_grid[r][c-1] == block):
                                    return True
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
                                if rf % 2 == 1:
                                    piece_map = np.flipud(piece_map)
                                if rf == 0 or rf == 1:
                                    pass
                                elif rf == 2 or rf == 3:
                                    piece_map = np.rot90(piece_map, 3).copy()
                                elif rf == 4 or rf == 5:
                                    piece_map = np.rot90(piece_map, 2).copy()
                                elif rf == 6 or rf == 7:
                                    piece_map = np.rot90(piece_map, 1).copy()
                                #print(piece, rf)
                                #tmp = piece_map_origin.block_map
                                #for row in tmp:
                                #    print(row)
                                #print("=====")
                                #for row in piece_map:
                                #    print(row)
                                #ピースの各マスについて、y or zに重ねて置いた時、反則でないかどうかを判定する。
                                for a in range(piece_map.shape[0]):
                                    for b in range(piece_map.shape[1]):
                                        if piece_map[a][b] == 1:
                                            if is_ok(next_grid, piece_map, i, j, a, b):
                                                ok_cases.append(get_ok_string(piece, rf, i, j, a, b))
                                                tmp.append([get_ok_string(piece, rf, i, j, a, b), piece, rf, i, j, a, b, piece_map])
                        #print("i, j: ", i, j)

                            #置けるかどうかの判定
                            #置ける場合は、その手をリストに追加

            return ok_cases, tmp

        # ===============================================


        # ヒューリスティックに良い手を選ぶ関数 ==================yet
        def dicide_hand(ok_cases, tmp) -> str:
            id = random.randrange(len(ok_cases))
            print(tmp[id])
            return ok_cases[id]


        # 以下、==========================================
        # 処理のフロー ====================================

        # 文字列から2次元配列に変換する
        print("player_num", self._player_number)
        board_matrix = make_matrix(board)

        #for row in board_matrix:
        #    print(row)

        # 自分が置ける起点となるマスにマークを加えた配列を作成する
        next_grid = get_next_grid(board_matrix, player = self._player_number)
        print("next_grid")
        for row in next_grid:
            print(row)
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
            # 選別を経て複数の手が残った場合は、ヤケクソのランダム
        #返り値は、単一の文字列が好ましいと思われる。多分。
        this_turn_hand = dicide_hand(ok_cases, tmp)
        print("this_turn_hand: ", this_turn_hand)
        #if self._player_number == 2:
        #    sys.exit()

        #選択した手を手札から削除
        self.my_hands.remove(this_turn_hand[0])

        #次の手番に備えて、手番を進める
        self.p1turn += 1
        self.p2turn += 1

        #適当です。
        #readmeのテストが動いて、反則負けできるようにしてあります。
        return this_turn_hand





        #以下、もともとのcreate_action内部
    #def create_action(self, board):
    #    actions: list[str]
    #    turn: int

    #    if self.player_number == 1:
    #        actions = self.p1Actions
    #        turn = self.p1turn
    #        self.p1turn += 1
    #    else:
    #        actions = self.p2Actions
    #        turn = self.p2turn
    #        self.p2turn += 1

    #    if len(actions) > turn:
    #        return actions[turn]
    #    else:
    #        # パスを選択
    #        return 'X000'

    @staticmethod
    async def create(url: str, loop: asyncio.AbstractEventLoop) -> PlayerClient:
        socket = await websockets.connect(url)
        print('PlayerClient: connected')
        player_number = await socket.recv()
        print(f'player_number: {player_number}')
        return PlayerClient(int(player_number), socket, loop)
