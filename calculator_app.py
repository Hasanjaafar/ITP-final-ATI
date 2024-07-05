import tkinter as tk
from tkinter import messagebox
import json
import os

# Define a function to perform arithmetic operations with improved error handling
def calculate(expression) :
    try :
        return eval(expression) #evaluating the arithmetic expresions
    except ZeroDivisionError:
        return "Remember you can't divide by 0" # handling the division by zero
    except SyntaxError:
        return "Error didected"  #handle invalide syntax errors
    except Exception as e :
        return f"Error: {str(e)}" # this for handling any other type of errors such incase

# Save history to file
def save_history(history) :
    with open('history.json', 'w') as file:

        json.dump(history, file)  # for saving the history to the file

# Load history from file
# and loading the history list from a json file
def load_history():
    if os.path.exists('history.json') :

        with open('history.json', 'r') as file :
            return json.load(file) 
    return []

# sort the history with alphabetics by expression
def sort_history(history):
    return sorted(history, key=lambda x: x['expression']) # sort history by the 'expression' key

# Search history for an expression
def search_history(history, query) :
    return [item for item in history if query in item['expression']] #filtering the history for expressions containing the query

# Define the GUI application class
class calculator_app:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.expression=""
        self.history= load_history() #load history from file on startup
        self.input_text = tk.StringVar()  #this is a variable to store the input expression
        self.create_widgets()
        self.root.bind('<Key>', self.key_event) #make the main window respond to the key pressing

    def create_widgets(self):
        input_frame = tk.Frame(self.root) # frame for the input field
        input_frame.pack()
        # input field
        input_field= tk.Entry(input_frame, textvariable=self.input_text, font=('arial', 18, 'bold'), bd=10, insertwidth=4, width=34, borderwidth=8)
        input_field.grid(row=0, column=0)
        button_frame= tk.Frame(self.root) #frame for the buttons
        button_frame.pack()
        # Definning the buttons with texts and colors
        buttons = [
            ('7', 'lightgray'), ('8', 'lightgray'), ('9', 'lightgray'), ('/', 'orange'), ('clear', 'red'),
            ('4', 'lightgray'), ('5', 'lightgray'), ('6', 'lightgray'), ('*', 'orange'), ('history', 'blue'),
            ('1', 'lightgray'), ('2', 'lightgray'), ('3', 'lightgray'), ('-', 'orange'), ('sort', 'green'),
            ('0', 'lightgray'), ('.', 'lightgray'), ('=', 'green'), ('+', 'orange'), ('quit', 'purple')
        ]

        row_val =0
        col_val = 0
        for (text, color) in buttons:
            if col_val > 4:
                col_val= 0
                row_val += 1
            #make a button that uses the on_button_click method
            button= tk.Button(button_frame, text=text, font=('arial', 18, 'bold'), bd=1, padx=20, pady=20, width= 5,bg=color, command=lambda x=text: self.on_button_click(x))
            button.grid(row=row_val, column=col_val)
            col_val += 1

    def on_button_click(self, button):
        if button =="clear":
            self.expression = "" # when pressing on the clear button it clears the expression and so on for the other buttons down
        elif button == "=":
            self.evaluate_expression() #evaluate the expression
        elif button== "history":
            self.show_history() #shows the history
        elif button== "sort":
            self.sort_and_show_history() # sorts and showing history
        elif button == "quit":
            save_history(self.history) # saves the history to file before quitting
            self.root.quit() # closes the application
        else:
            self.expression += button # Append the button text to the expression
        self.input_text.set(self.expression) # update the input field

    def evaluate_expression(self):
        result= calculate(self.expression) #calculate the results
        self.history.append({'expression': self.expression, 'result': result}) #for adding the expression and the results to history
        self.expression = str(result) #update the expression with the result
        self.input_text.set(self.expression) #update the input field

    def show_history(self):
        history_window=tk.Toplevel(self.root) #create a new window for history
        history_window.title("history")
        history_text= tk.Text(history_window, font=('arial', 12)) #text widget to display history
        history_text.pack()

        for item in self.history:
            history_text.insert(tk.END, f"{item['expression']} = {item['result']}\n") #inserting each history item

    def sort_and_show_history(self):
        sorted_history=sort_history(self.history) # Sort history
        history_window=tk.Toplevel(self.root) # Create a new window for sorted history
        history_window.title("sorted history")
        history_text=tk.Text(history_window, font=( 'arial', 12)) # text box to show the sorted history
        history_text.pack()

        for item in sorted_history:
            history_text.insert( tk.END, f"{item['expression']} = {item['result']}\n " ) # to insert each sorted history item

    def key_event(self, event):
        if event.char in '0123456789.+-*/':
            self.expression +=event.char #append the character to the expression
        elif event.keysym== 'Return' or event.char == '=': 
            self.evaluate_expression() # Evaluate the expression when user press Enter or '='
        elif event.keysym== 'BackSpace':
            self.expression= self.expression[:-1] # erase the last character oif he presses the backSpace key
        elif event.keysym== 'Escape':
            self.expression= "" #clearing the expression with esc key
        self.input_text.set( self.expression ) # update the input field

# Main function to run the application
if __name__=="__main__":
    root=tk.Tk() # creating the main window
    app=calculator_app(root) #starts the calculator applicetion
    root.mainloop() #keep the app running in a loops and wait for user to interact
