
def main() -> None:
    x = input("What is your name? ") 
    y = input("What is your age? ")

    print(type(x))
    print(type(y))

    print(f"Hello {x}")
    print(f"You are {y} years old")

if __name__ == "__main__":
    main()