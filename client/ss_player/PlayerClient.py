from __future__ import annotations
import asyncio
import websockets


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

	def __get_start_grid(matrix, player):
		if player == 1:
			matrix[4][4] = 'y'
		else:
			matrix[9][9] = 'z'
		return matrix

	def get_next_grid(matrix, player):
		# 最初の置く位置の指定
		if (self.p1turn == 0 and player == 1)
			self.p1turn += 1
			return (__get_start_grid(matrix, player=1))
		else if (self.p2turn == 0 and player == 2)
			self.p2turn += 1
			return (__get_start_grid(matrix, player=2))

		if player == 1:
			block = 'o'
			p = 'y'
		else:
			block = 'x'
			p = 'z'

		rows = len(matrix)
		cols = len(matrix[0])

		# 新しい行列を作成
		new_matrix = [row[:] for row in matrix]

		# ブロックの位置を記録するリスト
		block_positions = []

		# ブロックの位置を探して記録
		for r in range(rows):
			for c in range(cols):
				if matrix[r][c] == block:
					block_positions.append((r, c))

		# 'block' の位置を基に対角線上の位置を 'p' に置き換え
		for r, c in block_positions:
			# 右上の座標 (r-1, c+1)
			if r > 0 and c < cols - 1:
				if matrix[r-1][c] != block and matrix[r][c+1] != block and matrix[r-1][c+2] != block and matrix[r-2][c+1] != block and matrix[r-1][c+1] == '.':
					new_matrix[r-1][c+1] = p
			# 右下の座標 (r+1, c+1)
			if r < rows - 1 and c < cols - 1:
				if matrix[r+1][c] != block and matrix[r][c+1] != block and matrix[r+1][c+2] != block and matrix[r+2][c+1] != block and matrix[r+1][c+1] == '.':
					new_matrix[r+1][c+1] = p
			# 左下の座標 (r+1, c-1)
			if r < rows - 1 and c > 0:
				if matrix[r+1][c] != block and matrix[r][c-1] != block and matrix[r+1][c-2] != block and matrix[r+2][c-1] != block and matrix[r+1][c-1] == '.':
					new_matrix[r+1][c-1] = p
			# 左上の座標 (r-1, c-1)
			if r > 0 and c > 0:
				if matrix[r-1][c] != block and matrix[r][c-1] != block and matrix[r-1][c-2] != block and matrix[r-2][c-1] != block and matrix[r-1][c-1] == '.':
					new_matrix[r-1][c-1] = p

		return new_matrix

	def make_matrix(board):
        l = 0
        new = ""
        for char in board:
            if char in ('.', 'o', 'x', '\n'):
            new += char
        if new.startswith('\n'):
            new = new[1:]
        if new.endswith('\n'):
            new = new[:-1]
        board_list = new.split(sep = '\n')
        board_matrix = [[char for char in string] for string in board_list]
        return board_matrix

    def create_action(self, board):
		# 文字列から2次元配列に変換する
		board_matrix = make_matrix(board)
	
		# 自分が置ける起点となるマスにマークを加えた配列を作成する
		next_grid = get_next_grid(board_matrix, player = self.player_number)

        #反則を無視して可能な手を全列挙するフェーズ
        #反則の手を潰すフェーズ
        #以降、OKケースの中からヒューリスティックに良い手を探索。以下は現状上がってる選別法
            #相手が置けるマスをより多く潰す手を選ぶ
            #選ぶピースの大きさが大きいものを優先する
            #次の自分のターンで、置けるようになるマスの多さ　＝　置くピースの角の多さ
                #相手のピースの位置も見て、その角が有効かどうかの判定もあるとなおよし

        #選別を経て複数の手が残った場合は、ヤケクソのランダム


        #適当です。
        #readmeのテストが動いて、反則負けできるようにしてあります。
        return 'U034'





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
