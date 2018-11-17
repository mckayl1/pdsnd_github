import time
import pandas as pd
import numpy as np
#refactoring
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in ('chicago','new york city','washington','all'):
            city = input("Which of the following cities would you like to look at? (chicago, new york city, washington)\n")
            city = city.lower()
    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while month not in ('january','february','march','april','june','all'):
        month = input("which month would you like to look at (all, january, february, ... , june)?\n")
        month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'):
        day = input('which day would you like to look at (all, monday, tuesday, ... sunday)?\n')
        day = day.lower()
        
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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost Popular Month:', popular_month)
    # TO DO: display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('\nMost Popular Day:', popular_dow)
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is: ', popular_start)

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is: ', popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df[['Start Station','End Station']].mode()
    print('\nThe most common trip is:\n ', popular_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = np.sum(df['Trip Duration'])
    print('\nThe total time is :\n', total_time)

    # TO DO: display mean travel time
    mean_time = np.mean(df['Trip Duration'])
    print('\nThe average travel time is:\n', mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # TO DO: Display counts of gender
    dfs = df.loc[lambda df: df['User Type'] == 'Subscriber']
    #got this from https://pandas.pydata.org/pandas-docs/stable/indexing.html
    if city != 'washington':
        gender_types = dfs['Gender'].value_counts()
        print(gender_types)


        # TO DO: Display earliest, most recent, and most common year of birth
        earliest = dfs['Birth Year'].min()
        #got this from https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.min.html
        recent = dfs['Birth Year'].max()
        #got this from https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.max.html
        
        common = dfs['Birth Year'].mode()[0]
        print("\nThe earliest year of birth was: ", earliest)
        print("\nThe most recent year of birth was: ", recent)
        print("\nThe most common year of birth was: ", common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    raw_data = ''
    while raw_data.lower() not in ('yes','no'):
        print(raw_data.lower())
        raw_data = input('\nWould you like to see raw data?\n')
    i=0
    while raw_data.lower() == 'yes':
        print(df.iloc[i:i+5])
        i +=5
        raw_data=''
        while raw_data.lower() not in ('yes','no'):
            raw_data = input('\nWould you like to see more raw data?\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
