import database

def read():
    """Leer el juego actual desde la base de datos"""
    return database.read_current_game()

def main():
    choices = read()
    print(choices)

if __name__ == "__main__":
    main()