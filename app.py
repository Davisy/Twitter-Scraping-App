import streamlit as st
import twint
import pandas as pd


# add banner image
st.header("Data Scraper App")
st.image('images/twitter.jpg')
st.subheader('''
A simple app to scrap data from Twitter.
''')

# form to collect searcy query and other conditions
my_form = st.form(key='Twitter_form')
search_query = my_form.text_input('Input your search query')
data_limit = my_form.slider('How many tweets do you want to get?', 
                    10, 
                    3000, 
                    value= 100,
                    step=10)

output_csv = my_form.radio('Save data to a CSV file?', 
                        ['Yes', 'No'])
file_name = my_form.text_input('Name the CSV file:')
submit = my_form.form_submit_button(label='Search')

# function to show output in pandas dataframe with specific folumns 
def twint_to_pd(columns):
  return twint.output.panda.Tweets_df[columns]

# configure twint to serach the query
if submit:
    config = twint.Config()
    config.Search = search_query
    config.Limit = data_limit
    config.Pandas = True
    if output_csv == "Yes":
        config.Store_csv = True
        config.Output = 'data/{}.csv'.format(file_name)
    twint.run.Search(config)

    st.subheader("Results: Sample Data")
    if output_csv == "Yes":
        # show data in pandas dataframe
        data = pd.read_csv('data/{}.csv'.format(file_name),usecols=['date','username','tweet'])
        st.table(data)
    else:
        data = twint_to_pd(["date","username","tweet"])
        st.table(data)
        
    
    #download the dataframe
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(data)

    st.download_button(
        label="Download scrapped data as CSV",
        data=csv,
        file_name='{}.csv'.format(file_name),
        mime='text/csv',
 )