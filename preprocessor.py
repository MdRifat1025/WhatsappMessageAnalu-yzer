import re
import pandas as pd

def preprocess(data):
    # Pattern to match datetime and message
    pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?(?:AM|PM)?) - (.*)")

    matches = pattern.findall(data)

    df = pd.DataFrame(matches, columns=["date", "user_message"])

    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y, %I:%M %p", errors="coerce")

    users = []
    messages = []
    for message in df['user_message']:
        # Split between "username: message"
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:  # Case: normal message
            users.append(entry[1])
            messages.append(entry[2])
        else:  # Case: group notification
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional time features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create period column (hour ranges)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour+1}")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df
