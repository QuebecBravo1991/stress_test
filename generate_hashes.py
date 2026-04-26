from hashlib import sha256

if __name__ == "__main__":
    with open("test_strings.txt", 'r') as file:
        lines = file.readlines()

    with open('hashes.txt', 'w') as file:
        for line in lines:
            print(line.strip('\n'))
            file.write(sha256(line.strip('\n').encode('utf-8')).hexdigest() + "\n")