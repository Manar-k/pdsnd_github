import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': r'chicago.csv',
              'new york city': r"new_york_city.csv",
              'washington': r"washington.csv" }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
        if city not in ("chicago", "new york city", "washington"):
            print('\nPlease enter valid input')
        else:
            break
            
    while True:
        # get user input for month (all, january, february, ... , june)
        month = input('Enter name of the month to filter by, or "all" to apply no month filter: ').lower()
        if month not in ('all','january', 'february', 'march', 'april', 'may', 'june'):
            print('\nPlease enter valid input')
        else:
            break
          
    while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Enter name of the day of week to filter by, or "all" to apply no day filter: ').lower()
        if day not in ('all','sunday','monday','tuesday','wednesday','thursday','friday','saturday'):
            print('\nPlease enter valid input')
        else:
            break
    
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
    
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        

    # filter by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()] 

    return df




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month: ",df["Start Time"].dt.month_name().mode()[0])

    # display the most common day of week
    print("The most common day of week: ",df["Start Time"].dt.day_name().mode()[0])

    # display the most common start hour
    print("The most common start hour: ",df["Start Time"].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station: ',df["Start Station"].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station: ',df["End Station"].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip: \n {} {}'.format(
        df.groupby(["Start Station","End Station"])['Start Station'].count().idxmax(),
        df.groupby(["Start Station","End Station"])['Start Station'].count().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', np.sum(df['Trip Duration']))

    # display mean travel time
    print('Mean travel time: ', np.mean(df['Trip Duration']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types: \n',df['User Type'].value_counts())
    
    # Display counts of gender
    if 'Gender' in df:
        print('\nCounts of gender: \n',df['Gender'].value_counts())
    else:
        print('\nNo gender data to display. ')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nEarliest year of birth: ',df['Birth Year'].min())
        print('Most recent year of birth: ',df['Birth Year'].max())
        print('Most common year of birth: ',df['Birth Year'].mode()[0])
    else:
        print('\nNo birth year data to display.')

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
        
        # raw data
        df1 = df.iloc[ : , :len(df.columns)-2]
        index, lastindex = 0, 5
        while True:
            showdata = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if showdata.lower() == 'yes':
                print(df1.iloc[index : lastindex])
                index += 5
                lastindex += 5
            elif showdata.lower() == 'no' or lastindex >= df1.shape[0]:
                break
            else:
                print('\nPlease enter valid input')
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
