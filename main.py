def get_dictionary(filename):
    dictionary = {}
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if "=" not in line:
                continue
            word, translation = line.split("=", 1)
            dictionary[word] = translation
    return dictionary

def choose_language(current=None):
    print("Choose a language pair / Scegli una coppia di lingue:")
    print("1. English → Italian / Inglese → Italiano")
    print("2. Italian → English / Italiano → Inglese")
    while True:
        choice = input("Pick 1 or 2 / Scegli 1 o 2: ").strip()
        if choice == "-c" and current:  # Change language
            return "ital-eng.txt" if current == "eng-ital.txt" else "eng-ital.txt"
        if choice == "1":
            return "eng-ital.txt"
        elif choice == "2":
            return "ital-eng.txt"
        else:
            print("Invalid choice, try again / Scelta non valida, riprova.")

def translator():
    print("Hi! This is a simple translator / Ciao! Questo è un traduttore semplice ")
    
    filename = choose_language()
    while True:
        dictionary = get_dictionary(filename)
        dictionary_lower = {k.lower(): v for k, v in dictionary.items()}

        phrase = input("\nEnter a word or phrase (type '-c' to change language) / Inserisci una parola o frase: ").strip()
        
        if phrase.lower() == "-c":
            filename = choose_language(current=filename)
            print("Language changed! / Lingua cambiata!")
            continue

        phrase_lower = phrase.lower()
        if phrase_lower in dictionary_lower:
            print(f"Translation / Traduzione: {dictionary_lower[phrase_lower]}")
        else:
            print(f"Sorry, '{phrase}' is not in the dictionary / Sfortunatamente '{phrase}' non è presente nel dizionario")

if __name__ == "__main__":
    translator()
