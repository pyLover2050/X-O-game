
import os
import sys
import re
import random
import time
import threading
#from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.prompt import IntPrompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich.align import Align


# def colored_text(color: str, text: str):
#     color = getattr(Fore, color.upper(), Fore.WHITE)
#     return color+str(text)+Style.RESET_ALL

# def remove_ansi(text: str):
#     rm = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
#     result = rm.sub('', text)
#     return result

console = Console()



class Game:
    def __init__(self):
        self.board = [
        "-", "-", "-",
        "-", "-", "-",
        "-", "-", "-",
        ]
        self.move = 1
        self.turn = 'Player'
        self.status = Align.left(f'Status: [green]move[/] = {self.move} | [green]turn[/] = {self.turn}')
        self.welcome_msg =  Align.center('[green i] Welcome to x-o game!\n')
        

    def show_board(self) -> None:
            console.clear()

            table = Table(
                show_lines=True,
                show_edge=False,
                show_header= False, )

            for i in range(0, 9, 3):
                column = [f'[bold blue]{j}' if j != 'O' else f'[bold red]{j}'for j in self.board[i:i+3]]
                table.add_row(*column)

            table = Align.center(table)

            rprint(self.welcome_msg)
            rprint(table)
            rprint()
            rprint(self.status)

    
    def random_empty_cell(self) -> int:
        cell = random.randrange(0, 8)
        if self.board[cell] != '-':
            return self.random_empty_cell()
        else:
            return cell

    def get_empty_cell(self) -> int:
        board = self.board
        patterns = [
            # columns
            {i: board[i] for i in range(0, 3)}, 
            {i: board[i] for i in range(3, 6)},
            {i: board[i] for i in range(6, 9)},

            #rows
            {i: board[i] for i in range(0, 9, 3)},
            {i: board[i] for i in range(1, 10, 3)},
            {i: board[i] for i in range(2, 11, 3)},

            #diagonals
            {i: board[i] for i in range(0, 12, 4)},
            {i: board[i] for i in range(2, 8, 2)},
        ]

        # itrate over the pattern 
        for i in patterns:
            values = list(i.values())
            #check 2 cells out of 3 is O and third one is empty 
            if values.count('O') == 2 and '-' in values:
                return list(i.keys())[values.index('-')]

        for i in patterns:
            values = list(i.values())
            #check 2 cells out of 3 is X and third one is empty 
            if values.count('X') == 2 and '-' in values:
                return list(i.keys())[values.index('-')]

        # if all possible patterns are not match then return a random cell		
        else:
            return self.random_empty_cell()
        


        
    def is_empty(self, index) -> bool:
        return  self.board[index] == "-"
        
    def reset(self) -> None:
        for i in range(len(self.board)):
            self.board[i] = "-"

        self.turn = 'Player'
        self.move = 1
        self.status = Align.left(f'Status: [green]move[/] = {self.move} | [green]turn[/] = {self.turn}')
        
        
    def ask_input(self) -> int:
        move = IntPrompt.ask("[green]Enter the numbers of your selected cell[/green] [1 --> 9] ")
        
        if move > 9 or move < 1:
            rprint(f"[red]You entered an invalid number that is out of range .. please Enter[/red] [1 -->9] ")
            return self.ask_input()
            
        if not self.is_empty(move-1):
            cell = self.board[move-1]
            if cell == "O":
                rprint(f'[red]your move on [/red][ {move} ] [red]is not valid since it is already filled by computer please enter again!')
                return self.ask_input()
            else:
                rprint(f"[red]Cell [/red][ {move} ][red] already filled by you !!... please enter correct one ")
                return self.ask_input()
        return move
            
    def ask_again(self) -> None:
            q = Confirm.ask("Would you like to play again?", default='y', show_default=True)
            if q:
                self.reset()
            else:
                sys.exit(1)
            
            
    def run(self) -> None:

        self.show_board()
        while True:
            my_move = self.ask_input()
            self.board[my_move-1] = "X"
            self.turn = 'Computer'
            self.move = self.move+1
            self.status = Align.left(f'Status: [green]move[/] = {self.move} | [green]turn[/] = {self.turn}')
            self.show_board()
            if self.check_win():
                continue

            time.sleep(1)
            rindex = self.get_empty_cell()
            self.board[rindex] = "O"
            self.move = self.move+1
            self.turn = 'Player'
            self.status = Align.left(f'Status: [green]move[/] = {self.move} | [green]turn[/] = {self.turn}')
            self.show_board()
            if self.check_win():
                continue
                       
            
    def check_win(self) -> bool:
        b = self.board
        pattern = [
            # columns
            b[0:3], b[3:6], b[6:9],
            # rows
            b[0:9:3], b[1:10:3], b[2:11:3],
            # diagonals
            b[0:12:4], b[2:8:2],
        ]
        win_text = Align.center('[green]Yay, you\'ve won :hamburger:')
        loss_text = Align.center('[magenta]Oops, computer won!')
        draw_text = Align.center('[blue]Match draw!')

        for i in pattern:
            if all([j=="X"  for j in i]):
                self.status = win_text
                self.show_board()
                self.ask_again()
                self.show_board()
                return True
            
            elif all([j=="O"  for j in i]):
                self.status = loss_text
                self.show_board()
                self.ask_again()
                self.show_board()
                return True
        else:
            if all([j!="-" for j in b]):
                self.status = draw_text
                self.show_board()
                self.ask_again()
                self.show_board()
                return True
        return False
         
        
        
            
            
            




if __name__=="__main__":
	game = Game()
	game.run()
            
            


            
        
        