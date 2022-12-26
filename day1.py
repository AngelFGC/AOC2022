def day1():
    elf_calories = []

    with open("inputs/day1.txt", mode="r+", encoding="utf-8") as f:
        full_text = f.read()
        elf_texts = full_text.split("\n\n")
        elf_calories = [sum(int(cals) for cals in elf.split()) for elf in elf_texts]
    
    elf_calories.sort()
    print(elf_calories[-1])
    print(sum(elf_calories[-3:]))

if __name__ == "__main__":
    day1()