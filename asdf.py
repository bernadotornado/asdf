import commands
import hash

def main():
    # Print splash screen
    print() 
    print(r" $$$$$$\   $$$$$$\  $$$$$$$\  $$$$$$$$\ ")
    print(r"$$  __$$\ $$  __$$\ $$  __$$\ $$  _____|")
    print(r"$$ /  $$ |$$ /  \__|$$ |  $$ |$$ |      ")
    print(r"$$$$$$$$ |\$$$$$$\  $$ |  $$ |$$$$$\    ")
    print(r"$$  __$$ | \____$$\ $$ |  $$ |$$  __|   ")
    print(r"$$ |  $$ |$$\   $$ |$$ |  $$ |$$ |      © 2024 Rosoll Johanna")
    print(r"$$ |  $$ |\$$$$$$  |$$$$$$$  |$$ |             Szekely Bernat")
    print(r"\__|  \__| \______/ \_______/ \__|             Axel Dultinger")
    print()   
    print("Automated    System    for    Dynamic    Finance")   
    print()
    stock_registry = hash.StockRegistry()
    # Main loop
    while True:
        # Get the command
        print("Commands: ADD, DEL, IMPORT, SEARCH, PLOT, SAVE, LOAD, QUIT")
        command = input("Enter a command: ").split()

        # Handle qutting the program
        if command[0].upper() == "QUIT":
             commands.QUIT()

        # Handle missing arguments
        if(len (command) < 2):
            commands.ERROR("Missing argument")
            continue

        # Call the command
        commands.call(stock_registry, command[0].upper(), command[1:])

# Run the main function
if __name__ == "__main__":
    main()