"""
    Odd Temporal Milestones

    Created by Eric Kong, September 2018.
    All rights reserved.
"""

import datetime
import wpyears

"""
    main()

    Handles user input-output.
"""
def main():
    print("=== Odd Temporal Milestones ===")
    print("\nEnter a past date of interest (e.g., your birthdate).")
    input_date = None
    try:
        year = int(input("Year: "))
        month = int(input("Month (1-12): "))
        day = int(input("Day: "))
        input_date = datetime.date(year, month, day)
    except ValueError:
        print("\nThat does not make for a valid date, silly.")
        return
    today = datetime.date.today()
    if today < input_date:
        print("\nThat date is in the future, silly.")
        return
    
    print("\n===\n")
    print("Your date is " + input_date.strftime("%B %d, %Y") + ".")
    print("To-day is " + today.strftime("%B %d, %Y") + ".")
    delta = today - input_date
    print("That's a difference of " + str(abs(delta.days)) + " days.")
    further_date = input_date - delta
    print(str(abs(delta.days)) + " days before " + input_date.strftime("%B %d, %Y") +
          " is " + further_date.strftime("%B %d, %Y") + ".")

    wpy = wpyears.WPYears()
    before_events, events, after_events = wpy.find_events_on_and_around(further_date)

    if events:
        print("\n===\n")
        print("On " + further_date.strftime("%B %d, %Y") + ", these events happened.\n")
        for event in events:
            print("* " + str(event))
        print("\n" + input_date.strftime("%B %d, %Y") + " is precisely as close to these events as it is to the present day.\n" )

    if after_events:
        print("\n===\n")
        print(input_date.strftime("%B %d, %Y") + " is closer to these events than to the present day.\n")
        for event in after_events:
            print("* " + str(event))

    if before_events:
        before_events = reversed(before_events)
        print("\n===\n")
        print("Soon, " + input_date.strftime("%B %d, %Y") +
              " will be closer to these events than to the present day.\n")
        for event in before_events:
            print("* " + str(event))

    print("\n===\n")
    print("Time is passing.")
    print("\nEvents taken from Wikipedia year articles.")

if __name__ == "__main__":
    main()
