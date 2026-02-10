import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji
import re


# =======================
# STATS
# =======================
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = df['message'].apply(lambda x: len(x.split())).sum()
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(re.findall(r'http\S+', message))

    return num_messages, words, num_media_messages, len(links)


# =======================
# MONTHLY TIMELINE
# =======================
def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = (
        df.groupby(['year', 'month_name', 'month'])
        .count()['message']
        .reset_index()
    )

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


# =======================
# DAILY TIMELINE
# =======================
def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily = df.groupby('only_date').count()['message'].reset_index()
    return daily


# =======================
# ACTIVITY MAP
# =======================
def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


# =======================
# WORD CLOUD
# =======================
def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['message'] != '<Media omitted>\n']

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    text = " ".join(df['message'])
    return wc.generate(text)


# =======================
# MOST COMMON WORDS
# =======================
def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            words.append(word)

    common_df = pd.DataFrame(Counter(words).most_common(20))
    return common_df


# =======================
# EMOJI ANALYSIS
# =======================
def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])
    return emoji_df


# =======================
# HEATMAP
# =======================
def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return heatmap
