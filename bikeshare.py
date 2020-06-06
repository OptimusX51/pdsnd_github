import time
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please select a city: Chicago, New York City, or Washington\n')
        if city.lower() in ['chicago', 'new york city', 'washington']:
            print('You have chosen {}!\n'.format(city.title()))
            break
        else:
            print('Invalid input. Try again.\n\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month_filter = input('Would you like to filter by month?\n')
        if month_filter.lower() in ['no', 'n']:
            month = 'all'
            print('All months data will be used.')
            break
        elif month_filter.lower() in ['yes', 'y']:
            while True:
                month_in = input('Please enter a month between January and June:\n')
                if len(month_in) > 1 and [i for i in months_list if month_in in i] :
                    month = str([i for i in months_list if month_in in i[0:3]]).title().strip("[]'").lower()
                #if month.lower() in months_list:
                    print('You have chosen {}.\n'.format(month.title()))
                    break
                else:
                    print('Invalid input. Please enter month.\n\n')
            break
        else:
            print('Invalid input. Try again.\n')
    
    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day_filter = input('Would you like to filter by day of the week?\n')
        if day_filter.lower() in ['no', 'n']:
            day='all'
            break
        elif day_filter in ['yes', 'y']:
            while True:
                day_in = input('Please enter the day of the week or "all" for all days:\n')
                if len(day_in) > 1 and [i for i in days_list if day_in in i] :
                    day = str([i for i in days_list if day_in in i[0:3]]).title().strip("[]'").lower()
                    print('You have chosen {}.\n'.format(day))
                    break
                else:
                    print('Invalid input. Try again.\n\n')
            break
        else:
            print('Invalid input.  Try again.\n')

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
        df = df[df['day_of_week'] == str(day).strip("[]'").title()]

    return df


def time_stats(df):
    
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # TO DO: display the most common month
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    df['month'] = df['Start Time'].dt.month
    month_index = df['month'].mode()[0]-1
    popular_month = str(month_list[month_index]).title()
    print('The most popular month for a bike ride this time period: {}\n'.format(popular_month))


    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most Popular ride day: {}\n'.format(popular_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: {}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input('Press any key to continue with more statistics!')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is {}.'.format(popular_start_station))
    
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is {}{}.'.format(('also ' if popular_start_station==popular_end_station else ''),popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Endpoint Stations'] = df['Start Station'] + df['End Station']
    
    popular_endpoints = df['Endpoint Stations'].mode()[0]
    print('The most popular station endpoints are {}.\n'.format(popular_endpoints))

    input('Press any key to continue with more statistics!')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is:       {:,} hours'.format(total_travel_time))
    
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time is:     {:.2f} hours'.format(mean_travel_time))

    input('Press any key to continue with more statistics!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    users = df['User Type'].value_counts()
    print('User types:\n{}\n'.format(users))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('User genders:\n{}\n'.format(genders))
    else:
        print("\nNo 'Gender' data in this set\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        print('Earliest user birth year:       {}\n'.format(int(oldest)))

        youngest = df['Birth Year'].max()
        print('Most recent user birth year:    {}\n'.format(int(youngest)))

        popular_birthyear = df['Birth Year'].mode()[0]
        print('Most common user birth year:    {}\n'.format(int(popular_birthyear)))
    else:
        print("\nNo 'Birth Year' data in this set\n")
        
    time.sleep(.5)

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

        restart = input('\nWould you like to run a different query?(yes/no)\n')
        if restart.lower() not in ['y','yes']:
            for chunk in pd.read_csv(CITY_DATA[city], chunksize=5):
                print(chunk)
                end = input('\nContinue with data..?(y/n)\n')
                if end.lower() not in ['yes','y']:
                    break
                else:
                    continue
            print('Goodbye')
            break


if __name__ == "__main__":
    main()
