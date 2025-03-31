import datetime
from playsound import playsound

def play_sound(file):
    try:
        playsound(f"sound/{file}")
    except Exception:
        print(f"[SOUND ERROR: {file}]")

def number_to_word_form(num, singular, dual, plural):
    if num == 1 or (num%10 == 1 and num>20):
        return singular
    elif (2 <= num <= 4) or ((2 <= num%10 <= 4) and num>20):
        return dual
    else:
        return plural

def construct_number(num):
    if num <= 19 or num % 10 == 0:
        return [f"{num}.mp3"]
    else:
        tens = (num // 10) * 10
        ones = num % 10
        return [f"{tens}.mp3", f"{ones}.mp3"]

def greeting():
    now = datetime.datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        play_sound("dobro_jutro.mp3")
        print("\nDobro jutro!")
    elif 12 <= hour < 18:
        play_sound("dobar_dan.mp3")
        print("\nDobar dan!")
    else:
        play_sound("dobra_vecer.mp3")
        print("\nDobra večer!")

def read_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    hour_word = number_to_word_form(hour, "sat", "sata", "sati")
    play_sound("sada_je.mp3")
    print("\nSada je", end=" ")
    for voice in construct_number(hour):
        play_sound(voice)
    play_sound(f"hour_{hour_word}.mp3")
    print(f"{hour} {hour_word}", end="")

    if minute != 0:
        minute_word = number_to_word_form(minute, "minuta", "minute", "minuta")
        play_sound("i.mp3")
        print(" i", end=" ")
        for voice in construct_number(minute):
            if int(voice.split('.')[0]) % 10 == 1 and int(voice.split('.')[0]) != 11:
                play_sound("jedna.mp3")
            elif int(voice.split('.')[0]) % 10 == 2 and int(voice.split('.')[0]) != 12:
                play_sound("dvije.mp3")
            else:
                play_sound(voice)
        play_sound(f"minute_{minute_word}.mp3")
        print(f"{minute} {minute_word}\n")


def read_price(euros, cents):
    if euros != 0:
        euro_word = number_to_word_form(euros, "euro", "eura", "eura")
        for voice in construct_number(euros):
            play_sound(voice)
        play_sound(f"euros_{euro_word}.mp3")

    if cents != 0:
        cent_word = number_to_word_form(cents, "cent", "centa", "centi")
        for voice in construct_number(cents):
            play_sound(voice)
        play_sound(f"cents_{cent_word}.mp3")

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
            "5": ("Voda 0.5L", 0.50),
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
        play_sound("navigacija.mp3")
        print("Odaberite kategoriju: Specijalno, Slatko, Slano ili Piće.\n")
        category = input("Vaš odabir: ").strip().lower()

        if category in prices:
            play_sound(f"{category}.mp3")
            print(f"\n{category.capitalize()}:\n")
            for key, (product, price) in prices[category].items():
                print(f"{key}. {product} - {price:.2f} EUR")
            print("")
            play_sound("br_proizvoda.mp3")
            choice = input("Odaberite broj proizvoda: ").strip()
            if choice in prices[category]:
                _, price = prices[category][choice]
                total_cost += price
                play_sound("potvrda_odabira.mp3")
                play_sound(f"{choice}.mp3")
                print(f"\nOdabrali ste proizvod broj {choice}.\n")
            else:
                play_sound("pogresan_unos.mp3")
                print("\nNeispravan unos. Pokušajte ponovno.\n")
                continue
        else:
            play_sound("pogresan_unos.mp3")
            print("\nNeispravan odabir. Pokušajte ponovno.\n")
            continue

        play_sound("jos_nesto.mp3")
        another = input("Želite li još nešto? da/ne: ").strip().lower()
        if another != "da":
            break

    euros_total = int(total_cost)
    cents_total = int(round((total_cost - euros_total) * 100))
    print(f"\nUkupni trošak: {total_cost:.2f} EUR.\n")
    play_sound("ukupni_trosak.mp3")
    read_price(euros_total, cents_total)

    play_sound("nacin_placanja.mp3")
    print("Odaberite način plaćanja: Gotovina, Kartica, Mobitel")
    placanje = input("Vaš odabir: ")

    while True:
        if placanje.strip().lower() == "gotovina":
            play_sound("gotovina.mp3")
            print("\nUnesite novčanice i kovanice.")
            break
        elif placanje.strip().lower() == "kartica" or placanje.strip().lower() == "mobitel":
            play_sound("kartica.mp3")
            print("\nPrislonite karticu ili mobilni uređaj.")
            break
        else:
            play_sound("pogresan_unos.mp3")
            print("\nNeispravan odabir. Pokušajte ponovno.\n")
            continue

    input()
    play_sound("hvala_dovidenja.mp3")
    print("Hvala i doviđenja!\n")

if __name__ == "__main__":
    vending_machine()