#! /usr/bin/env python3

import random
import sys
        
class GameBoard:
    def __init__(self):
        self.board = [
        "-", "-", "-",
        "-", "-", "-",
        "-", "-", "-",
        ]
            
            
    def show_board(self):
            index = 0
            print (" -------------")
            for i in range (3):
                print (" |", end="")
                for j in range (3):
                    print (f" {self.board[index]} |", end= "")
                    index = index+1
                print ()
            print (" -------------")
        
    def get_empty_cell(self):
        emcell = []
        for i, j in enumerate(self.board, start=1):
            if j == "-":
                emcell.append(i)
        return random.choice(emcell)
        
    def is_empty(self, index):
        return  self.board[index] == "-"
        
    def reset(self):
     	for i in range(len(self.board)):
     		self.board[i] = "-"
     
    def ask_input(self):
            move = int(input("Enter the numbers of your selected cells [1 --> 9] "))
            if move > 9 or move < 0:
            	print (f"You entered an invalid number that is out of range .. please Enter [1 -->9] ")
            	move = int(input("Enter the numbers of your selected cells [1 --> 9] "))
            	
            if not self.is_empty(move-1):
                cell = self.board[move-1]
                ran_num = self.get_empty_cell()
                if cell == "O":
                    print (f"your move on {move} is not valid since it is already filled by computer please enter again! ")
                else:
                    print (f" Cell {move} already filled by you !!... please enter correct one ")
            return move
            
    def ask_again(self):
            q = input("You want to play again y/n ").lower()
            if q == "n":
                sys.exit(0)
            else:
            	self.reset ()
            
            
    def run(self):
        print ("Welcome to x-o game ")
        self.show_board()
        while True:
            my_move = self.ask_input()
            if self.is_empty(my_move-1):
                self.board[my_move-1] = "X"
                print (f"Here is how the board looks now after Your move on position {my_move}")
                self.show_board()
                if self.check_win():
                    print (self.check_win())
                    self.ask_again()
                    self.show_board()
                    continue 
                
                rindex = self.get_empty_cell()
                self.board[rindex-1] = "O"
                
                print (f"Here is how the board looks now after computer move on position {rindex}")
                self.show_board()
                
                
                if self.check_win():
                    print (self.check_win())
                    self.ask_again()
                    self.show_board()
                    continue 
                
            
    def check_win(self):
        b = self.board
        wc = [b[0:3], b[3:6], b[6:9],
        b[0:9:3], b[1:10:3], b[2:11:3],
        b[0:12:4], b[2:8:2]]
        for i in wc:
            if all([j=="X"  for j in i]):
                return "------------ Yayy You Won ------------\n_____________________________________________"
            elif all([j=="O"  for j in i]):
                return "------------ Wow Computer Won ------------\n------------Better Luck Next Time------------\n_____________________________________________"
            elif all([j!="-" for j in b]):
                return "------------Hey It's Match Draw! ------------\n------------Lets Play again------------\n_____________________________________________"
                
        return False 
        
        
            
            
            




if __name__=="__main__":
	game = GameBoard()
	game.run()
            
            


            
        
        