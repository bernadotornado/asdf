import commands

def main():
    # Print splash screen
    print(r"                                        ") 
    print(r" $$$$$$\   $$$$$$\  $$$$$$$\  $$$$$$$$\ ")
    print(r"$$  __$$\ $$  __$$\ $$  __$$\ $$  _____|")
    print(r"$$ /  $$ |$$ /  \__|$$ |  $$ |$$ |      ")
    print(r"$$$$$$$$ |\$$$$$$\  $$ |  $$ |$$$$$\    ")
    print(r"$$  __$$ | \____$$\ $$ |  $$ |$$  __|  ")
    print(r"$$ |  $$ |$$\   $$ |$$ |  $$ |$$ |      © 2024 Rosoll Johanna")
    print(r"$$ |  $$ |\$$$$$$  |$$$$$$$  |$$ |             Szekely Bernat")
    print(r"\__|  \__| \______/ \_______/ \__|             Axel Dultinger")
    print(r"                                        ")   
    print("Automated    System    for    Dynamic    Finance")   
    print()

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
        commands.call(command[0].upper(), command[1])

# Run the main function
if __name__ == "__main__":
    main()