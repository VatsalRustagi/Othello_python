import tkinter
import othello

FONT = ('Arial',16)
BACKGROUND = '#0086b3'

class OthelloGrid:
    def __init__(self,data):
        """
        Initializes the othello board.
        """
        self.rows,self.cols,self.cell_length = data[0],data[1],75
        self.grid = othello.new_game(self.rows,self.cols,data[2],data[3])
        self.decider = data[4]
        self.width,self.height = self.cell_length*self.cols,self.cell_length*self.rows

        #Creating a window to display the game
        self.board = tkinter.Tk()
        self.board.title('Othello FULL')
        self.board.configure(bg = BACKGROUND)

        #Variable Strings
        self.turn_text = tkinter.StringVar()
        self.turn_text.set('TURN : {}'.format(self.grid.get_turn()))
        b,w = self.grid.get_count()
        self.count_text = tkinter.StringVar()
        self.count_text.set('Black: {}\nWhite: {}'.format(b,w))

        #Turn Label
        self.turn_label = tkinter.Label(master = self.board,textvariable = self.turn_text,
                                        font = FONT,fg = 'black', bg = BACKGROUND)
        self.turn_label.grid(row = 0, column = 0,padx = 10, pady = 10)

        #Count Label
        count_label = tkinter.Label(
            master= self.board, textvariable = self.count_text, font = FONT,fg = 'black',
            bg = BACKGROUND
        )
        count_label.grid(row = 0, column = 1,pady = 10,padx =10)

        #Canvas
        self.board_canvas = tkinter.Canvas(
            master=self.board, width = self.width, height = self.height,
            background = BACKGROUND, highlightbackground = 'black'
        )
        self.board_canvas.grid(row = 1,column = 0, columnspan = 2,padx = 5, pady = 5,
                               sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        self.board_canvas.bind('<Configure>', self._canvas_resize)
        self._print_board()
        self.board_canvas.bind('<Button-1>',self._on_click)

        self.board.rowconfigure(0, weight = 1)
        self.board.rowconfigure(1, weight = 1)
        self.board.columnconfigure(0, weight = 1)
        self.board.columnconfigure(1, weight = 1)


    def _print_board(self):
        """
        Prints the othello board, with the turn and count of discs,
        and also deals with the resizing of the window.
        """
        self.wr = self.board_canvas.winfo_width()/self.width    #Width Ratio
        self.hr = self.board_canvas.winfo_height()/self.height  #Height Ratio
        self.board_canvas.delete(tkinter.ALL)
        self._create_board()
        l = self.cell_length
        for i in range(self.grid.rows()):
            for j in range(self.grid.cols()):
                if self.grid._board[i][j] == othello.BLACK:
                    self.board_canvas.create_oval(
                        (j*l+10)*self.wr,(i*l+10)*self.hr,
                        ((j+1)*l-10)*self.wr,((i+1)*l-10)*self.hr,
                        fill = 'black')
                elif self.grid._board[i][j] == othello.WHITE:
                    self.board_canvas.create_oval(
                        (j*l+10)*self.wr,(i*l+10)*self.hr,
                        ((j+1)*l-10)*self.wr,((i+1)*l-10)*self.hr,
                        fill = 'white')
        self.grid.count_discs()

        #Update Count
        b,w = self.grid.get_count()
        self.count_text.set('Black: {}\nWhite: {}'.format(b,w))

        if not self.grid.game_over():
            self.turn_text.set('Turn : {}'.format(self.grid.get_turn()))
            if self.grid.get_turn() == 'W':
                self.turn_label.config(fg = 'white')
            else:
                self.turn_label.config(fg = 'black')

    def _on_click(self,event: tkinter.Event):
        """
        Gets the row and column at the canvas when a user clicks on canvas,
        checks if move can be made, if yes updates the board otherwise ignores
        the click.
        """
        row = int(event.y/(self.cell_length*self.hr))
        col = int(event.x/(self.cell_length*self.wr))
        l = self.cell_length
        try:
            if not (0 <= row < self.rows and 0 <= col < self.cols):
                raise othello.InvalidMoveError()
            othello.make_move(self.grid,row,col)
            if not othello.if_valid_move_exists(self.grid):
                raise othello.NoMoveError()
            self._print_board()
        except othello.InvalidMoveError:
            pass
        except othello.NoMoveError:
            self.grid.skip_turn()
            if not othello.if_valid_move_exists(self.grid):
                self._declare_winner()
            else:
                self._print_board()

    def _declare_winner(self):
        """
        Pops a window declaring the winner, with a quit button.
        """
        self.grid.game_over()
        self._print_board()
        self.turn_text.set('Game Over!')

        self.winner = tkinter.Toplevel()
        self.winner.title("Game Over!")
        self.winner.config(bg = BACKGROUND)

        winner_text = tkinter.StringVar()
        black,white = self.grid.get_count()
        if  black > white and self.decider == '>' or black < white and self.decider == '<':
            winner_text.set('Black Wins!')
        elif black == white:
            winner_text.set("It's a Draw!")
        else:
            winner_text.set('White Wins!')

        winner_label = tkinter.Label(master = self.winner,textvariable = winner_text,
                                        font = ('Arial',20),fg = 'black', bg = BACKGROUND)
        winner_label.grid(row = 0, column = 0,padx = 10, pady = 10)

        quit_button = tkinter.Button(
            master= self.winner, text = "Quit", command = self._quit_app, font = FONT,
            highlightbackground = BACKGROUND
        )
        quit_button.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.winner.rowconfigure(0, weight = 1)
        self.winner.columnconfigure(0, weight = 1)
        self.winner.rowconfigure(1, weight = 1)
        self.winner.grab_set()
        self.winner.wait_window()

    def _quit_app(self):
        """
        Closes the winner and the Othello window.
        """
        self.winner.destroy()
        self.board.destroy()

    def _create_board(self):
        """
        Draws the lines on canvas.
        """
        cl = self.cell_length
        for i in range(self.cols-1):
            self.board_canvas.create_line(cl*self.wr,0,
                                          cl*self.wr,self.height*self.hr)
            cl += self.cell_length
        cl = self.cell_length
        for i in range(self.rows-1):
            self.board_canvas.create_line(0,cl*self.hr,
                                          self.width*self.wr,cl*self.hr)
            cl += self.cell_length

    def _canvas_resize(self,event):
        """
        Resizes the canvas.
        """
        self._print_board()

    def start(self):
        """
        Starts the application.
        """
        self.board.mainloop()

"""
Menu application takes the number of rows and columns for the board. Moreover, takes the first turn, top left disc
and the way the winner will be decided. Once it gets all the data, the window closes and starts the Othello game.
"""
class Menu:
    def __init__(self):
        """
        Initializes the Menu app.
        """
        self.menu_window = tkinter.Tk()
        self.menu_window.title('Othello Menu')
        self.menu_window.config(bg = BACKGROUND)
        self._row_label()
        self._col_label()
        self._turn_label()
        self._corner_label()
        self._decider_label()
        # Done and Cancel Button Frame
        button_frame = tkinter.Frame(master= self.menu_window) #Include the cancel button into this frame
        button_frame.config(bg = BACKGROUND)
        button_frame.grid(
            row = 5, column = 0, columnspan = 2, padx = 10, pady = 10)
        #Done Button
        done_button = tkinter.Button(
            master= button_frame, text = 'Done', font = FONT,
            command = self._done_clicked, bg = BACKGROUND,
            highlightbackground = BACKGROUND
        )
        done_button.grid(row = 0, column = 0, padx = 5, pady = 5)
        #Cancel button
        cancel_button = tkinter.Button(
            master= button_frame, text = 'Cancel', font = FONT,
            command = self._close_window, bg = BACKGROUND,bd = 0,
            highlightbackground = BACKGROUND
        )
        cancel_button.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.menu_window.rowconfigure(0, weight = 1)
        self.menu_window.rowconfigure(1, weight = 1)
        self.menu_window.rowconfigure(2, weight = 1)
        self.menu_window.rowconfigure(3, weight = 1)
        self.menu_window.rowconfigure(4, weight = 1)
        self.menu_window.rowconfigure(5, weight = 1)
        self.menu_window.rowconfigure(6, weight = 1)
        self.menu_window.columnconfigure(0, weight = 1)
        self.menu_window.columnconfigure(1, weight = 1)

    def _row_label(self):
        """
        Creates the row label, and spinbox on the Menu window.
        """
        self._create_label('Select Rows:',0,0)
        self.rows_spinbox = self._create_spinbox(self._get_values())
        self.rows_spinbox.grid(row = 0, column = 1,padx = 5, pady  = 5)

    def _col_label(self):
        """
        Creates the column label, and spinbox on the Menu window.
        """
        self._create_label('Select Columns:',1,0)
        self.cols_spinbox = self._create_spinbox(self._get_values())
        self.cols_spinbox.grid(row = 1, column = 1,padx = 5, pady  = 5)

    def _turn_label(self):
        """
        Creates the turn label, and spinbox on the Menu window.
        """
        self._create_label('First Turn: ',2,0)
        self.turn_spinbox = self._create_spinbox(('B','W'))
        self.turn_spinbox.grid(row = 2,column = 1,padx = 5, pady  = 5)

    def _corner_label(self):
        """
        Creates the top-left label, and spinbox on the Menu window.
        """
        self._create_label('Top Left: ',3,0)
        self.corner_spinbox = self._create_spinbox(('B','W'))
        self.corner_spinbox.grid(row = 3,column = 1,padx = 5, pady  = 5)

    def _decider_label(self):
        """
        Creates the decider label, and spinbox on the Menu window.
        """
        self._create_label('Game won when: ',4,0)
        self.decider_spinbox = self._create_spinbox(('Most discs win','Least discs win'))
        self.decider_spinbox.grid(row = 4, column = 1,padx = 5, pady  = 5)

    def _create_label(self,s,r,c):
        """
        Takes the text to display on the label, the row and column to place align on
        the window and creates a label with the data.
        """
        cols_label = tkinter.Label(
            master= self.menu_window, text = '{}'.format(s), font = FONT, bg = BACKGROUND,
            anchor = tkinter.E,width = 20
        )
        cols_label.grid(row = r, column = c,padx = 5, pady  = 5)

    def _create_spinbox(self,vals: tuple):
        """
        Takes a tuple of values, and returns a spinbox object with those values.
        """
        return tkinter.Spinbox(
            master= self.menu_window, values = vals, wrap = True,
            highlightbackground = BACKGROUND, state = 'readonly'
        )

    def _done_clicked(self):
        """
        Collects the data, kills the Menu window and starts the Othello game
        according to user input.
        """
        if self.decider_spinbox.get() == 'Most discs win':
            decider = '>'
        else:
            decider = '<'
        data = [int(self.rows_spinbox.get()),
                int(self.cols_spinbox.get()),
                self.turn_spinbox.get(),
                self.corner_spinbox.get(),
                decider
                ]
        self._close_window()
        OthelloGrid(data).start()

    def _close_window(self):
        """
        Kills the window.
        """
        self.menu_window.destroy()

    def _get_values(self) -> tuple:
        """
        Creates a tuple of all the even numbers from 2-16 inclusive.
        """
        valid_values = ()
        for i in range(4,17):
            if i%2 == 0:
                valid_values += (i,)
        return valid_values

    def start(self):
        """
        Starts the Menu application.
        """
        self.menu_window.mainloop()

if __name__ == '__main__':
    Menu().start()