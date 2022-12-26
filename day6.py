def read_day6_file() -> str:
    with open("inputs/day6.txt", mode="r+", encoding="utf-8") as f:
        return f.read().strip()

def day6():
    buffer = read_day6_file()

    # Start of Packet
    for i in range(3,len(buffer)):
        if len(set(buffer[i-3:i+1])) == 4:
            print(i+1)
            break

    # Start of Message
    for i in range(13,len(buffer)):
        if len(set(buffer[i-13:i+1])) == 14:
            print(i+1)
            break

if __name__ == "__main__":
    day6()