import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import helper
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide"
)

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file (.txt)")

if uploaded_file is not None:

    # =======================
    # READ FILE
    # =======================
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # =======================
    # PREPROCESS
    # =======================
    df = preprocessor.preprocess(data)

    # =======================
    # USER LIST
    # =======================
    user_list = df['user'].unique().tolist()

    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "Show analysis wrt",
        user_list
    )

    if st.sidebar.button("Show Analyze"):

        # =======================
        # TOP STATS
        # =======================
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # =======================
        # DAILY TIMELINE
        # =======================
        st.header("Daily timeline ")

        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        ax.set_xlabel("Time")
        ax.set_ylabel("Messages")
        st.pyplot(fig)

        st.dataframe(timeline)

        # =======================
        # DAILY TIMELINE
        # =======================
        st.subheader("Monthly Timeline")

        daily = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'])
        plt.xticks(rotation='vertical')
        ax.set_xlabel("Date")
        ax.set_ylabel("Messages")
        st.pyplot(fig)

        # =======================
        # BUSIEST USERS
        # =======================
        if selected_user == "Overall":

            st.title("Most Busy Users")

            x = df['user'].value_counts(normalize=True) * 100

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                percent_df = (
                    df['user']
                    .value_counts(normalize=True)
                    .mul(100)
                    .reset_index()
                )
                percent_df.columns = ['User', 'Percentage']
                st.dataframe(percent_df)

        # =======================
        # ACTIVITY MAP
        # =======================
        st.title("Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='red')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # =======================
        # WORD CLOUD
        # =======================
        st.title("Word Cloud ☁️")

        wc = helper.create_wordcloud(selected_user, df)

        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # =======================
        # MOST COMMON WORDS
        # =======================
        st.title("Most Common Words")

        common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(common_df[0], common_df[1], color='red')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.dataframe(common_df)

        # =======================
        # EMOJI ANALYSIS
        # =======================
        st.title("Emoji Analysis 😊")

        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.barh(emoji_df['emoji'].head(10), emoji_df['count'].head(10))
            st.pyplot(fig)

        # =======================
        # HEATMAP
        # =======================
        st.title("🔥 Activity Heatmap")

        heatmap = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots()
        sns.heatmap(heatmap, ax=ax)
        st.pyplot(fig)
