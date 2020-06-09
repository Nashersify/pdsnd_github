mport time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    def user_prompt(input_prompt, valid_values):
        out = input(input_prompt + ": \n")
        out = out.lower()
        while(out not in valid_values):
            print("Not recognized")
            out = input(input_prompt + ": \n")
        return out
                  
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_prompt = "Please select a city, your choices are chicago, new york city, and washington"
    city = user_prompt(city_prompt, CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)
    month_prompt = "Please select a month (all, january, february, ... , june)"
    month_valid_values = {"all", "january", "february", "march", "april", "may", "june"}
    month = user_prompt(month_prompt, month_valid_values)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_prompt = "Please select a day (all, monday, tuesday, ... sunday)"
    day_valid_values = {"all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
    day = user_prompt(day_prompt, day_valid_values)


    print('-'*40)
    print(city, month, day)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def most_popular(df, field, human_text):
    """Generalized function to print the most common value of a field."""
    out = df[field].mode()[0]
    print('Most Popular', human_text, ":", out)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # month already extracted
    most_popular(df, 'month', 'Start Month')


    # display the most common day of week
    # day of week already extracted
    most_popular(df, 'day_of_week', "Day of Week")

    
    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    most_popular(df, 'hour', 'Start Hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular(df, "Start Station", "Start Station")

    # display most commonly used end station
    most_popular(df, "End Station", "End Station")

    # display most frequent combination of start station and end station trip
    # create column with combination of start and end stations
    df['start_end'] = df["Start Station"] + " TO " + df["End Station"]
    most_popular(df, "start_end", "Start & End Station Combination")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # convert end time to date time. Start time was already converted
    df['End Time'] = pd.to_datetime(df['End Time'])

    # create travel time per trip
    df['travel_time'] = df['End Time'] - df['Start Time']
    
    # display total travel time
    print('Total travel time :', df['travel_time'].sum())

    # display mean travel time
    print('Mean travel time :', df['travel_time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print('User Type Counts:')
    print(df['User Type'].value_counts())

    # display counts of gender
    print('Gender Counts:')
    print(df['Gender'].value_counts())

    # display earliest, most recent, and most common year of birth
    print("Earliest Birth Year:", df['Birth Year'].min())
    print("Most Recent Birth Year:", df['Birth Year'].max())
    most_popular(df, 'Birth Year', 'Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

