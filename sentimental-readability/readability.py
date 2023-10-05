import cs50


def main():

    excerpt = cs50.get_string("Your excerpt: ")

    L = count_letters(excerpt) / count_words(excerpt) * 100

    S = count_sentences(excerpt) / count_words(excerpt) * 100

    index = 0.0588 * L - 0.296 * S - 15.8

    index_rounded = round(index)

    if (index_rounded < 16 and index_rounded > 0):
        print(f"Grade {index_rounded}")

    elif (index_rounded < 1):
        print("Before Grade 1")

    else:
        print("Grade 16+")


def count_letters(excerpt):

    letters = 0

    for i in range(len(excerpt)):
        if str.isalpha(excerpt[i]):
            letters += 1

    return letters


def count_words(excerpt):

    words = 0

    for i in range(len(excerpt)):
        if str.isspace(excerpt[i]):
            words += 1

    return words + 1


def count_sentences(excerpt):

    sentences = 0

    for i in range(len(excerpt)):
        if excerpt[i] == '!' or excerpt[i] == '.' or excerpt[i] == '?':
            sentences += 1

    return sentences


if __name__ == "__main__":
    main()