import time
import pandas as pd


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

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in ["chicago", "new york city", "washington"] :
        city = input("Choose city (Chicago, New York City, Washington) :\n").lower()

    
    time_filter =""
    while time_filter not in ["month", "day", "both", "none"] :
        time_filter = input("Would you like to filter the data by (month, day, both, none) :\n").lower()
        
        if time_filter =="month" :
            # get user input for month (all, january, february, ... , june)
            month=''
            while month not in ["january", "february", "march", "april", "may", "june"] :
                month = input("Choose month (January, February, March, April, May, June) :\n").lower()
            print('-'*40)
            return city, month, 'all'
        
        elif time_filter =="day" :
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day=''
            while day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] :
                day = input("Choose day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) :\n").lower()
            print('-'*40)
            return city, 'all', day

        elif time_filter =="both" :
            month=''
            while month not in ["january", "february", "march", "april", "may", "june"] :
                month = input("Choose month (January, February, March, April, May, June) :\n").lower()
            day=''
            while day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] :
                day = input("Choose day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) :\n").lower()
            print('-'*40)
            return city, month, day
        
        elif time_filter =="none"  :
            print('-'*40)
            return city, 'all', 'all'



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

    # convert the start time column to datetime column
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week to new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].mode()[0]
    print('The most common month:', most_month)

    # display the most common day of week
    most_day = df['day_of_week'].mode()[0]
    print('The most common day of week:', most_day)

    # display the most common start hour
    most_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common Start Time:', most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start = df['Start Station'].mode()[0]
    print('The most common Start Station:', most_start)

    # display most commonly used end station
    most_end = df['End Station'].mode()[0]
    print('The most common End Station:', most_end)

    # display most frequent combination of start station and end station trip
    most_combination = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most frequent combination of start station and end station trip:', most_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("counts of user types :", user_counts)

    if city != 'washington' :
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("counts of user types :", gender_counts)

        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print("The most earliest birth year:", earliest_year)
        recent_year = df['Birth Year'].max()
        print("The most recent birth year:", recent_year)
        common_year = df['Birth Year'].mode()[0]
        print("The most most common year of birth:", common_year)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_data(df):
    """Raw data is displayed upon request by the user"""
    n=0
    while True:
        display=input("\nWould you like to see want to see 5 lines of raw data? (yes, no)\n").lower()
        if display =='no':
            break
        elif display=='yes':
            n=n+5
            print(df.iloc[n-5:n])
        else:
            print('\nInvalid input')
  


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
