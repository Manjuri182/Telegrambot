import streamlit as st
import pandas as pd
import requests
import re
import time
import datetime

# Function to send message via Telegram bot
def telegram_bot_sendtext(bot_message):
    bot_token = '1022661921:AAFSCX73U3iNoRlNTVKbM5RumEuu4pQQ8lY'
    bot_chatID = '@EducasJOBS'
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)
    return response.json()

# Function to remove text within parentheses and square brackets
def strip_character(dataCol):
    r = re.compile(r'[\(\[].*?[\)\]]')
    return r.sub('', dataCol)

# Function to process CSV and send messages
def process_and_send_csv(file_path):
    ind = 0
    df = pd.read_csv(file_path)
    df = df.dropna()
    df.About_Work = df.About_Work.str.replace(r'Selected interns day-to-day responsibilities include:', '').str.replace('Only those', '')
    x = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    x['ApplyBy'] = pd.to_datetime(x['ApplyBy']).map(lambda x: x.strftime('%d-%m-%Y'))
    x = x.sort_values('ApplyBy', ascending=False).reset_index(drop=True)
    x.Skills = x.Skills.apply(strip_character)
    y = x.iloc[ind:ind+6]
    
    for index, row in y.iterrows():
        JobTItle = row['JobTItle']
        Company = row['Company']
        URL = row['Url']
        StartDate = row['StartDate']
        Duration = row['Duration']
        Stipend = row['Stipend']
        ApplyBy = row['ApplyBy']
        About_Company = row['About_Company']
        About_Work = row['About_Work']
        Skills = row['Skills']
        
        message = (
            f"\n*JobTitle :*  {JobTItle}\n"
            f"*Company :*  {Company}\n"
            f"*Url :*  {URL}\n"
            f"*StartDate :*  {StartDate}\n"
            f"*Duration :*  {Duration}\n"
            f"*Stipend :*  {Stipend}\n"
            f"*ApplyBy :*  {ApplyBy}\n"
            f"*Skills :*  {Skills}\n"
            "\n*For More Updates*: [Register here](https://forms.gle/ayhd1WyafUKijJm79) \n"
        )
        
        time.sleep(10)
        telegram_bot_sendtext(message)
        st.write(f"Message sent for Index {index} at {datetime.datetime.now()}")
        
    ind = y.index[-1]
    st.write(f"Resetting Index = {ind}")

st.title("CSV Upload and Telegram Bot")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Save the uploaded file
    with open("uploaded_file.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully")

    # Process and send CSV
    if st.button("Process and Send CSV"):
        process_and_send_csv("uploaded_file.csv")
        st.success("CSV processed and messages sent")
