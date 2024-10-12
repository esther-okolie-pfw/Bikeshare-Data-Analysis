import time
import pandas as pd
import numpy as np
import datetime as dat
import matplotlib.pyplot as plt
import seaborn as sns




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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city_ref = int(input('What city would you like to get insight on?\navailable cities are chicago, new york city and washington.\npress 1  for chicago\npress 2 for new york city\npress 3 for washington\n'))

            city_list = ('chicago', 'new york city', 'washington')

        except Exception as e:
            print('\nPlease check your input!,\n Exception Occurred: {}, \n\n we don\'t have that city on our database\n'.format(e))

        else:
            city = city_list[(city_ref - 1)]
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('What month would you be interested in(Available for Jan - June)? \n input "ALL" if you prefer to see for all months: ').title()
            assert month in ('All', 'January', 'February', 'March', 'April', 'May', 'June')
            break

        except Exception as e:
            print('Please check your input!,\n Exception Occurred: {}, \n\n You could have misspelt something or no data for selected month\n'.format(e))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('What day are you interested in? \n input "ALL" if you prefer to see for all days: ').title()
            assert day in ('All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
            break

        except Exception as e:
            print('Please check your input!,\n Exception Occurred: {}, \n\n You could have misspelt something\n'.format(e))

    print('-'*40 + '\n')
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

    current_DateTime = dat.datetime.now()
    current_date = current_DateTime.date()
    current_year = int(current_date.strftime("%Y"))

    print('\n' + '.'*20 + 'retrieving data\n')
    df = pd.read_csv(CITY_DATA[str(city)])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #drops the  unamed column
    df.drop("Unnamed: 0", axis=1, inplace=True)

    #Adds the age column to the dataset
    if 'Birth Year' in df.columns:
        df['Age'] = current_year - df['Birth Year']
        #create a new column for age class
        df['Age Class'] = np.where(((current_year-2) <= df['Birth Year']) & (df['Birth Year'] < (current_year + 1)), 'Babies (0-2yrs)', 
                                (np.where(((current_year - 16) <= df['Birth Year']) & (df['Birth Year'] < (current_year - 2)),'Children (3-16yrs)',
                                        (np.where(((current_year - 30) <= df['Birth Year']) & (df['Birth Year'] < (current_year - 16)),"Young Adults (17-30yrs)",
                                        (np.where(((current_year - 45) <= df['Birth Year']) & (df['Birth Year'] < (current_year - 30)),"Middle_aged_Adults (31-45yrs)",
                                                    (np.where((df['Birth Year'] < (current_year - 45)),"Old Adults (above 45yrs)","")))))))))
    

    # filter by month if applicable
    if month != 'All':
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == str(month)]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == str(day)]
    

    print('\nData Retrieved!!!\n')
    # Ask if user would like to preview data
    while True:
        try:
            preview = input('\nWould you like to preview the raw data? Enter yes or no.\n').lower()
            break
        except:
            print('oops!!!, check your input and try again\n')

    if preview == 'yes':
        print('\n','.'*10 + "loading city data\n")
        print('\n\n', df.head(), '\n')

        # Ask if user would like to view more raw data and in how many steps
        while True:
            try:
                preview_more = input('\nWould you like to preview more raw data? Enter yes or no.\n').lower()
                start_index = 5
                break
            except:
                print('\noops!!!, check your input and try again\n')

        if preview_more == 'yes':
            while len(df)-1 >= start_index+10:
                while True:
                    try:
                        steps = int(input('How many more rows would you like to see? (number from 1 - 10): \n'))
                        assert steps in range(11)
                        break
                    except:
                        print('\n oops!!!, check your input and try again\n')

                print('\n','.'*10 + "loading {} more rows of city data\n".format(steps))
                print('\n', df.iloc[(start_index + 1):(start_index + 1 +steps)], '\n')
                start_index += steps

                #ask if user would like to view more
                while True:
                    try:
                        see_more = input('\nWould you like to preview more raw data? Enter yes or no.\n').lower()
                        break
                    except:
                        print('\n oops!!!, check your input and try again \n')

                if see_more != 'yes':
                    print('\n\nAlright then, let\'s have a fun experience exploring your selected data.\n')
                    break

    else:
        print('\n\n Alright then, let\'s have a fun experience exploring your selected data.\n')


    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'Start Time' and 'End Time' and 'month' and 'day_of_week' in set(df.columns):
        # TO DO: display the most common month
        if month == 'all':
            most_common_month = df['month'].mode()
            print('\nThe most common month(s) for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
            for value in most_common_month.values:
                print(value)
            

        # TO DO: display the most common day of week
        if day == 'All':
            most_common_dow = df['day_of_week'].mode()
            print('\nThe most common day(s) of the week for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
            for value in most_common_dow.values:
                print(value)
            

        # TO DO: display the most common start hour
        df['start hour'] = df['Start Time'].dt.hour
        most_common_start_hour = df['start hour'].mode()
        print('\nThe most common start hour(s) for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
        for value in most_common_start_hour.values:
            print(value, '(00)hrs')

        # TO DO: display the most common end hour
        df['end hour'] = pd.to_datetime(df['End Time']).dt.hour
        most_common_end_hour = df['end hour'].mode()
        print('\nThe most common end hour(s) for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
        for value in most_common_end_hour.values:
            print(value, '(00)hrs')

        # display a count for total number of completed trips
        trip_count = df['end hour'].count()
        print('\nThe total number of trips for City: {}, Month: {}, Day: {} is:\n{} {}'.format(city,month,day,trip_count,'Trip(s)'))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    if 'Start Station' in set(df.columns):
        common_start_station = df['Start Station'].mode()
        print('\nThe most commonly used start station(s) for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
        for value in  common_start_station.values:
            print(value)

    # TO DO: display most commonly used end station
    if 'End Station' in set(df.columns):
        common_end_station = df['End Station'].mode()
        print('\nThe most commonly used end station(s) for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
        for value in common_end_station.values:
            print(value)

    # TO DO: display most frequent combination of start station and end station trip
    if 'Start Station' in set(df.columns) and 'End Station' in set(df.columns):
        df['Trip Combination'] = df['Start Station'] + ' ' + 'to' + ' ' + df['End Station']
        most_common_trip = df['Trip Combination'].mode()
        print('\nThe most frequent trip(s) for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
        for value in most_common_trip.values:
            print(value)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    if 'Trip Duration' in set(df.columns):
        total_travel_time = df['Trip Duration'].sum()
        print('\nThe total travel time for City: {}, Month: {}, Day: {} is:\n{} {}'.format(city,month,day,total_travel_time,'Seconds'))

    # TO DO: display mean travel time
        mean_travel_time = np.mean(df['Trip Duration'])
        print('\nThe mean travel time for City: {}, Month: {}, Day: {} is:\n{} {}'.format(city,month,day,mean_travel_time,'Seconds'))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in set(df.columns):
        user_type_count = df['User Type'].value_counts()
        print('\nThe User type Count for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day),user_type_count)

    # TO DO: Display counts of gender
    if 'Gender' in set(df.columns):
        gender_count = df['Gender'].value_counts()
        print('\nThe Gender Count for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day),gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in set(df.columns):
        earliest_yob = int(df['Birth Year'].min())
        print('\nThe earliest year of birth of users for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day),earliest_yob)

        most_recent_yob = int(df['Birth Year'].max())
        print('\nThe most recent year of birth of users for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day),most_recent_yob)

        most_common_yob = df['Birth Year'].mode()
        print('\nThe most common year(s) of birth of users for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day))
        for value in most_common_yob.values:
            print(int(value))

    # Display age range distribution of users
    # The code block below was gotten from defltstack.com literature and modified to access current year
    current_DateTime = dat.datetime.now()
    current_date = current_DateTime.date()
    current_year = int(current_date.strftime("%Y"))


    # create new column to label age class distribution
    if 'Birth Year' in df.columns:
        # get count of distinct values in age class column
        age_dist_count = df['Age Class'].value_counts()
        print('\nThe age demographic for City: {}, Month: {}, Day: {} is:\n'.format(city,month,day),age_dist_count)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def plots(df, city, day, month, rows=3, cols=2, dashboard_size=(70, 40)):
    # Create figure and subplots for the Dashboard
    fig, axs = plt.subplots(rows, cols, figsize=dashboard_size)

    fig.suptitle("Dashboard On BikeShare Data in {}".format((city).title()), fontsize=24, fontweight='bold')

    # Color palette for consistency
    palette = sns.color_palette("Set2")

    # Top 10 most popular start hour
    start = df["start hour"].value_counts().iloc[:10]

    # Create a bar plot instead of a count plot
    sns.barplot(x=start.index, y=start.values, ax=axs[0, 1], palette=palette).set(title="Top 10 Most Popular Start Hour")
    axs[0, 1].set_ylabel("Count")
    axs[0, 1].grid(axis='y', linestyle='--', alpha=0.7)
    axs[0, 1].set_yticklabels([])  # Remove y-axis tick labels

    # Top 10 most popular start station
    popular_stations = df["Start Station"].value_counts(ascending=True).iloc[-10:].index

    # Count plot for top 10 most popular start stations
    sns.countplot(data=df[df["Start Station"].isin(popular_stations)], 
                y="Start Station", 
                order=popular_stations, 
                palette=palette, 
                ax=axs[0, 0]).set(title="Top 10 Most Popular Start Station")

    axs[0, 0].set_ylabel("Start Station")
    axs[0, 0].grid(axis='x', linestyle='--', alpha=0.7)
    axs[0, 0].set_xticklabels([])  # Remove x-axis tick labels

    if "Age" in set(df.columns):
        # Removes rows without Age Class Label
        age_df = df[df["Age Class"] != ""]
        # Age class count
        sns.countplot(data=age_df, y=age_df["Age Class"], hue= age_df["Age Class"], legend=False, ax=axs[1, 0], palette=palette).set(title="Age Class Count")
        axs[1, 0].set_ylabel("Count")
        axs[1, 0].grid(axis='x', linestyle='--', alpha=0.7)
        axs[1, 0].set_xticklabels([])  # Remove x-axis tick labels
    else:
        # Average Trip Duration by User Type
        sns.barplot(data=df, x="User Type", y="Trip Duration", estimator=np.mean, ax=axs[1, 0], hue ="Trip Duration", 
                    legend = False, palette=palette).set(title="Average Trip Duration By User Type")
        axs[1, 0].set_ylabel("Average Trip Duration")
        axs[1, 0].grid(axis='y', linestyle='--', alpha=0.7)
        axs[1, 0].set_yticklabels([])  # Remove y-axis tick labels

    if "Gender" in set(df.columns):
        # Total trip by Gender
        sns.barplot(data=df, x="Gender", y="end hour", estimator=np.count_nonzero, ax=axs[1, 1], hue= "Gender", legend = False, palette=palette).set(title="Total Trip By Gender")
        axs[1, 1].set_ylabel("Count of Completed Trips")
        axs[1, 1].grid(axis='y', linestyle='--', alpha=0.7)
        axs[1, 1].set_yticklabels([])  # Remove y-axis tick labels
    else:
        # Total trip by User type
        sns.barplot(data=df, x="User Type", y="end hour", estimator=np.count_nonzero, hue = "User Type", legend =False, ax=axs[1, 1], palette=palette).set(title="Total Trip By User Type")
        axs[1, 1].set_ylabel("Count of Completed Trips")
        axs[1, 1].grid(axis='y', linestyle='--', alpha=0.7)
        axs[1, 1].set_yticklabels([])  # Remove y-axis tick labels

    # Average Trip Duration across Hours
    sns.lineplot(data=df, y="Trip Duration", x="start hour", estimator=np.mean, ax=axs[2, 0], palette=palette).set(title="Average Trip Duration across Hours")
    axs[2, 0].grid(linestyle='--', alpha=0.7)
    axs[2, 0].set_yticklabels([])

    if month == 'All' and day == "All":
        # Total number of Trips Across the days for each month
        sns.lineplot(data=df, hue="month", y="end hour", x="day_of_week", style="month", estimator=np.count_nonzero, ax=axs[2, 1], palette=palette).set(title="Trips Counts Across Days for Each Month")
        plt.xticks(rotation=20)
        axs[2, 1].set_ylabel("NonZero Trip Counts")
        axs[2, 1].grid(linestyle='--', alpha=0.7)
        # axs[2, 1].legend().set_visible(False)
        plt.legend(bbox_to_anchor=(1.02,1),loc='upper left', borderaxespad=0)
        axs[2, 1].set_yticklabels([])

    elif month == "All" and day != "All":
        # Total number of Trips Across months
        sns.lineplot(data=df, x="month", y="end hour", estimator=np.count_nonzero, ax=axs[2, 1], palette=palette).set(title="Trips Counts Across Months")
        plt.xticks(rotation=20)
        axs[2, 1].set_ylabel("NonZero Trip Counts")
        axs[2, 1].grid(linestyle='--', alpha=0.7)
        axs[2, 1].legend().set_visible(False)
        axs[2, 1].set_yticklabels([])

    elif month != 'All' and day == "All":
        # Total number of Trips Across the days
        sns.lineplot(data=df, y="end hour", x="day_of_week", estimator=np.count_nonzero, hue="day_of_week", legend=False, ax=axs[2, 1], palette=palette).set(title="Trips Counts Across Days")
        plt.xticks(rotation=20)
        axs[2, 1].set_ylabel("NonZero Trip Counts")
        axs[2, 1].grid(linestyle='--', alpha=0.7)
        axs[2, 1].legend().set_visible(False)
        axs[2, 1].set_yticklabels([])
    else:
        # Trip count Across the Hours
        sns.lineplot(data=df, x="start hour", y="end hour", estimator=np.count_nonzero, ax=axs[2, 1], palette=palette).set(title="Trips Counts Across Hours")
        plt.xticks(rotation=20)
        axs[2, 1].set_ylabel("NonZero Trip Counts")
        axs[2, 1].grid(linestyle='--', alpha=0.7)
        axs[2, 1].legend().set_visible(False)
        axs[2, 1].set_yticklabels([])

    plt.subplots_adjust(left=0.2, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.5)
    plt.show()








def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        while True:
            '''The next four lines of code does a quick statistical summary of the data.
                You should modify the print statements in their functions above to make the print happen inside the dashboard 
                You should also carry out your own exploratory data analysis to produce insightful charts that can be plotted in the dashboard

            '''
            
            time_stats(df, city, month, day)
            station_stats(df, city, month, day)
            trip_duration_stats(df, city, month, day)
            user_stats(df, city, month, day)

            plots(df= df, month=month,  city = city, day = day)
            

            see_another_stat = input('\nWould you like to see another statistics? Enter yes or no.\n')
            if see_another_stat.lower() != 'yes':
                break



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
