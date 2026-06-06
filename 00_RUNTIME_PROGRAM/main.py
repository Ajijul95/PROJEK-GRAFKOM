import tkinter as tk
from ui.app import App


def main():
    root = tk.Tk()
    root.title("Modul Akbar — Generator Peta Kota")
    root.geometry("1280x820")
    root.resizable(True, True)
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
