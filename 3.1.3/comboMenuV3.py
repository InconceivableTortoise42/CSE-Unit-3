from colored import Fore, Style
import os

def clear() -> None:
    if os.name == 'nt':
        _ = os.system('cls') 
    else:
        _ = os.system('clear') 

def banner() -> None:
    print(f'''{Fore.green}
     _____           _       _     _              
    |   __|___ ___ _| |_ _ _|_|___| |_            
    |__   | .'|   | . | | | | |  _|   |           
    |_____|__,|_|_|___|_____|_|___|_|_|           
     _____ _                          ___     ___ 
    |     | |_ ___ ___ ___ ___ ___   |_  |   |   |
    |   --|   | . | . |_ -| -_|  _|   _| |_ _| | |
    |_____|_|_|___|___|___|___|_|    |_____|_|___|

    {Style.reset}''')

def main() -> None:
    banner() 

    beverage: str = None
    fries: str = None
    sandwich: str = None
    total: float = 0.0

    sandwiches: dict = {
        "chicken": 5.25,
        "beef": 6.25,
        "tofu": 5.75
    }

    beverageSize: dict = {
        "small": 1.00,
        "medium": 1.75,
        "large": 2.25
    }

    friesSizes: dict = {
        "small": 1.00,
        "medium": 1.50,
        "large": 2.00
    }

    # Sandwich prompt

    while True:

        print("    (Chicken $5.25, Beef $6.25, Tofu $5.75)")
        choice: str = input("    Choose a sandwich: ")

        if choice.lower() in sandwiches.keys():
            print(f"\n    You chose a {choice} sandwich!")
            sandwich = choice
            total += sandwiches[sandwich]
            break
        else:
            print(f"\n{Fore.red}    Invalid input (check your spelling)!{Style.reset}\n")

    
    clear()
    banner()
    # Beverage prompt

    choice: str = input("\n    Would you like a beverage? (y, N): ")
    print()

    if choice == "y":
        while True:

            print("    (Small $1.00, Medium $1.75, Large $2.25)")
            choice: str = input("    Choose a size: ")

            if choice.lower() in beverageSize.keys():
                print(f"\n    You chose a {choice} drink!")
                beverage = choice
                total += beverageSize[beverage]
                break
            else:
                print(f"\n{Fore.red}    Invalid input (check your spelling)!{Style.reset}\n")

    clear()
    banner()
    # Fries prompt

    choice: str = input("\n    Would you like fries? (y, N): ")
    print()

    if choice == "y":
        while True:

            print("    (Small $1.00, Medium $1.50, Large $2.00)")
            choice: str = input("    Choose a size: ")

            if choice.lower() in friesSizes.keys():
                print(f"\n    You chose a {choice} fries!")
                fries = choice
                total += friesSizes[fries]
                break
            else:
                print(f"\n{Fore.red}    Invalid input (check your spelling)!{Style.reset}\n")

    if fries == "small":
        choice: str = input("\n    Would you like to Mega-Size your fries? (y, N): ")
        if choice == "y":
            fries = "large"

    # Order Summary

    clear()
    banner()
    print("    " + 40 * "-")
    print()
    print("    Order Summary:")
    print(f"    Beverage: {beverage + f' - ${beverageSize[beverage]:.2f}' if beverage else 'None'}")
    print(f"    Fries: {fries + f' - ${friesSizes[fries]:.2f}' if fries else 'None'}")
    print(f"    Sandwich: {sandwich} - ${sandwiches[sandwich]:.2f}")
    print(f"    Total: ${total:.2f}")

    input("\n    Press enter to quit...")

if __name__ == "__main__":
    main()