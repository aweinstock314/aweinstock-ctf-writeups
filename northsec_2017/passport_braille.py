#!/usr/bin/env python
import sys

# https://en.wikipedia.org/wiki/French_Braille
french = {
        " ": "",
        u"\u2820 \u282e": u"\u00c9",
        u"\u2820 \u2817": "R",
        u"\u2820 \u280f": "P",
        u"\u2820 \u281b": "G",

        u"\u2818 \u280e": "$",

        u"\u2820": "",
        u"\u2801": "a",
        u"\u2803": "b",
        u"\u2809": "c",
        u"\u2819": "d",
        u"\u2811": "e",
        u"\u280b": "f",
        u"\u281b": "g",
        u"\u2813": "h",
        u"\u280a": "i",
        u"\u281a": "j",
        u"\u2805": "k",
        u"\u2807": "l",
        u"\u280D": "m",
        u"\u281D": "n",
        u"\u2815": "o",
        u"\u280f": "p",
        u"\u281f": "q",
        u"\u2817": "r",
        u"\u280E": "s",
        u"\u281E": "t",

        u"\u2825": "u",
        u"\u2827": "v",
        u"\u282D": "x",
        u"\u283D": "y",
        u"\u2835": "z",
        u"\u282f": "ç",
        u"\u283f": "é",
        u"\u2837": "à",
        u"\u282e": "è",
        u"\u283e": "ù",
        u"\u2821": "â",
        u"\u2823": "ê",
        u"\u2829": "î",
        u"\u2839": "ô",
        u"\u2831": "û",
        u"\u282b": "ë",
        u"\u283b": "ï",
        u"\u2833": "ü",
        u"\u282a": "œ",
        u"\u283a": "w",

        u"\u2832": ".",
        u"\u2812": ":",
        u"\u280c": u"\u00ec",
        }
'''
print("French mapping:")
for (k,v) in french.items():
    print("\t%s -> %s" % (k, v))
'''

# https://en.wikipedia.org/wiki/English_Braille
english = {
        " ": "",
        u"\u2820 \u282e": u"\u00c9",
        u"\u2820 \u2801": "A",
        u"\u2820 \u2817": "R",
        u"\u2820 \u280f": "P",
        u"\u2820 \u281b": "G",

        u"\u2818 \u280e": "$",

        u"\u2820": "",
        u"\u2801": "a",
        u"\u2803": "b",
        u"\u2809": "c",
        u"\u2819": "d",
        u"\u2811": "e",
        u"\u280b": "f",
        u"\u281b": "g",
        u"\u2813": "h",
        u"\u280a": "i",
        u"\u281a": "j",
        u"\u2805": "k",
        u"\u2807": "l",
        u"\u280D": "m",
        u"\u281D": "n",
        u"\u2815": "o",
        u"\u280f": "p",
        u"\u281f": "q",
        u"\u2817": "r",
        u"\u280E": "s",
        u"\u281E": "t",

        u"\u2825": "u",
        u"\u2827": "v",
        u"\u282D": "x",
        u"\u283D": "y",
        u"\u2835": "z",
        u"\u282f": "ç",
        u"\u283f": "é",
        u"\u2837": "of",
        u"\u2820 \u282e": "The",
        u"\u282e": "the",
        u"\u283e": "ù",
        u"\u2821": "â",
        u"\u2823": "ê",
        u"\u2829": "î",
        u"\u2839": "ô",
        u"\u2831": "û",
        u"\u282b": "ë",
        u"\u283b": "ï",
        u"\u2833": "ü",
        u"\u282a": "œ",
        u"\u283a": "w",

        u"\u2832": ".",
        u"\u2812": "-cc-",
        u"\u280c": "st",
        u"\u2814": "in",

        # https://en.wikipedia.org/wiki/English_Braille#Abbreviations
        u"\u2818 \u283a": "word",
        }


#lines = [u"\u2820 \u282e   \u280e \u2811 \u2812 \u2819   \u2813 \u2801 \u2807 \u280b   \u2837   \u282e   \u280b \u2807 \u2801 \u281b   \u280a \u280e   \u282e   \u2818 \u283a"]
lines = [[u"\u2820 \u282e", u"\u280e \u2811 \u2812 \u2819", u"\u2813 \u2801 \u2807 \u280b", u"\u2837", u"\u282e", u"\u280b \u2807 \u2801 \u281b", u"\u280a \u280e", u"\u282e", u"\u2818 \u283a"],
         [u"\u2820 \u280f \u2807 \u2801 \u281e \u283d \u280f \u2825 \u280e \u2832", u"\u280c \u2819 \u2819", u"\u282d", u"\u2808 \u280b", u"\u280f", u"\u280b \u280c", u"\u2813 \u2801 \u2807 \u280b", u"\u281e \u2815"],
         [u"\u2815 \u2803 \u281e \u2801 \u2814", u"\u2801", u"\u2809 \u2815 \u280d \u280f \u2807 \u2811 \u281e \u2811", u"\u280b \u2807 \u2801 \u281b \u2832", u"\u2820 \u281b \u2807 \u2815 \u2817 \u283d", u"\u281e \u2815"],
         [u"\u2820 \u2820 \u2817 \u2801 \u2815"]]

lines[1][1] = "\u2820 \u2801 \u2819 \u2819" # correction
print("Braille thingies from the passport:")
for line in lines:
    for word in line:
        sys.stdout.write(word + " "*3)
    sys.stdout.write("\n")

for line in lines:
    for word in line:
        for (k,v) in sorted(english.items(), key=lambda x:len(x[0]), reverse=True):
            word = word.replace(k, v)
        sys.stdout.write(word + " ")
    sys.stdout.write("\n")

'''
The se-cc-d half of the flag is the word
Platypus. Add x ⠈f p fst half to
obtain a complete flag. Glory to
Rao
'''
