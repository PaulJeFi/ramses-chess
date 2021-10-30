from best_move import *
from graphic import *

BLUE = (0, 0, 255)
def cadre(position) :
   	pygame.draw.rect(screen, BLUE, (position[0], position[1], size, 5))
   	pygame.draw.rect(screen, BLUE, (position[0], position[1], 5, size))
   	pygame.draw.rect(screen, BLUE, (position[0], position[1]+size-5, size, 5))
   	pygame.draw.rect(screen, BLUE, (position[0]+size-5, position[1], 5, size))
   	pygame.display.update()


class Main() :
	def __init__(self) :
		self.turn = "Human"
		self.selected = (0, 0)
		self.selection = []
		self.move_list = [None]

	def case(self, position) :
		lettre = None
		chiffre = None
		if position[0] == 0*size :
			lettre = 'a'
		elif position[0] == 1*size :
			lettre = 'b'
		elif position[0] == 2*size :
			lettre = 'c'
		elif position[0] == 3*size :
			lettre = 'd'
		elif position[0] == 4*size :
			lettre = 'e'
		elif position[0] == 5*size :
			lettre = 'f'
		elif position[0] == 6*size :
			lettre = 'g'
		elif position[0] == 7*size :
			lettre = 'h'
		if position[1] == 0*size :
			chiffre = '8'
		elif position[1] == 1*size :
			chiffre = '7'
		elif position[1] == 2*size :
			chiffre = '6'
		elif position[1] == 3*size :
			chiffre = '5'
		elif position[1] == 4*size :
			chiffre = '4'
		elif position[1] == 5*size :
			chiffre = '3'
		elif position[1] == 6*size :
			chiffre = '2'
		elif position[1] == 7*size :
			chiffre = '1'
		return (lettre + chiffre)


	def mouse_case(self, mouse) :
		lettre = int
		if (mouse >= 0*size) and (mouse <= 1*size) :
			lettre = 0*size
		elif (mouse >= 1*size) and (mouse <= 2*size) :
			lettre = 1*size
		elif (mouse >= 2*size) and (mouse <= 3*size) :
			lettre = 2*size
		elif (mouse >= 3*size) and (mouse <= 4*size) :
			lettre = 3*size
		elif (mouse >= 4*size) and (mouse <= 5*size) :
			lettre = 4*size
		elif (mouse >= 5*size) and (mouse <= 6*size) :
			lettre = 5*size
		elif (mouse >= 6*size) and (mouse <= 7*size) :
			lettre = 6*size
		elif (mouse >= 7*size) and (mouse <= 8*size) :
			lettre = 7*size
		return (lettre)

	def main(self) :
		board = chess.Board()
		show(board.fen(), board, self.move_list[-1])
		while True :
			if self.turn == "BOT" :
				if not game_is_finished(board) :
					move, evalu = best_move(board)
					if evalu is float :
						if board.turn == chess.WHITE :
							print(evalu)
						else :
							print(-evalu)
					else :
						print(evalu)
					board.push(chess.Move.from_uci(move))
					print(move)
					print(board.fen())
					self.move_list.append(move)
					show(board.fen(), board, self.move_list[-1])
				cadre(self.selected)
				self.selection = []
				self.turn = "Human"
			while self.turn == "Human" :
				for event in pygame.event.get() :
					if event.type == pygame.QUIT :
						pygame.quit()

					if event.type == pygame.KEYDOWN :
						if event.key == pygame.K_UP :
							# Aller en haut et afficher.
							self.selected = (self.selected[0], self.selected[1] - size)
							show(board.fen(), board, self.move_list[-1])
							cadre(self.selected)

						elif event.key == pygame.K_DOWN :
							# Aller en bas et afficher.
							self.selected = (self.selected[0], self.selected[1] + size)
							show(board.fen(), board, self.move_list[-1])
							cadre(self.selected)

						elif event.key == pygame.K_LEFT :
							# Aller à gauche et afficher.
							self.selected = (self.selected[0] - size, self.selected[1])
							show(board.fen(), board, self.move_list[-1])
							cadre(self.selected)

						elif event.key == pygame.K_RIGHT :
							# Aller à droite et afficher.
							self.selected = (self.selected[0] + size, self.selected[1])
							show(board.fen(), board, self.move_list[-1])
							cadre(self.selected)

						elif event.key == pygame.K_SPACE :
							# Ajouter la position à la liste.
							if self.selected in self.selection :
								self.selection.remove(self.selected)
							else :
								self.selection.append(self.selected)
							show(board.fen(), board, self.move_list[-1])
							cadre(self.selected)

						elif event.key == pygame.K_RETURN :
							try:
								move = chess.Move.from_uci(self.case(self.selection[0]) + self.case(self.selection[1]))
								if move in board.legal_moves :
									board.push(move)
									self.move_list.append(str(move))
									show(board.fen(), board, self.move_list[-1])
									self.turn = "BOT"
									self.selection = []
							except Exception :
								self.selection = []

						elif event.key == pygame.K_p :
							board.pop()
							self.move_list.pop()
							show(board.fen(), board, self.move_list[-1])

						elif event.key == pygame.K_n :
							board = chess.Board()
							show(board.fen(), board, self.move_list[-1])

						elif event.key == pygame.K_f :
							print(board.fen())

						elif event.key == pygame.K_s :
							c = str(input("Paste FEN :"))
							board = chess.Board(c)
							show(board.fen(), board, self.move_list[-1])

						elif event.key == pygame.K_e :
							self.turn = "BOT"

						elif event.key == pygame.K_a :
							move, evalu = best_move(board)
							if evalu is float :
								if board.turn == chess.WHITE :
									print(evalu)
								else :
									print(evalu)
							else :
								print(evalu)
							print(move)
							print(board.fen())

					if event.type == pygame.MOUSEBUTTONDOWN :
						if event.button == 3 :
							board.pop()
							show(board.fen(), board, self.move_list[-1])
						if event.button == 1 :
							(x, y) = pygame.mouse.get_pos()
							mouse = (x, y)
							self.selected = (self.mouse_case(mouse[0]), self.mouse_case(mouse[1]))
							cadre(self.selected)
							if self.selected in self.selection :
								self.selection.remove(self.selected)
							else :
								self.selection.append(self.selected)
							show(board.fen(), board, self.move_list[-1])
							cadre(self.selected)
							if len(self.selection) == 2 :
								try:
									move = chess.Move.from_uci(self.case(self.selection[0]) + self.case(self.selection[1]))
									if move in board.legal_moves :
										board.push(move)
										self.move_list.append(str(move))
										show(board.fen(), board, self.move_list[-1])
										self.turn = "BOT"
										self.selection = []
										show(board.fen(), board, self.move_list[-1])
									show(board.fen(), board)
								except Exception :
									self.selection = []
							show(board.fen(), board, self.move_list[-1])




			show(board.fen(), board, self.move_list[-1])

echecs = Main()
echecs.main()
