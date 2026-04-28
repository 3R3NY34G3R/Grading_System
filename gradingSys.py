def per_com():
    components_catalog = [
        "Quiz",
        "Homework",
        "Assignment",
        "Hands on Activity",
        "Discussion",
        "Recitation",
        "Attendance",
        "Laboratory"
    ]

    selected=[]

    print("\nSelect Class Standing Components")

    for comp in components_catalog:
        while True:
            ans=input(
                f"Include {comp}? (y/n): "
            ).lower().strip()

            if ans=="y":
                selected.append(comp)
                break
            elif ans=="n":
                break
            else:
                print("Enter y or n only.")

    if not selected:
        print("At least one component required.")
        return per_com()

    while True:
        percents=[]

        print("\nEnter component weights")

        for comp in selected:
            while True:
                try:
                    p=float(
                        input(f"{comp} weight (%): ")
                    )
                    percents.append(p)
                    break
                except ValueError:
                    print("Invalid number.")

        if round(sum(percents),2)==100:
            break
        else:
            print(
              f"Total is {sum(percents)}%. Must equal 100%."
            )

    return selected,percents


# -----------------------------
# Class Standing
# -----------------------------

def CS(components,weights):

    total_grade=0

    for i in range(len(components)):

        while True:
            try:
                num=int(
                    input(
                        f"How many {components[i]} items? "
                    )
                )

                if num>0:
                    break
                else:
                    print("Must be at least 1.")

            except ValueError:
                print("Enter valid integer.")


        names=[
            f"{components[i]} {x}"
            for x in range(1,num+1)
        ]

        scores=[]
        totals=[]

        for item in names:
            while True:
                try:
                    raw=float(
                        input(
                          f"{item} raw score: "
                        )
                    )

                    total=float(
                        input(
                           f"{item} total score: "
                        )
                    )

                    if raw<=total and total>0:
                        scores.append(raw)
                        totals.append(total)
                        break
                    else:
                        print(
                          "Raw cannot exceed total."
                        )

                except ValueError:
                    print("Invalid input.")

        component_grade=(
            sum(scores)/sum(totals)
        )*weights[i]

        total_grade+=component_grade

    return total_grade


# -----------------------------
# Exam Input
# -----------------------------

def exam_input():

    while True:
        try:
            raw=float(input("Exam raw score: "))
            total=float(input("Exam total score: "))

            if raw<=total and total>0:
                return (raw/total)*100
            else:
                print(
                  "Raw cannot exceed total."
                )

        except ValueError:
            print("Enter valid numbers.")


# -----------------------------
# Prelim
# -----------------------------

def prelim_grade(cs_grade):

    ans=input(
       "Do you have prelim exam? (y/n): "
    ).lower()

    if ans=="y":

        exam=exam_input()

        prelim=50+(
            (cs_grade*.5)
            +
            (exam*.5)
        )

        return prelim

    elif ans=="n":

        projected=50+(cs_grade*.5)

        need=(75-projected)/0.5

        print("\n--- PRELIM STATUS ---")
        print(
          f"Current CS: {cs_grade:.2f}"
        )
        print(
          f"Projected Prelim: {projected:.2f}"
        )

        if need<=100:
            print(
             f"Needed exam score to pass: {need:.2f}"
            )
        else:
            print(
             "Passing is mathematically impossible."
            )

        return None


# -----------------------------
# Midterm
# -----------------------------

def midterm_grade(prelim,components,weights):

    cs_grade=CS(
        components,
        weights
    )

    ans=input(
      "Do you have midterm exam? (y/n): "
    ).lower()

    if ans=="y":

        exam=exam_input()

        mid_comp=(cs_grade*.5)+(exam*.5)

        mid=50+(
            (prelim/3)
            +
            ((2/3)*mid_comp)
        )

        return mid

    elif ans=="n":

        projected=50+(
            (prelim/3)
            +
            ((2/3)*(cs_grade*.5))
        )

        need=(
            75-(50+(prelim/3))
        )/((2/3)*0.5)

        print("\n--- MIDTERM STATUS ---")
        print(
         f"Current CS: {cs_grade:.2f}"
        )
        print(
         f"Projected Midterm: {projected:.2f}"
        )

        if need<=100:
            print(
             f"Needed exam score to pass: {need:.2f}"
            )
        else:
            print(
             "Passing is mathematically impossible."
            )

        return None


# -----------------------------
# Finals
# -----------------------------

def final_grade(midterm,components,weights):

    cs_grade=CS(
        components,
        weights
    )

    ans=input(
      "Do you have final exam? (y/n): "
    ).lower()

    if ans=="y":

        exam=exam_input()

        final_comp=(cs_grade*.5)+(exam*.5)

        final=50+(
            (midterm/3)
            +
            ((2/3)*final_comp)
        )

        return final

    elif ans=="n":

        projected=50+(
            (midterm/3)
            +
            ((2/3)*(cs_grade*.5))
        )

        need=(
           75-(50+(midterm/3))
        )/((2/3)*0.5)

        print("\n--- FINAL STATUS ---")
        print(
          f"Current CS: {cs_grade:.2f}"
        )
        print(
          f"Projected Final: {projected:.2f}"
        )

        if need<=100:
            print(
             f"Needed exam score to pass: {need:.2f}"
            )
        else:
            print(
              "Passing is mathematically impossible."
            )

        return None


# -----------------------------
# Main Menu
# -----------------------------

def main():

    components,weights=per_com()

    prelim=None
    midterm=None
    final=None

    while True:

        print("\n====== MENU ======")
        print("1 Prelim")
        print("2 Midterm")
        print("3 Finals")
        print("4 Summary")
        print("5 Exit")

        choice=input(
          "Select (1-5): "
        )

        if choice=="1":

            cs=CS(
                components,
                weights
            )

            prelim=prelim_grade(cs)

            if prelim is not None:
                print(
                 f"Prelim Grade: {prelim:.2f}"
                )


        elif choice=="2":

            if prelim is None:
                prelim=float(
                  input(
                    "Enter Prelim Grade: "
                  )
                )

            midterm=midterm_grade(
                prelim,
                components,
                weights
            )

            if midterm is not None:
                print(
                 f"Midterm Grade: {midterm:.2f}"
                )


        elif choice=="3":

            if midterm is None:
                midterm=float(
                   input(
                     "Enter Midterm Grade: "
                   )
                )

            final=final_grade(
                midterm,
                components,
                weights
            )

            if final is not None:
                print(
                 f"Final Grade: {final:.2f}"
                )


        elif choice=="4":

            print("\n--- SUMMARY ---")

            print(
              f"Prelim: {prelim:.2f}"
              if prelim is not None
              else "Prelim pending"
            )

            print(
              f"Midterm: {midterm:.2f}"
              if midterm is not None
              else "Midterm pending"
            )

            print(
              f"Final: {final:.2f}"
              if final is not None
              else "Final pending"
            )


        elif choice=="5":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__=="__main__":
    main()

