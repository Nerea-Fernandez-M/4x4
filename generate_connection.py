import random
import database

def check(words):
    """Verificar si hay categorías disponibles"""
    for key in words:
        if len(words[key]) < 1:
            return False
    return True

def select_categories(words):
    """Seleccionar categorías aleatorias y marcarlas como usadas"""
    result = {}
    count = {"D": 1, "O": 3}
    
    for key in words:
        while count[key] > 0:
            sel = random.choice(words[key])
            clave = list(sel.keys())[0]
            text = sel[clave]
            new_data = {clave: text}
            result.update(new_data)
            
            # Guardar en la base de datos como usada
            database.save_used_category(key, clave, text)
            
            count[key] -= 1
    
    return result

def select_words(words):
    """Seleccionar 4 palabras aleatorias de cada categoría"""
    result = {}
    for key in words:
        sel = []
        available_words = words[key].copy()
        
        for i in range(4):
            word = random.choice(available_words)
            available_words.remove(word)
            sel.append(word)
        
        choice = {key: sel}
        result.update(choice)
    
    return result

def generate():
    """Generar un nuevo juego"""
    used = database.read_used()
    words = database.read_words(used)
    val = check(words)
    
    if not val:
        database.clean_used()
        used = database.read_used()
        words = database.read_words(used)
    
    categories = select_categories(words)
    return select_words(categories)

def write(words):
    """Guardar el juego actual en la base de datos"""
    database.save_current_game(words)

def main():
    write(generate())

if __name__ == "__main__":
    main()