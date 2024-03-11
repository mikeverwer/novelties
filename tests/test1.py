my_list = [
    "1•1•1•1•2•2",
    "1•2•2•1•2•2",
    "1•4•1•4",
    "14•14",
    "2•2•1",
    "2•1•2",
    "3•3",
]

sorted_list = sorted(my_list, key=lambda s: (s.count('•'), int(s.replace('•', ''))))

for item in sorted_list:
    print(item)
