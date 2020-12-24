import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
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

    #Prepare series for easy filters entry check
    city_series = ['Chicago', 'NYC', 'Washington', 'chicago', 'nyc', 'washington']
    month_series = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_series = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'staurday', 'sunday']

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, NYC or Washington? ").lower()

    #Re-prompt for entry in case of invalid city
    while city not in city_series:
        try:
            city = input("Oops! You entered an invalid city, please choose from: Chicago, NYC or Washington ").lower()
        except Exception as e:
            print("Exception occurred: {}".format(e))

    usr_filter = input("Would you like to filter data by Month, Day or Both? ").lower()

    if usr_filter == "month":
        # TO DO: get user input for month (all, january, february, ... , june)
        month = input("Which month: all, january, february, march, april, may or june.. ").lower()
        day = None
        #Re-prompt for entry in case of invalid month
        while month not in month_series:
            try:
                month = input("Oops! You entered an invalid month, please choose from: all, january, february, march, april, may or june.. ").lower()
                day = None
            except Exception as e:
                print("Exception occurred: {}".format(e))
    elif usr_filter == "day":
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("And day of week? all, monday, tuesday, wednesday, thursday, friday, saturday or sunday.. ").lower()
        month = None
        #Re-prompt for entry in case of invalid day
        while day not in day_series:
            try:
                day = input("Oops! You entered an invalid day of week, please choose from: all, monday, tuesday, wednesday, thursday, friday, saturday or sunday.. ").lower()
                month = None
            except Exception as e:
                print("Exception occurred: {}".format(e))

    elif usr_filter == "both":
        month = input("Which month: all, january, february, march, april, may or june.. ").lower()
        #Re-prompt for entry in case of invalid month
        while month not in month_series:
            try:
                month = input("Oops! You entered an invalid month, please choose from: all, january, february, march, april, may or june.. ").lower()
            except Exception as e:
                print("Exception occurred: {}".format(e))

        day = input("And day of week? all, monday, tuesday, wednesday, thursday, friday, saturday or sunday.. ").lower()
        #Re-prompt for entry in case of invalid day
        while day not in day_series:
            try:
                day = input("Oops! You entered an invalid day of week, please choose from: all, monday, tuesday, wednesday, thursday, friday, saturday or sunday.. ").lower()
            except Exception as e:
                print("Exception occurred: {}".format(e))

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all' and month is not None:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all' and day is not None:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: get the month, day of week and hour
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular month, day, hour
    popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]
    popular_hour = df['hour'].mode()[0]

    # display the most popular month, day, hour
    print('Most Common Month:', popular_month)
    print('Most Common Day of Week:', popular_day)
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: get most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    # TO DO: get most commonly used end station
    popular_end = df['End Station'].mode()[0]

    # TO DO: get most frequent combination of start station and end station trip
    df['Combined Trip']=df.apply(lambda x:'%s_%s' % (x['Start Station'],x['End Station']),axis=1)
    popular_trip = df['Combined Trip'].mode()[0]

    # display the most common stations and trips
    print('Most Common Start Station:', popular_start)
    print('Most Common End Station:', popular_end)
    print('Most Common Start-End Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()

    print('Total Travel Time:', total_travel)
    print('Average Travel Time:', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: get counts of user types
    subs_count    = df['User Type'].value_counts()[0]
    cust_count    = df['User Type'].value_counts()[1]

    # display user types count..
    print('Subscriber Total:', subs_count)
    print('Customer Total:', cust_count)

    # Applicable ONLY to Chicago and NYC files and addtional colums (gender/birth year)
    if city != 'washington':
        # display user types count..
        df['Gender'].fillna(0)
        df['Birth Year'].fillna(0)

        # TO DO: get counts of gender
        male_count    = df['Gender'].value_counts()[0]
        female_count  = df['Gender'].value_counts()[1]

        # TO DO: get earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        recent_year   = df['Birth Year'].max()
        common_year   = df['Birth Year'].mode()[0]

        # display gender counts, earliest, most recent, and most common year of birth
        print('Male Total:', male_count)
        print('Female Total:', female_count)
        print('Earliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', recent_year)
        print('Most Common Year of Birth:', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #Ask user to view 5 rows of trip info?
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    #Repeat asking until user chooses 'no'
    while view_data.lower() != 'no':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you wish to continue?: ').lower()

def main():
    while True:

        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except Exception as e:
            print("Exception occurred: {}".format(e))
            print("Exiting program..")
            break

if __name__ == "__main__":
	main()
