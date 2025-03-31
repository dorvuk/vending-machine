import datetime
import subprocess

def play_sound(text, voice_path="cr1", output_pho="temp.PHO", output_wav="output.wav"):
    try:
        phoneme_mapping = {
            "a": "a", "b": "b", "c": "ts", "č": "tS", "ć": "tS'", "d": "d", "đ": "dZ'",
            "e": "e", "f": "f", "g": "g", "h": "x", "i": "i", "j": "j", "k": "k",
            "l": "l", "m": "m", "n": "n", "o": "o", "p": "p", "r": "r", "s": "s",
            "š": "S", "t": "t", "u": "u", "v": "v", "z": "z", "ž": "Z", "_": "_"
        }

        previous_phoneme = None
        with open(output_pho, "w") as pho_file:
            pho_file.write(";;T=1.5\n")
            pho_file.write("_ 50\n")  
            for word in text.split():  
                for char in word.lower():
                    if char in phoneme_mapping:
                        phoneme = phoneme_mapping[char]
                        if phoneme != previous_phoneme:  
                            pho_file.write(f"{phoneme} 50\n")
                            previous_phoneme = phoneme
                pho_file.write("_ 50\n")  
            pho_file.write("_ 50\n")  

        subprocess.run(["mbrola", voice_path, output_pho, output_wav], check=True)
        subprocess.run(["afplay", output_wav], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] MBROLA failed: {e}")
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

number_mapping = {
    0: "nula",
    1: "jedan",
    2: "dva",
    3: "tri",
    4: "četiri",
    5: "pet",
    6: "šest",
    7: "sedam",
    8: "osam",
    9: "devet",
    10: "deset",
    11: "jedanaest",
    12: "dvanaest",
    13: "trinaest",
    14: "četrnaest",
    15: "petnaest",
    16: "šesnaest",
    17: "sedamnaest",
    18: "osamnaest",
    19: "devetnaest",
    20: "dvadeset",
    30: "trideset",
    40: "četrdeset",
    50: "pedeset",
    60: "šezdeset",
    70: "sedamdeset",
    80: "osamdeset",
    90: "devedeset"
}

def number_to_word_form(num, singular, dual, plural):
    if num == 1 or (num % 10 == 1 and num > 20):
        return singular
    elif (2 <= num <= 4) or ((2 <= num % 10 <= 4) and num > 20):
        return dual
    else:
        return plural

def construct_number(num):
    if num <= 19 or num % 10 == 0:
        return number_mapping[num]
    else:
        tens = (num // 10) * 10
        ones = num % 10
        return f"{number_mapping[tens]} {number_mapping[ones]}"

def greeting():
    now = datetime.datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        play_sound("Dobro jutro!")
        print("\nDobro jutro!")
    elif 12 <= hour < 18:
        play_sound("Dobar dan!")
        print("\nDobar dan!")
    else:
        play_sound("Dobra večer!")
        print("\nDobra večer!")

def read_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    hour_word = number_to_word_form(hour, "sat", "sata", "sati")
    hour_text = construct_number(hour)
    play_sound(f"Sada je {hour_text} {hour_word}")

    if minute != 0:
        minute_word = number_to_word_form(minute, "minuta", "minute", "minuta")

        if minute % 10 == 1 and minute != 11:
            minute_text = "jedna"
        elif minute % 10 == 2 and minute != 12:
            minute_text = "dvije"
        else:
            minute_text = construct_number(minute)

        play_sound(f"i {minute_text} {minute_word}")
    print(f"Sada je {hour} {hour_word} i {minute} {minute_word}.\n")

def read_price(euros, cents):
    if euros != 0:
        euro_word = number_to_word_form(euros, "euro", "eura", "eura")
        euro_text = construct_number(euros)
        play_sound(f"{euro_text} {euro_word}")
    if euros != 0 and cents != 0:
        play_sound(" i ")
    if cents != 0:
        cent_word = number_to_word_form(cents, "cent", "centa", "centi")
        cent_text = construct_number(cents)
        play_sound(f"{cent_text} {cent_word}")

def vending_machine():
    prices = {
        "specijalno": {
            "1": ("Astronautska juha", 1.50),
            "2": ("Sendvič", 2.20),
            "3": ("Voćna salata", 1.80),
            "4": ("Senf", 0.50),
            "5": ("Kečap", 0.50),
            "6": ("Majoneza", 0.60),
        },
        "slatko": {
            "1": ("Puding od čokolade", 1.00),
            "2": ("Protein bar", 1.20),
            "3": ("Krafna", 0.80),
            "4": ("Čokoladni keksi", 1.50),
        },
        "slano": {
            "1": ("Lays", 1.20),
            "2": ("Slani kikiriki", 1.00),
            "3": ("Kokice", 0.80),
            "4": ("Čips sa sirom", 1.50),
            "5": ("Tortilja čips", 1.40),
        },
        "piće": {
            "1": ("Kava", 1.00),
            "2": ("Soy mlijeko", 1.20),
            "3": ("Sok od naranče", 1.50),
            "4": ("Coca-cola", 1.00),
            "5": ("Voda", 0.50),
            "6": ("Čokoladno mlijeko", 1.20),
            "7": ("Monster", 2.00),
            "8": ("Iso Sport", 1.80),
            "9": ("Ledeni čaj", 1.50),
        },
    }
    total_cost = 0
    greeting()
    read_time()
    while True:
        play_sound("Odaberite kategoriju: Specijalno, Slatko, Slano ili Piće.")
        print("Odaberite kategoriju: Specijalno, Slatko, Slano ili Piće.\n")
        category = input("Vaš odabir: ").strip().lower()
        if category in prices:
            play_sound(category)
            for key, (product, price) in prices[category].items():
                play_sound(product)

            print(f"\n{category.capitalize()}:\n")
            for key, (product, price) in prices[category].items():
                print(f"{key}. {product} - {price:.2f} EUR")
            print("")

            play_sound("Odaberite broj proizvoda")
            choice = input("Odaberite broj proizvoda: ").strip()
            if choice in prices[category]:
                _, price = prices[category][choice]
                total_cost += price
                play_sound(f"Odabrali ste proizvod broj {construct_number(int(choice))}.")
                print(f"\nOdabrali ste proizvod broj {choice}.\n")
            else:
                play_sound("Neispravan unos. Pokušajte ponovno.")
                print("\nNeispravan unos. Pokušajte ponovno.\n")
                continue
        else:
            play_sound("Neispravan odabir. Pokušajte ponovno.")
            print("\nNeispravan odabir. Pokušajte ponovno.\n")
            continue
        play_sound("Želite li još nešto?")
        another = input("Želite li još nešto? da/ne: ").strip().lower()
        if another != "da":
            break
    euros_total = int(total_cost)
    cents_total = int(round((total_cost - euros_total) * 100))
    print(f"\nUkupni trošak: {total_cost:.2f} EUR.\n")
    play_sound(f"Ukupni trošak je") 
    read_price(euros_total, cents_total)
    play_sound("Odaberite način plaćanja: Gotovina, Kartica, Mobitel.")
    print("Odaberite način plaćanja: Gotovina, Kartica, Mobitel")
    
    while True:
        placanje = input("Vaš odabir: ")
        if placanje.strip().lower() == "gotovina":
            play_sound("Unesite novčanice i kovanice.")
            print("\nUnesite novčanice i kovanice.")
            break
        elif placanje.strip().lower() in ["kartica", "mobitel"]:
            play_sound("Prislonite karticu ili mobilni uređaj.")
            print("\nPrislonite karticu ili mobilni uređaj.")
            break
        else:
            play_sound("Neispravan odabir. Pokušajte ponovno.")
            print("\nNeispravan odabir. Pokušajte ponovno.\n")
            continue
    input()
    play_sound("Hvala i doviđenja!")
    print("Hvala i doviđenja!\n")

if __name__ == "__main__":
    vending_machine()