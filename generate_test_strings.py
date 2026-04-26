from string import ascii_letters
from random import choice

if __name__ == "__main__":
    with open("test_strings.txt", 'w') as file:
        lines = []
        for _ in range(1000):
            lines.append(''.join([choice(ascii_letters) for _ in range(128)]) + '\n')
        file.writelines(lines)