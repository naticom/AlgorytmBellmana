import module

f = open('map.txt','r')
file = [line.strip('\n').split() for line in f.readlines()]
f.close()


tabTypeElement = []    #typ każdego z pól
tabValueR = []          # wartość R każego z pól
height = int(file[0][1])
width = int(file[0][0])
columns = height * width
gamma = 0.5

for line in file[2:]:
    if line:
        tabTypeElement.append(line)
    else:
        break

for line in file[(2+height):]:
        if line:
            tabValueR.append(line)

print(tabTypeElement)
print(tabValueR)

allElements = [[0 for x in range(width)] for y in range(height)]

rowIndex = 0
for row in tabTypeElement:
    elIndex = 0
    for element in row:

        if element == '1':   #robimy działania tylko na elementach 1
            #ruch w gore
            moveUp = [[0]*width for i in range(height)]
            #ruch w prawo
            moveRight = [[0]*width for i in range(height)]
            #ruch w dol
            moveDown = [[0]*width for i in range(height)]
            #ruch w lewo
            moveLeft = [[0]*width for i in range(height)]

            if ((rowIndex - 1) < 0) or (tabTypeElement[rowIndex-1][elIndex] == '0'):
                moveUp[rowIndex][elIndex] += 0.8
                moveRight[rowIndex][elIndex] += 0.1
                moveLeft[rowIndex][elIndex] += 0.1
            else:
                moveUp[rowIndex-1][elIndex] += 0.8
                moveRight[rowIndex-1][elIndex] += 0.1
                moveLeft[rowIndex-1][elIndex] += 0.1

            if ((elIndex + 1) >= width) or (tabTypeElement[rowIndex][elIndex+1] == '0'):
                moveUp[rowIndex][elIndex] += 0.1
                moveRight[rowIndex][elIndex] += 0.8
                moveDown[rowIndex][elIndex] += 0.1
            else:
                moveUp[rowIndex][elIndex+1] += 0.1
                moveRight[rowIndex][elIndex+1] += 0.8
                moveDown[rowIndex][elIndex+1] += 0.1


            if((rowIndex + 1) >= height) or (tabTypeElement[rowIndex+1][elIndex] == '0'):
                moveRight[rowIndex][elIndex] += 0.1
                moveDown[rowIndex][elIndex] += 0.8
                moveLeft[rowIndex][elIndex] += 0.1
            else:
                moveRight[rowIndex+1][elIndex] += 0.1
                moveDown[rowIndex+1][elIndex] += 0.8
                moveLeft[rowIndex+1][elIndex] += 0.1

            if ((elIndex - 1) < 0) or (tabTypeElement[rowIndex][elIndex-1] == '0'):
                moveUp[rowIndex][elIndex] += 0.1
                moveDown[rowIndex][elIndex] += 0.1
                moveLeft[rowIndex][elIndex] += 0.8
            else:
                moveUp[rowIndex][elIndex-1] += 0.1
                moveDown[rowIndex][elIndex-1] += 0.1
                moveLeft[rowIndex][elIndex-1] += 0.8

        else:
            moveUp = 0
            moveRight = 0
            moveLeft = 0
            moveDown = 0

        movements = [moveUp, moveRight, moveDown, moveLeft]
        allElements[rowIndex][elIndex] = module.Field(rowIndex, elIndex, movements, float(tabValueR[rowIndex][elIndex]), float(tabValueR[rowIndex][elIndex]),0,element)

        elIndex += 1
    rowIndex += 1

for i in range(1000):
    for row in allElements:
        for element in row:
            if element.type == '1':
                actionTab = [module.Action(1,0), module.Action(2,0), module.Action(3,0), module.Action(4,0)] #polityka ruchu 1,2,3,4 - góra prawo dół lewo
                oldV = element.v

                for j in range(len(element.movements)):
                    probab = element.movements[j]
                    pRow = 0
                    for row in probab:
                        pCol = 0
                        for col in row:
                            if col!= 0:
                                elP = float(probab[pRow][pCol])
                                elV = float(allElements[pRow][pCol].v)
                                actionTab[j].value += float(elP*elV)
                            pCol += 1
                        pRow += 1
                maxValueAction = actionTab[0].value    #maksymalna wartość w akcji
                newAction = actionTab[0].move

                newV = 0
                for ac in actionTab:
                    if ac.value > maxValueAction:
                        maxValueAction = float(ac.value)
                        newAction = ac.move
                    newV = int(element.r) + gamma * maxValueAction     #potencjał stanu s

                if abs(oldV - newV) > 0.0001:
                    element.v = newV
                    element.action = newAction
                else:
                    break

resultMap = [['' for x in range(width)] for y in range(height)]
rowNumber = 0
for row in allElements:
    colNumber = 0
    for elem in row:
        string = ("{0:.2f}".format(elem.v)), elem.action
        resultMap[rowNumber][colNumber] = string
        colNumber += 1
    rowNumber +=1

print
for row in resultMap:                #Mapa potencjałów dla gammy =0,5
    print(row)