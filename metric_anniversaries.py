"""
    Metric Historical Anniversaries

    Created by Eric Kong, September 2018.
    All rights reserved.
"""

import datetime
import wpyears


"""
    generate_round_numbers()

    Returns a list of round numbers.
"""
def generate_round_numbers():
    numbers = []
    for power in range(2, 6):
        for digit in range(1, 10):
            numbers.append(digit * (10 ** power))
    return numbers

"""
    main()

    Handles user input-output.
"""
def main():
    print("=== Metric Historical Anniversaries ===")
    today = datetime.date.today()
    print("\nTo-day is " + today.strftime("%B %d, %Y") + ".")

    numbers = generate_round_numbers()
    wpy = wpyears.WPYears()
    for number in numbers:
        try:
            date = today - datetime.timedelta(days=number)
        except OverflowError:
            break
        events = wpy.find_events_on(date, ranges=False)
        if events:
            print("\n" + str(number) + " days ago was " + date.strftime("%B %d, %Y") + ". On this date:")
            for event in events:
                print("* " + event.string)

    print("\n===\n")
    print("Those are your metric historical anniversaries for to-day.")
    print("\nEvents taken from Wikipedia year articles.")

if __name__ == "__main__":
    main()
