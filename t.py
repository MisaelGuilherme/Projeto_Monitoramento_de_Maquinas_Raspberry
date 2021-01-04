from tkinter import *

jane = Tk()
# Resolução do Sistema
largura_screen = jane.winfo_screenwidth()
altura_screen = jane.winfo_screenheight()

print(f'Lagura da tela: {largura_screen}')
print(f'Altura da tela: {altura_screen}')
end = input()

jane.mainloop()
