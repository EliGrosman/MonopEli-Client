

text = "fishd ioug hdfisuoghfd iughiudfhgiu"
maxLineLength = 10

splitLines = text.split(' ')
# print(splitLines)
lines = []

cur = splitLines[0]
del splitLines[0]

currentLine = cur
while len(splitLines) > 0:
    next = splitLines[0]
    del splitLines[0]

    while len(currentLine) > maxLineLength:
        lines.append(currentLine[:maxLineLength].strip())
        currentLine = currentLine[maxLineLength:]
    else:
        testLine = currentLine +  " " + next

        if len(testLine) > maxLineLength:
            lines.append(currentLine)

            while len(next) > maxLineLength:
                lines.append(next[:maxLineLength].strip())
                next = next[maxLineLength:]
            else:
                cur = next
                currentLine = next
        else:
            currentLine = testLine
            cur = next
    
    
else:
    while len(currentLine) > maxLineLength:
        lines.append(currentLine[:maxLineLength].strip())
        currentLine = currentLine[maxLineLength:]
    else:
        lines.append(currentLine)

    
    
print(lines)

