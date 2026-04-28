def per_com():
    components_catalog = [
        "Quiz", "Homework", "Assignment",
        "Hands on Activity", "Discussion",
        "Recitation", "Attendance", "Laboratory"
    ]

    selected = []

    print("\nSelect Class Standing Components")

    for comp in components_catalog:
        while True:
            ans = input(f"Include {comp}? (y/n): ").lower().strip()

            if ans == "y":
                selected.append(comp)
                break
            elif ans == "n":
                break
            else:
                print("Enter y or n only.")

    if not selected:
        print("At least one component required.")
        return per_com()

    while True:
        percents = []
        print("\nEnter component weights")

        for comp in selected:
            while True:
                try:
                    p = float(input(f"{comp} weight (%): "))
                    percents.append(p)
                    break
                except ValueError:
                    print("Invalid number.")

        if round(sum(percents), 2) == 100:
            break
        else:
            print(f"Total is {sum(percents)}%. Must equal 100%.")

    return selected, percents


# -----------------------------
# CLASS STANDING
# -----------------------------
def CS(components, weights):

    total_grade = 0

    for i in range(len(components)):

        while True:
            try:
                num = int(input(f"How many {components[i]} items? "))
                if num > 0:
                    break
                else:
                    print("Must be at least 1.")
            except ValueError:
                print("Enter valid integer.")

        scores = []
        totals = []

        for x in range(1, num + 1):
            while True:
                try:
                    raw = float(input(f"{components[i]} {x} raw score: "))
                    total = float(input(f"{components[i]} {x} total score: "))

                    if raw <= total and total > 0:
                        scores.append(raw)
                        totals.append(total)
                        break
                    else:
                        print("Raw cannot exceed total.")
                except ValueError:
                    print("Invalid input.")

        component_grade = (sum(scores) / sum(totals)) * weights[i]
        total_grade += component_grade

    return total_grade


# -----------------------------
# EXAM INPUT
# -----------------------------
def exam_input():
    while True:
        try:
            raw = float(input("Exam raw score: "))
            total = float(input("Exam total score: "))

            if raw <= total and total > 0:
                return (raw / total) * 100
            else:
                print("Raw cannot exceed total.")
        except ValueError:
            print("Enter valid numbers.")


# -----------------------------
# PRELIM
# -----------------------------
def prelim_grade(cs_grade):

    ans = input("Do you have prelim exam? (y/n): ").lower()

    if ans == "y":
        exam = exam_input()
        return 50 + ((cs_grade * 0.5) + (exam * 0.5))

    else:
        projected = 50 + (cs_grade * 0.5)
        need = (75 - projected) / 0.5

        print("\n--- PRELIM STATUS ---")
        print(f"Current CS: {cs_grade:.2f}")
        print(f"Projected Prelim: {projected:.2f}")

        if need <= 100:
            print(f"Needed exam score to pass: {need:.2f}")
        else:
            print("Passing is mathematically impossible.")

        return None


# -----------------------------
# MIDTERM
# -----------------------------
def midterm_grade(prelim, cs_grade):

    ans = input("Do you have midterm exam? (y/n): ").lower()

    if ans == "y":
        exam = exam_input()
        mid_comp = (cs_grade * 0.5) + (exam * 0.5)
        return 50 + ((prelim / 3) + ((2/3) * mid_comp))

    else:
        projected = 50 + ((prelim / 3) + ((2/3) * (cs_grade * 0.5)))
        need = (75 - (50 + (prelim / 3))) / ((2/3) * 0.5)

        print("\n--- MIDTERM STATUS ---")
        print(f"Current CS: {cs_grade:.2f}")
        print(f"Projected Midterm: {projected:.2f}")

        if need <= 100:
            print(f"Needed exam score to pass: {need:.2f}")
        else:
            print("Passing is mathematically impossible.")

        return None


# -----------------------------
# FINALS
# -----------------------------
def final_grade(midterm, cs_grade):

    ans = input("Do you have final exam? (y/n): ").lower()

    if ans == "y":
        exam = exam_input()
        final_comp = (cs_grade * 0.5) + (exam * 0.5)
        return 50 + ((midterm / 3) + ((2/3) * final_comp))

    else:
        projected = 50 + ((midterm / 3) + ((2/3) * (cs_grade * 0.5)))
        need = (75 - (50 + (midterm / 3))) / ((2/3) * 0.5)

        print("\n--- FINAL STATUS ---")
        print(f"Current CS: {cs_grade:.2f}")
        print(f"Projected Final: {projected:.2f}")

        if need <= 100:
            print(f"Needed exam score to pass: {need:.2f}")
        else:
            print("Passing is mathematically impossible.")

        return None


# -----------------------------
# MAIN
# -----------------------------
def main():

    components, weights = per_com()

    prelim = None
    midterm = None
    final = None

    cs_prelim = None
    cs_midterm = None
    cs_final = None

    while True:

        print("\n====== MENU ======")
        print("1 Prelim")
        print("2 Midterm")
        print("3 Finals")
        print("4 Summary")
        print("5 Exit")

        choice = input("Select (1-5): ")

        # PRELIM
        if choice == "1":
            if cs_prelim is None:
                cs_prelim = CS(components, weights)

            prelim = prelim_grade(cs_prelim)

            if prelim is not None:
                print(f"Prelim Grade: {prelim:.2f}")

        # MIDTERM
        elif choice == "2":
            if prelim is None:
                prelim = float(input("Enter Prelim Grade: "))

            if cs_midterm is None:
                cs_midterm = CS(components, weights)

            midterm = midterm_grade(prelim, cs_midterm)

            if midterm is not None:
                print(f"Midterm Grade: {midterm:.2f}")

        # FINALS
        elif choice == "3":
            if midterm is None:
                midterm = float(input("Enter Midterm Grade: "))

            if cs_final is None:
                cs_final = CS(components, weights)

            final = final_grade(midterm, cs_final)

            if final is not None:
                print(f"Final Grade: {final:.2f}")

        # SUMMARY
        elif choice == "4":
            print("\n--- SUMMARY ---")

            print(f"Prelim: {prelim:.2f}" if prelim else "Prelim pending")
            print(f"Midterm: {midterm:.2f}" if midterm else "Midterm pending")
            print(f"Final: {final:.2f}" if final else "Final pending")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
