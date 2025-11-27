def per_com():
    component = ["Quiz","Homework","Assignment","Hands on Activity","Discussion","Recitation","Attendance"]

    Y = []
    for comp in component:
        stud = input(f"Is this in your CS {comp} (y/n): ").lower() 
        if stud == 'y':
            Y.append(comp)
        elif stud == 'n':
            continue
        else:
            print("Please type a valid answer!")

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
            print(f"Percentage sum = {sum(percent)}. Must equal 100.")

    return Y, percent


def CS(component, percent):
    total_grade = 0
    for i in range(len(component)):
        while True:    
            user = input(f"How many {component[i]}? ")
            try:
                num = int(user)
                break
            except ValueError:
                print("Type a valid number")

        names = [f"{component[i]}{_}" for _ in range(1, num+1)]
        scores = []
        allOver = []

        for name in names:
            while True:
                try:
                    y = int(input(f"{name} raw score: "))
                    z = int(input("Total score: "))
                    if y <= z:
                        scores.append(y)
                        allOver.append(z)
                        break
                    else:
                        print("Raw score must be less than or equal to Total score")
                except ValueError:
                    print("Input a valid number!")

        for name, score, over in zip(names, scores, allOver):
            print(f"{name} : {score}/{over}")

        CS_grade = (sum(scores) / sum(allOver)) * percent[i]
        total_grade += CS_grade

    return total_grade


def exam_input():
    while True:
        try:
            raw = int(input("Exam raw score: "))
            total = int(input("Exam total score: "))
            if raw <= total:
                return (raw / total) * 100
            else:
                print("Raw score must be less than or equal to total score")
        except ValueError:
            print("Input valid numbers!")


def prelim_grade(cs_grade):
    user2 = input("Do you have prelim exam ?(y/n): ").lower()
    if user2 == "y":
        pre_ex = exam_input()
        pre_g = 50 + ((cs_grade * 0.5) + (pre_ex * 0.5))
    else:
        need_exam = (75 - (50 + (cs_grade * 0.5))) / 0.5
        print(f"You need {need_exam:.2f} in the exam to pass.")
        pre_g = 50 + (cs_grade * 0.5)
    return pre_g


def midterm_grade(pre_g, components, percents):
    cs_grade = CS(components, percents)
    user = input("Do you have midterm exam ?(y/n): ").lower()
    if user == "y":
        mid_ex = exam_input()
        mid_cs = (cs_grade * 0.5) + (mid_ex * 0.5)
        mid_g = 50 + ((pre_g * (1/3)) + (mid_cs * (2/3)))
    else:
        need = (75 - (50 + (pre_g * (1/3)))) / (2/3 * 0.5)
        print(f"You need {need:.2f} in the midterm exam to pass.")
        mid_g = 50 + ((pre_g * (1/3)) + (cs_grade * 0.5 * (2/3)))
    return mid_g


def final_grade(mid_g, components, percents):
    cs_grade = CS(components, percents)
    user = input("Do you have final exam ?(y/n): ").lower()
    if user == "y":
        fin_ex = exam_input()
        fin_cs = (cs_grade * 0.5) + (fin_ex * 0.5)
        fin_g = 50 + ((mid_g * (1/3)) + (fin_cs * (2/3)))
    else:
        need = (75 - (50 + (mid_g * (1/3)))) / (2/3 * 0.5)
        print(f"You need {need:.2f} in the final exam to pass.")
        fin_g = 50 + ((mid_g * (1/3)) + (cs_grade * 0.5 * (2/3)))
    return fin_g


def main():
    components, percents = per_com()
    pre = mid = fin = None

    while True:
        print("\n1.Prelim\n")
        print("2.Midterm\n")
        print("3.Finals\n")
        print("4.Summary\n")
        print("5.Exit\n")

        users = input("\nWhat do you want to do? (1-5): ")

        if users == "1":
            cs = CS(components, percents)
            pre = prelim_grade(cs)
            print(f"Prelim Grade: {pre:.2f}")
        elif users == "2":
            if pre is None:
                pre = float(input("Enter your Prelim Grade: "))
            mid = midterm_grade(pre, components, percents)
            print(f"Midterm Grade: {mid:.2f}")
        elif users == "3":
            if mid is None:
                mid = float(input("Enter your Midterm Grade: "))
            fin = final_grade(mid, components, percents)
            print(f"Final Grade: {fin:.2f}")
        elif users == "4":
            print("\nSummary\n")
            print(f"Prelim Grade: {pre:.2f}" if pre else "Prelim not computed yet")
            print(f"Midterm Grade: {mid:.2f}" if mid else "Midterm not computed yet")
            print(f"Final Grade: {fin:.2f}" if fin else "Final not computed yet")
        elif users == "5":
            print("Exit!")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()