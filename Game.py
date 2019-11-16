import time
class Game:
	def __init__(self):
		self.start()

	def field_print(self):
		for i in range(0, 3):
			for j in range(0, 3):
				print('{}|'.format(self.first_stage[i][j]), end=" ")
			print()
		print()

	def start(self):
		self.first_stage = [['*','*','*'],['*','*','*'],['*','*','*']]
		self.gamer_turn = 'X'

	def is_valid(self, px, py):
		if px < 0 or px > 2 or py < 0 or py > 2:
			return False
		elif self.first_stage[px][py] != '*':
			return False
		else:
			return True

	def is_end(self):
		for i in range(0, 3):
			if (self.first_stage[0][i] != '*' and
				self.first_stage[0][i] == self.first_stage[1][i] and
				self.first_stage[1][i] == self.first_stage[2][i]):
				return self.first_stage[0][i]

		for i in range(0, 3):
			if (self.first_stage[i] == ['X', 'X', 'X']):
				return 'X'
			elif (self.first_stage[i] == ['O', 'O', 'O']):
				return 'O'

		if (self.first_stage[0][0] != '*' and
			self.first_stage[0][0] == self.first_stage[1][1] and
			self.first_stage[0][0] == self.first_stage[2][2]):
			return self.first_stage[0][0]

		if (self.first_stage[0][2] != '*' and
			self.first_stage[0][2] == self.first_stage[1][1] and
			self.first_stage[0][2] == self.first_stage[2][0]):
			return self.first_stage[0][2]


		for i in range(0, 3):
			for j in range(0, 3):
				if (self.first_stage[i][j] == '*'):
					return None
		return '*'

	def max(self):
		maxv = -1

		px = None
		py = None

		result = self.is_end()


		if result == 'X':
			return (-1, 0, 0)
		elif result == 'O':
			return (1, 0, 0)
		elif result == '*':
			return (0, 0, 0)

		for i in range(0, 3):
			for j in range(0, 3):
				if self.first_stage[i][j] == '*':
					self.first_stage[i][j] = 'O'
					m = self.min()

					if m > maxv:
						maxv = m
						px = i
						py = j
					self.first_stage[i][j] = '*'
		return (maxv, px, py)

	def min(self):
		minv = 1

		qx = None
		qy = None

		result = self.is_end()

		if result == 'X':
			return (-1, 0, 0)
		elif result == 'O':
			return (1, 0, 0)
		elif result == '*':
			return (0, 0, 0)

		for i in range(0, 3):
			for j in range(0, 3):
				if self.first_stage[i][j] == '*':
					self.first_stage[i][j] = 'X'
					m = self.max()
					if m < minv:
						minv = m
						qx = i
						qy = j
					self.first_stage[i][j] = '*'

		return (minv, qx, qy)

	def play(self):
		while True:
			self.field_print()
			self.result = self.is_end()
			if self.result != None:
				if self.result == '0':
					print('Vitório de 0!')
				elif self.result == 'X':
					print('Vitória de X!')
				elif self.result == '*':
					print("Empate!")

				self.start()
				return

			if self.gamer_turn == 'X':

				while True:

					start = time.time()
					(qx, qy) = self.min()
					end = time.time()
					print('Tempo de processamento: {}s'.format(round(end - start, 7)))
					print('Jogada recomendada: X = {}, Y = {}'.format(qx, qy))

					px = int(input('Movimento de X (0, 1 ou 2): '))
					py = int(input('Movimento de Y (0, 1 ou 2): '))

					(qx, qy) = (px, py)

					if self.is_valid(px, py):
						self.first_stage[px][py] = 'X'
						self.gamer_turn = 'O'
						break
					else:
						print('Jogada inválida')

			else:
				(px, py) = self.max()
				self.first_stage[px][py] = 'O'
				self.gamer_turn = 'X'

def main():
	g = Game()
	g.play()

if __name__ == "__main__":
	main()

