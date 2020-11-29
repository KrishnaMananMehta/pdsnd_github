import datetime
import pandas as pd
import calendar


def get_city():
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n').title()
    if city == 'Chicago':
        return 'chicago.csv'
    elif city == 'New York':
        return 'new_york_city.csv'
    elif city == 'Washington':
        return 'washington.csv'
    else:
        print("\nWe did not understand, please try again")
        return get_city()


def get_time_period():
    time_period = input('\nWould you like to filter the data by month, day, none.\n').lower()
    if time_period == 'month':
        return ['month', get_month()]
    elif time_period == 'day':
        return ['day', get_day()]
    elif time_period == 'none':
        return ['none', 'no filter']
    else:
        print("\nI'm sorry, I'm not sure which time period you're trying to filter by. Let's try again.")
        return get_time_period()


def get_month():
    month = input('\nWhich month? January, February, March, April, May, or June?\n').title()
    if month == 'January':
        return '01'
    elif month == 'February':
        return '02'
    elif month == 'March':
        return '03'
    elif month == 'April':
        return '04'
    elif month == 'May':
        return '05'
    elif month == 'June':
        return '06'
    else:
        print("\nWe did not understand, please try again.")
        return get_month()


def get_day():
    day_of_week = input(
        '\nWhich day of the week would you like your data for? Mpnday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
    if day_of_week == 'Monday':
        return 0
    elif day_of_week == 'Tuesday':
        return 1
    elif day_of_week == 'Wednesday':
        return 2
    elif day_of_week == 'Thursday':
        return 3
    elif day_of_week == 'Friday':
        return 4
    elif day_of_week == 'Saturday':
        return 5
    elif day_of_week == 'Sunday':
        return 6
    else:
        print("\nI'm sorry I did not understand, please try again.")
        return get_day()


def popular_month(df):
    tbm = df.groupby('Month')['Start Time'].count()
    return "Most popular month for start time was: " + calendar.month_name[
        int(tbm.sort_values(ascending=False).index[0])]


def popular_day(df):
    tbdow = df.groupby('Day of Week')['Start Time'].count()
    return "Most popular day of the week for start time was: " + calendar.day_name[
        int(tbdow.sort_values(ascending=False).index[0])]


def popular_hour(df):
    tbhod = df.groupby('Hour of Day')['Start Time'].count()
    mphi = tbhod.sort_values(ascending=False).index[0]
    d = datetime.datetime.strptime(mphi, "%H")
    return "Most popular hour of the day for start time: " + d.strftime("%I %p")


def trip_duration(df):
    total_trip_duration = df['Trip Duration'].sum()
    avg_trip_duration = df['Trip Duration'].mean()
    m, s = divmod(total_trip_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    ttd = "\nTotal trip duration: %d years %02d days %02d hrs %02d min %02d sec" % (y, d, h, m, s)
    m, s = divmod(avg_trip_duration, 60)
    h, m = divmod(m, 60)
    atd = "Average trip duration: %d hrs %02d min %02d sec" % (h, m, s)
    return [ttd, atd]


def popular_stations(df):
    ssc = df.groupby('Start Station')['Start Station'].count()
    esc = df.groupby('End Station')['End Station'].count()
    sss = ssc.sort_values(ascending=False)
    ses = esc.sort_values(ascending=False)
    tt = df['Start Station'].count()
    mpss = "\nMost popular start station: " + sss.index[0] + " (" + str(
        sss[0]) + " trips, " + '{0:.2f}%'.format(
        ((sss[0] / tt) * 100)) + " of trips)"
    mpes = "Most popular end station: " + ses.index[0] + " (" + str(
        ses[0]) + " trips, " + '{0:.2f}%'.format(
        ((ses[0] / tt) * 100)) + " of trips)"
    return [mpss, mpes]


def popular_trip(df):
    tc = df.groupby(['Start Station', 'End Station'])['Start Time'].count()
    sts = tc.sort_values(ascending=False)
    tt = df['Start Station'].count()
    return "Most popular trip: " + "\n  Start station: " + str(
        sts.index[0][0]) + "\n  End station: " + str(sts.index[0][1]) + "\n  (" + str(
        sts[0]) + " trips, " + '{0:.2f}%'.format(
        ((sts[0] / tt) * 100)) + " of trips)"


def users(df):
    utc = df.groupby('User Type')['User Type'].count()
    return utc


def gender(df):
    gc = df.groupby('Gender')['Gender'].count()
    return gc


def birth_years(df):
    eby = "Earliest birth year: " + str(int(df['Birth Year'].min()))
    mrby = "Most recent birth year: " + str(int(df['Birth Year'].max()))
    byc = df.groupby('Birth Year')['Birth Year'].count()
    sby = byc.sort_values(ascending=False)
    tt = df['Birth Year'].count()
    mcby = "Most common birth year: " + str(int(sby.index[0])) + " (" + str(
        sby.iloc[0]) + " trips, " + '{0:.2f}%'.format(
        ((sby.iloc[0] / tt) * 100)) + " of trips)"
    return [eby, mrby, mcby]


def display_data(df, current_line):
    display = input('\nWould you like to view individual trip data?'
                    ' Type \'yes\' or \'no\'.\n')
    display = display.lower()
    if display == 'yes' or display == 'y':
        print(df.iloc[current_line:current_line + 5])
        current_line += 5
        return display_data(df, current_line)
    if display == 'no' or display == 'n':
        return

    else:
        print("\nI'm sorry, I'm not sure if you wanted to see more data or not. Let's try again.")
        return display_data(df, current_line)


def statistics():
    city = get_city()
    cdf = pd.read_csv(city)

    def gdow(str_date):
        do = datetime.date(int(str_date[0:4]), int(str_date[5:7]), int(str_date[8:10]))
        return do.weekday()

    cdf['Day of Week'] = cdf['Start Time'].apply(gdow)
    cdf['Month'] = cdf['Start Time'].str[5:7]
    cdf['Hour of Day'] = cdf['Start Time'].str[11:13]
    tp = get_time_period()
    fp = tp[0]
    fpv = tp[1]
    fpl = 'No filter'
    if fp == 'none':
        filtered_df = cdf
    elif fp == 'month':
        filtered_df = cdf.loc[cdf['Month'] == fpv]
        fpl = calendar.month_name[int(fpv)]
    elif fp == 'day':
        filtered_df = cdf.loc[cdf['Day of Week'] == fpv]
        fpl = calendar.day_name[int(fpv)]
    print('\n')
    print(city[:-4].upper().replace("_", " ") + ' -- ' + fpl.upper())

    print('Total trips: ' + "{:,}".format(filtered_df['Start Time'].count()))
    if fp == 'none' or fp == 'day':
        print(popular_month(filtered_df))
    if fp == 'none' or fp == 'month':
        print(popular_day(filtered_df))
    print(popular_hour(filtered_df))
    trip_duration_stats = trip_duration(filtered_df)
    print(trip_duration_stats[0])
    print(trip_duration_stats[1])
    most_popular_stations = popular_stations(filtered_df)
    print(most_popular_stations[0])
    print(most_popular_stations[1])
    print(popular_trip(filtered_df))
    print(users(filtered_df))
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print(gender(filtered_df))
        birth_years_data = birth_years(filtered_df)
        print(birth_years_data[0])
        print(birth_years_data[1])
        print(birth_years_data[2])
    display_data(filtered_df, 0)

    def restart_question():
        restart = input(
            '\nWould you like to restart? Type \'yes\' or \'no\'. (If you say no it will end the program.)\n')
        if restart.lower() == 'yes' or restart.lower() == 'y':
            statistics()
        elif restart.lower() == 'no' or restart.lower() == 'n':
            return
        else:
            print("\nI'm not sure if you wanted to restart or not. Let's try again.")
            return restart_question()

    restart_question()


if __name__ == "__main__":
    statistics()
