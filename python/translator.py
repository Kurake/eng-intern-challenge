import sys

alphabet = {
    "a":"O.....",
    "b":"O.O...",
    "c":"OO....",
    "d":"OO.O..",
    "e":"O..O..",
    "f":"OOO...",
    "g":"OOOO..",
    "h":"O.OO..",
    "i":".OO...",
    "j":".OOO..",
    "k":"O...O.",
    "l":"O.O.O.",
    "m":"OO..O.",
    "n":"OO.OO.",
    "o":"O..OO.",
    "p":"OOO.O.",
    "q":"OOOOO.",
    "r":"O.OOO.",
    "s":".OO.O.",
    "t":".OOOO.",
    "u":"O...OO",
    "v":"O.O.OO",
    "w":".OOO.O",
    "x":"OO..OO",
    "y":"OO.OOO",
    "z":"O..OOO"
}

numbers = {
    "1":"O.....",
    "2":"O.O...",
    "3":"OO....",
    "4":"OO.O..",
    "5":"O..O..",
    "6":"OOO...",
    "7":"OOOO..",
    "8":"O.OO..",
    "9":".OO...",
    "0":".OOO.."
}

special = {
    "cap":".....O",
    "dec":".O...O",
    "num":".O.OOO",
    "rig":"OOOOOO",
    ".":"..OO.O",
    ",":"..O...",
    "?":"..O.OO",
    "!":"..OOO.",
    ":":"..OO..",
    ";":"..O.O.",
    "-":"....OO",
    "/":".O..O.",
    "<":".OO..O",
    ">":"O..OO.",
    "(":"O.O..O",
    ")":".O.OO.",
    " ":"......"
}


# o and > are identical, braille wise
# Assuming paired, that is, a '<' implies a '>' when converting braille to English


def conBraille(input):
    # It's English, convert to Braille
    output = ""
    numFlag = 0
    for x in input:
        char = ord(x)
        if numFlag:
            if(char > 47 and char < 58):
                # Number, add number
                output += numbers.get(chr(char))
            elif(char == 32):
                # Space key, add space, turn off num mode
                output += special.get(chr(char))
                numFlag = 0
            elif(char == 46):
                # Period, rather, decimal
                output += special.get(chr(char))
            else: 
                # Not a number nor a space or a period
                # continue because this case wasn't covered in requirements
                numFlag = 0
                if(char > 64 and char < 91):
                    output += special.get("cap")
                    output += alphabet.get(chr(char + 32))
                elif(char > 96 and char < 123):
                    output += alphabet.get(chr(char))
                elif(chr(char) in special.keys()):
                    output += special.get(chr(char))
                else:
                    # Not a recognized character
                    print("Error, unrecognized character")
                    return 0
        elif(char > 64 and char < 91):
            # Capital letter, add cap follows then switch char to lowercase and add it
            output += special.get("cap")
            output += alphabet.get(chr(char + 32))
        elif(char > 96 and char < 123):
            # Lower case letter, add it
            output += alphabet.get(chr(char))
        elif(char > 47 and char < 58):
            # Number, add num follows then add number, switch to number processing
            output += special.get("num")
            output += numbers.get(chr(char))
            numFlag = 1
        elif(chr(char) in special.keys()):
            # If char in special keys, then add that too
            # If right pointed bracket, add right pointed bracket follows
            if (chr(char) == ">"):
                output += "OOOOOO"
            output += special.get(chr(char))
    return output


def interpret(input):
    # Assume braille until proven wrong - braille string must be length multiple of 6
    if len(input) % 6 != 0:
        # Must be english, convert to braille
        print(conBraille(input))
        return 0
    # Otherwise, move on and interpret each group of six characters as one braille character
    output = ""
    capFlag = 0
    decFlag = 0
    numFlag = 0
    leftCount = 0
    for y in range(0, int(len(input)/6)):
        char = input[6*y:6*(y+1)]
        if (char in special.values()):
            if(char == "O..OO."):
                # Could be o, could be >, assume o, then replace o's from the back equal to leftcount
                output += "o"
                continue

            char = list(special.keys())[list(special.values()).index(char)]
            if char == "cap":
                if capFlag or numFlag:
                    # Should not have two consecutive cap commands or capitalizing in a number
                    # Not valid braille, hence English
                    print(conBraille(input))
                    return 0
                capFlag = 1
                continue
            elif char == "num":
                if capFlag or numFlag:
                    # Should not have two consecutive num commands or capitalizing a num command
                    # Not valid braille, hence English
                    print(conBraille(input))
                    return 0
                numFlag = 1
                continue
            elif char == "dec":
                if capFlag or not numFlag:
                    # Cannot capitalize a command, should only decimal in a number.
                    # Not valid braille, hence English
                    print(conBraille(input))
                    return 0
                decFlag = 1
                continue
            else:
                if char == "<":
                    leftCount += 1
                output += char
        elif numFlag == 0:
            # Not looking for a number, must be alphabet
            if (char in alphabet.values()):
                char = list(alphabet.keys())[list(alphabet.values()).index(char)]
                if capFlag:
                    output += char.capitalize()
                    capFlag = 0
                else:
                    output += char
            else:
                # Not in the alphabet therefore it's not valid braille
                # Convert to braille
                print(conBraille(input))
                return 0
        else:
            # Looking for a number, or a decimal if decFlag
            if decFlag:
                # Next character should be a period. If not, invalid braille
                if char == "..OO.O":
                    output += "."
                else:
                    print(conBraille(input))
                    return 0
            # If no decimal flag, then either space or number
            elif (char in numbers.values()):
                char = list(numbers.keys())[list(numbers.values()).index(char)]
                output += char
            elif char == "......":
                # Space, add a space, switch off numFlag
                output += " "
                numFlag = 0
            else:
                # invalid braille, convert to braille
                print(conBraille(input))
                return 0
    if leftCount > 0:
        reversed = output[::-1]
        reversed.replace("o", ">", leftCount)
        output = reversed[::-1]
    print(output)
    return 0


inputs = sys.argv[1:]
inputString = " ".join(inputs)
interpret(inputString)
