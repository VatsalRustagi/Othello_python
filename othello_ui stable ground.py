import tkinter
import othello

# class OthelloGrid:
#     def __init__(self):
#         self.rows,self.cols,self.cell_length = 4,4,75
#         self.grid = othello.new_game(self.rows,self.cols,'B','B')
#         self.width,self.height = self.cell_length*self.cols,self.cell_length*self.rows
#
#         #Creating a master window
#         self.board = tkinter.Tk()
#         self.board.configure(bg = '#258e25')
#
#         #Variable Strings
#         self.turn_text = tkinter.StringVar()
#         self.turn_text.set('TURN : {}'.format(self.grid.get_turn()))
#         b,w = self.grid.get_count()
#         self.count_text = tkinter.StringVar()
#         self.count_text.set('Black: {}\nWhite: {}'.format(b,w))
#
#         #Turn Label
#         self.turn_label = tkinter.Label(master = self.board,textvariable = self.turn_text,
#                                         font = ('Arial', 20),fg = 'black', bg = '#258e25',activebackground = 'cyan')
#         self.turn_label.grid(row = 0, column = 0,padx = 10, pady = 10)
#
#         #Count Label
#         count_label = tkinter.Label(
#             master= self.board, textvariable = self.count_text, font = ('Arial', 20),fg = 'black',
#             bg = '#258e25'
#         )
#         count_label.grid(row = 0, column = 1,pady = 10,padx =10)
#
#         #Canvas
#         self.board_canvas = tkinter.Canvas(
#             master=self.board, width = self.width, height = self.height,
#             background = '#258e25', bd = 0
#         )
#         self.board_canvas.grid(row = 1,column = 0, columnspan = 2,
#                                sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
#
#         self.board_canvas.bind('<Configure>', self.canvas_resize)
#         self.print_board()
#         self.board_canvas.bind('<Button-1>',self.press)
#         self.board.rowconfigure(0, weight = 1)
#         self.board.rowconfigure(1, weight = 1)
#         self.board.columnconfigure(0, weight = 1)
#         self.board.columnconfigure(1, weight = 1)
#
#
#     def print_board(self):
#         self.wr = self.board_canvas.winfo_width()/self.width
#         self.hr = self.board_canvas.winfo_height()/self.height
#         self.board_canvas.delete(tkinter.ALL)
#         self.create_board()
#         l = self.cell_length
#         for i in range(self.grid.rows()):
#             for j in range(self.grid.cols()):
#                 if self.grid._board[i][j] == othello.BLACK:
#                     self.board_canvas.create_oval(
#                         (j*l+10)*self.wr,(i*l+10)*self.hr,
#                         ((j+1)*l-10)*self.wr,((i+1)*l-10)*self.hr,
#                         fill = 'black')
#                 elif self.grid._board[i][j] == othello.WHITE:
#                     self.board_canvas.create_oval(
#                         (j*l+10)*self.wr,(i*l+10)*self.hr,
#                         ((j+1)*l-10)*self.wr,((i+1)*l-10)*self.hr,
#                         fill = 'white')
#         self.grid.count_discs()
#
#         #Update Count
#         b,w = self.grid.get_count()
#         self.count_text.set('Black: {}\nWhite: {}'.format(b,w))
#
#         if not self.grid.game_over():
#             self.turn_text.set('Turn : {}'.format(self.grid.get_turn()))
#
#     def press(self,event: tkinter.Event):
#         row = int(event.y/(self.cell_length*self.hr))
#         col = int(event.x/(self.cell_length*self.wr))
#         print(event.y,event.x)
#         print(row,col)
#         l = self.cell_length
#         try:
#             if not (0 <= row < self.rows and 0 <= col < self.cols):
#                 raise othello.InvalidMoveError()
#             othello.make_move(self.grid,row,col)
#             if not othello.if_valid_move_exists(self.grid):
#                 raise othello.NoMoveError()
#             self.print_board()
#         except othello.InvalidMoveError:
#             print("Invalid!")
#         except othello.NoMoveError:
#             self.grid.skip_turn()
#             if not othello.if_valid_move_exists(self.grid):
#                 self.declare_winner('>')
#             else:
#                 self.print_board()
#
#     def declare_winner(self,decider):
#         self.grid.game_over()
#         self.print_board()
#         black,white = self.grid.get_count()
#         self.turn_label.config(state= tkinter.ACTIVE)
#         if  black > white and decider == '>' or black < white and decider == '<':
#             self.turn_text.set('Black Wins!'.format(self.grid.get_turn()))
#         elif black == white:
#             self.turn_text.set("It's a Draw!".format(self.grid.get_turn()))
#         else:
#             self.turn_text.set('White Wins!'.format(self.grid.get_turn()))
#
#     def create_board(self):
#         cl = self.cell_length
#
#         for i in range(self.cols-1):
#             self.board_canvas.create_line(cl*self.wr,0*self.hr,
#                                           cl*self.wr,self.height*self.hr)
#             cl += self.cell_length
#
#         cl = self.cell_length
#
#         for i in range(self.rows-1):
#             self.board_canvas.create_line(0*self.wr,cl*self.hr,
#                                           self.width*self.wr,cl*self.hr)
#             cl += self.cell_length
#
#     def canvas_resize(self,event):
#         self.print_board()
#
#     def start(self):
#         self.board.mainloop()
#
#
# OthelloGrid().start()

# class Menu:
#     def __init__(self):
#         self.menu_window = tkinter.Tk()
#
#         # 'Select Rows' label
#         rows_label = tkinter.Label(
#             master= self.menu_window, text = 'Select Rows:', font = ('Helvetica', 20)
#         )
#         rows_label.grid(row = 0, column = 0)
#
#         # Rows Spinbox
#         self.rows_spinbox = tkinter.Spinbox(
#             master= self.menu_window, width = 20,
#         )
#         self.rows_entry.grid(row = 0, column = 1)
#
#         # Done Button
#         button_frame = tkinter.Frame(master= self.menu_window) #Include the cancel button into this frame
#
#         button_frame.grid(
#             row = 1, column = 0, columnspan = 2, padx = 10, pady = 10,
#             sticky = tkinter.E + tkinter.S)
#
#         ok_button = tkinter.Button(
#             master= button_frame, text = 'Done', font = ('Helvetica', 20),
#             command = self.ok_clicked
#         )
#
#         ok_button.grid(row = 0, column = 0)
#
#     def start(self):
#         self.menu_window.mainloop()
#
#     def ok_clicked(self):
#         print(self.rows_entry.get())
#
#     def play(self):
#         pass
#
# def show_ui() -> None:
#     Menu().start()
#     """
#     root_window = tkinter.Tk()
#
#     button = tkinter.Button(
#         master = root_window, text = "",
#         font = ('Helvetica', 20),
#         command = _on_button_pressed)
#
#     button.bind('<Enter>', _on_mouse_entered_button)
#     button.bind('<Leave>', _on_mouse_exited_button)
#
#     button.pack()
#
#     root_window.mainloop()
#     """
#
# if __name__ == '__main__':
#     show_ui()