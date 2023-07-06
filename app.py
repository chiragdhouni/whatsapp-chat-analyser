import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title("whatsapp_chat_analyser")
uploaded_file=st.sidebar.file_uploader("upload a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)

    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("show_analysis"):
        #fetching information from helper function
        num_messages,total_words,total_media,total_links=helper.fetch_stats(df,selected_user)
        #stat area

        st.title("top_statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("total_messages")
            st.title(num_messages)
        with col2:
            st.header("total_words")
            st.title(total_words)
        with col3:
            st.header("total_media")
            st.title(total_media)
        with col3:
            st.header("total_links")
            st.title(total_links)

        #most_busy_user(df level ,not user level)
        if selected_user=="overall":
            st.title("most_busy_users")

            col1,col2=st.columns(2)
            busy_users,new_df=helper.most_busy_users(df)
            fig, ax = plt.subplots()

            with col1:
                ax.bar(busy_users.index, busy_users.values,color='red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # st.title("Wordcloud")
        # df_wc = helper.create_wordcloud(selected_user,df)
        # fig, ax = plt.subplots()
        # ax.imshow(df_wc)
        # st.pyplot(fig)
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        st.title("most common words ")
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='red')
        st.pyplot(fig)


        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title("activity map")
        col1,col2=st.columns(2)
        with col1:
            st.header("most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("most busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


