def per_com():
    component = ["Quiz","Homework","Assignment","Hands on Activity","Discussion","Recitation","Attendance"]

    Y =[]
    n = len(component)
    a = 0
    while n > 0:
        stud = input(f"Is this in your CS {component[a]}(y/n): ").lower()
        if stud == 'y':
            Y.append(component[a])
            n -= 1
            a += 1
        elif stud == 'n':
            n -= 1
            a += 1
            continue
        else:
            print("Please type invalid answer!")

    while True:
        percent = []
        for comp in Y:
            while True:
                stud1 = input(f"Percent of the {comp}: ")
                try:
                    percent.append(int(stud1))
                    break
                except ValueError:
                    print("Please input a valid number!")

        if sum(percent) == 100:
            break
        else:
            print(f"perctage: {sum(percent)} must be equal to 100")
  
    return Y, percent

def CS(component,percent):

    for i in range(len(component)):
            while(True):    
                user = input(f"How many {component[i]}? ")
                try:
                    num = int(user)
                    break
                except ValueError:
                    print("type a valid number")

            names = [f"{component[i]}{_}" for _ in range(1,num+1)]
            scores = []
            allOver =[]
            x = 0
            while num > 0:
                try:
                    y = int(input(f"{names[x]} raw score: "))
                    z = int(input(f"Tota score: "))
                    if y < z:
                        scores.append(y)
                        allOver.append(z)
                        num -= 1
                        x += 1
                    else:
                        print("Raw score must less than to Total score")
                except ValueError:
                    print("Input Valid number!")

            for name,score,over in zip(names,scores,allOver):
                print(f"{name} : {score}/{over}")

            CS_grade = (sum(scores)/len(allOver))*percent[i]

            return CS_grade


def prelim():
    pass

if __name__ == __name__:
    components, percents = per_com()
    grade = CS(components, percents)
    print(grade)
