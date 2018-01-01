#import syllables

str = input("Enter a paragraph: ")
words = str.split()
sentence = 0

for word in words:
    if(word.endswith(".")):
        sentence += 1

print (sentence)