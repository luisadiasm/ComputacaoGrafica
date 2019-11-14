import time
class Jogo:
	def __init__(self):
		self.iniciar_jogo()

	def iniciar_jogo(self):
		self.estado_atual = [['.','.','.'],['.','.','.'],['.','.','.']]
		self.turno_jogador = 'X'

	def printar_campo(self):
		for i in range(0, 3):
			for j in range(0, 3):
				print('{}|'.format(self.estado_atual[i][j]), end=" ")
			print()
		print()

	def is_valid(self, px, py):
		if px < 0 or px > 2 or py < 0 or py > 2:
			return False
		elif self.estado_atual[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		for i in range(0, 3):
			if (self.estado_atual[0][i] != '.' and
				self.estado_atual[0][i] == self.estado_atual[1][i] and
				self.estado_atual[1][i] == self.estado_atual[2][i]):
				return self.estado_atual[0][i]

		for i in range(0, 3):
			if (self.estado_atual[i] == ['X', 'X', 'X']):
				return 'X'
			elif (self.estado_atual[i] == ['O', 'O', 'O']):
				return 'O'

		if (self.estado_atual[0][0] != '.' and
			self.estado_atual[0][0] == self.estado_atual[1][1] and
			self.estado_atual[0][0] == self.estado_atual[2][2]):
			return self.estado_atual[0][0]

		if (self.estado_atual[0][2] != '.' and
			self.estado_atual[0][2] == self.estado_atual[1][1] and
			self.estado_atual[0][2] == self.estado_atual[2][0]):
			return self.estado_atual[0][2]


		for i in range(0, 3):
			for j in range(0, 3):
				if (self.estado_atual[i][j] == '.'):
					return None
		return '.'

	def max(self):
		maxv = -1

		px = None
		py = None

		resultado = self.is_end()


		if resultado == 'X':
			return (-1, 0, 0)
		elif resultado == 'O':
			return (1, 0, 0)
		elif resultado == '.':
			return (0, 0, 0)

		for i in range(0, 3):
			for j in range(0, 3):
				if self.estado_atual[i][j] == '.':
					self.estado_atual[i][j] = 'O'
					(m, min_i, min_j) = self.min()

					if m > maxv:
						maxv = m
						px = i
						py = j
					self.estado_atual[i][j] = '.'
		return (maxv, px, py)

	def min(self):
		minv = 1

		qx = None
		qy = None

		resultado = self.is_end()

		if resultado == 'X':
			return (-1, 0, 0)
		elif resultado == 'O':
			return (1, 0, 0)
		elif resultado == '.':
			return (0, 0, 0)

		for i in range(0, 3):
			for j in range(0, 3):
				if self.estado_atual[i][j] == '.':
					self.estado_atual[i][j] = 'X'
					(m, max_i, max_j) = self.max()
					if m < minv:
						minv = m
						qx = i
						qy = j
					self.estado_atual[i][j] = '.'

		return (minv, qx, qy)

	def play(self):
		while True:
			self.printar_campo()
			self.resultado = self.is_end()
			if self.resultado != None:
				if self.resultado == 'X':
					print('X Ganhou!')
				elif self.resultado == 'O':
					print('0 Ganhou!')
				elif self.resultado == '.':
					print("Empate!")

				self.iniciar_jogo()
				return

			if self.turno_jogador == 'X':

				while True:

					start = time.time()
					(m, qx, qy) = self.min()
					end = time.time()
					print('Tempo de processamento: {}s'.format(round(end - start, 7)))
					print('Jogada recomendada: X = {}, Y = {}'.format(qx, qy))

					px = int(input('Movimento desejado em X: '))
					py = int(input('Movimento desejado em Y: '))

					(qx, qy) = (px, py)

					if self.is_valid(px, py):
						self.estado_atual[px][py] = 'X'
						self.turno_jogador = 'O'
						break
					else:
						print('Jogada invalida.')

			else:
				(m, px, py) = self.max()
				self.estado_atual[px][py] = 'O'
				self.turno_jogador = 'X'

def main():
	g = Jogo()
	g.play()

if __name__ == "__main__":
	main()

