from colored import Fore, Style

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

    sandwiches: dict = {
        "chicken": 5.25,
        "beef": 6.25,
        "tofu": 5.75
    }

    while True:

        print("    (Chicken $5.25, Beef $6.25, Tofu $5.75)")
        choice: str = input("    Choose a sandwich: ")

        if choice.lower() in sandwiches.keys():
            print(f"\n    You chose a {choice} sandwich!")
            break
        else:
            print(f"\n{Fore.red}    Invalid input (check your spelling)!{Style.reset}\n")

if __name__ == "__main__":
    main()