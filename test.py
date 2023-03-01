import numpy as np 
size=int(1e7)

floats = np.random.uniform(size=size)
sum1= floats.sum()
nums1 = set(floats)
np.random.shuffle(floats)

sum2= floats.sum()

print(sum1 == sum2)
print(f"{sum1}\n{sum2}")

nums2 = set(floats)
print(nums1 == nums2)
# Given a nested list with arbitrary level of nesting, write a function, flatten to flatten it.

# sample input:
# x = [[4,5],[[1,2,3]],6]

# flatten(x) --> [4,5,1,2,3,6]

# Use: https://www.online-python.com or any IDE you have.
# def flattenList(x):
#     res = []
#     for element in x:
#         if type(element) is list:
#             res.extend(flattenList(element))
#         else:
#             res.append(element)
#     return res   

# x = [[4,5],[[1,2,3]],6]
# print(flattenList(x))
# x is a string representing a book of text. The pages are separatd by \b. The lines by \n. 

# Write a function that reverses the
# - order of pages
# - order of lines in each page
# - order of words in each line
# - don't reverse the characters in each word

# Sample string:
# x="the brown fox jumped over the fence\nthe brown bear fell down the hill\n\bThe big lion chased the deer\nThe monkey ate the bananas\n\b"
# expected=""


# Use: https://www.online-python.com

def reverse(str):
    # one line code as you mentioned with list comprehension operation
    # res = "\b".join(["\n".join([" ".join([word for word in line.split(" ")[::-1]]) for line in page.split("\n")[::-1]]) for page in str.split("\b")[::-1]])
    pages = str.split("\b")
    pages = pages[::-1]
    res = ""
    for page in pages:
        lines = page.split("\n")
        lines = lines[::-1]
        for line in lines:
            words = line.split(" ")
            words = words[::-1]
            res += " ".join(words)
            res += "\n"
        res += "\b"
    return res

x="the brown fox jumped over the fence\nthe brown bear fell down the hill\n\bThe big lion chased the deer\nThe monkey ate the bananas\n\b"

# x="The big lion chased the deer\nThe monkey ate the bananas\n\bthe brown fox jumped over the fence\nthe brown bear fell down the hill\n\b"
# x="The monkey ate the bananas\nThe big lion chased the deer\n\bthe brown bear fell down the hill\nthe brown fox jumped over the fence\n\b"
print(reverse(x))
