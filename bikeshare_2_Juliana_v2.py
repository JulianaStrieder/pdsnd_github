import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    while True:
        try:
            city = input('Enter a city: ').lower()
            if city in ('chicago', 'new york city', 'washington'):
                break
            else:
                print('\nNo city with this name: try again!')
        except ValueError:
            print('That\'s not a valid name!')

 # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Choose one month to analyze or type \'all\' to get all of them: ').lower()
            if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'):
                break
            else:
                print('That\'s not a valid month! Try again!')
        except ValueError:
            print('That\'s not a valid month!')
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Choose one day of the week or type \'all\' to get all of them: ').lower()
            
            if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursay', 'friday', 'saturday', 'sunday'):
                break
            else:
                print('That\'s not a valid day')
        except ValueError:
            print('That\'s not a valid day!')
        
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

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month 
        df = df[df['month'] == month]

    # filter by day of week 
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    #add hour column:
    df['hour'] = df['Start Time'].dt.hour

    return df

def raw_data(df):
    """Display raw data if the user wants. """
    x = 5
    while True:
        raw_dt_display = input('\nDo you want to see raw data?\n').lower()
        
        if raw_dt_display == 'yes' and x < len(df.index):
            print(df.head(x))
            x += 5
        elif x > len(df.index): #and x % 5 < 5:
            print(df.head((x + (x % 5))))
            print('\nYou have reached the last line of the dataset!\n')
            break
        else:
            break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: ', df['month'].mode()[0])


    # display the most common day of week
    print('The most common day is: ', df['day_of_week'].mode()[0])

    # display the most common start hour

    print('The most common start hour is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    m_startstation = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}'.format(m_startstation))

    # display most commonly used end station
    m_endstation = df['End Station'].mode()[0]
    print('The most commonly used end station is {}'.format(m_endstation))

    # display most frequent combination of start station and end station trip
    most_freq = df.groupby(['Start Station', 'End Station']).size().nlargest(1).reset_index(name='count')
    print('The most frequent combination of start station and end station trip is {} and {}'.format(most_freq['Start Station'], most_freq['End Station']))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is {} seconds'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time is {} seconds'.format(df['Trip Duration'].mean())) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Users by type: \n{}'.format(user_types))

    # Display counts of gender
    if city != 'washington':
        user_gender = df['Gender'].value_counts()
        print('Users by gender: {}'.format(user_gender))
    else:
        print('There is no gender data in Washington dataset!')


    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
        print('The earliest, most recent, and most common year of birth are {}, {}, {}, respectively'.format(earliest, most_recent, most_common))
    else:
        print('There is no birth year data in Washington dataset!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def plot_data(df):
    """Displays plots if user choose yes."""

    plot_true = input('\nWould you like to see some calculed statistics with plots? Enter yes or no\n').lower()
    
    if plot_true == 'yes':
        df['User Type'].value_counts().plot(kind='barh')
        plt.ylabel('User Type')
        plt.xlabel('Number of users')
        plt.title('Number of users per type')
        plt.show()

        df['Gender'].value_counts().plot(kind='barh')
        plt.ylabel('Gender')
        plt.xlabel('Number of users')
        plt.title('Number of users per gender')
        plt.show()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        plot_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        

if __name__ == "__main__":
	main()
