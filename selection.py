import random

def read_used()->dict:
    words: dict = {"D":[],"O":[]}
    file = open("used.csv","r",encoding="utf-8")
    for line in file:
        sel:list = line.strip().split(":")
        word:dict = {sel[1]:sel[2].strip().split(",")}
        words[sel[0]].append(word)
    file.close()
    return words

def read_words(used:dict,words:dict)->bool:
    file = open("words.csv","r",encoding="utf-8")
    for line in file:
        sel:list = line.strip().split(":")
        if sel[1] not in used[sel[0]]:
            word:dict = {sel[1]:sel[2].strip().split(",")}
            words[sel[0]].append(word)
    file.close()
    if len(words["D"]) == 0:
        return False
    return True

def select_groups(words:dict)->dict:
    file = open("used.csv","a",encoding="utf-8")
    sel:dict = {}
    word:dict = random.choice(words["D"])
    sel.update(word)
    save:tuple = word.popitem()
    file.write(f"D:{save[0]}:{save[1]}\n")
    for i in range(3):
        word:dict = random.choice(words["O"])
        words["O"].remove(word)
        sel.update(word) 
        save:tuple = word.popitem()
        file.write(f"O:{save[0]}:{save[1]}\n")
    file.close()
    return sel

def delete_used():
    file = open("used.csv","w",encoding="utf-8")
    file.close()

def select_words(groups:dict)->dict:
    for key in groups:
        while len(groups[key]) > 4:
            word:str = random.choice(groups[key])
            groups[key].remove(word)
    return groups

def main():
   used:dict = read_used()
   words:dict = {"D":[],"O":[]}
   if read_words(used,words)== False:
       delete_used()
       read_words(used,words)
   selected_groups:dict = select_groups(words)
   selected_words: dict = select_words(selected_groups)
   print(selected_words)

if __name__ == "__main__":
    main()
