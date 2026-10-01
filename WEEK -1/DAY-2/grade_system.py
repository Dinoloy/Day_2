def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


try:
    mark = float(input("Enter your mark (0-100): "))

    if mark < 0 or mark > 100:
        print("Invalid mark. Please enter a number between 0 and 100.")
    else:
        grade = get_grade(mark)
        print(f"Mark: {mark} | Grade: {grade}")

except ValueError:
    print("Invalid input. Please enter a number.")
