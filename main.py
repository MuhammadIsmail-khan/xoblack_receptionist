import streamlit as st
import speech_recognition as sr
from openai import OpenAI
import pyttsx3
import google.generativeai as genai 

from database import check_calling
import json
import pandas as pd
import sqlalchemy as sa
import base64

def decode_api_key(encoded_api_key):
    decoded_bytes = base64.b64decode(encoded_api_key.encode('utf-8'))
    decoded_str = str(decoded_bytes, 'utf-8')
    return decoded_str

api_key=decode_api_key("QUl6YVN5RDBmMmd4dExwSEd5cWVZOFdWQ1FkaHpsVEdWZU80U0RJ")
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]
genai.configure(api_key=api_key)
model=genai.GenerativeModel(model_name="gemini-pro",safety_settings=safety_settings)


dbschema="""
        conn = sqlite3.connect("pizza_db.db")
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS customer_info (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                phone_number INT NOT NULL,
                address VARCHAR(100) NOT NULL
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS pizza_info (
                pizza_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price INT NOT NULL
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS orders_info (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INT NOT NULL,
                order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                total_amount DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customer_info(customer_id)
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INT NOT NULL,
                pizza_id INT NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders_info(order_id),
                FOREIGN KEY (pizza_id) REFERENCES pizza_info(pizza_id)
            )''')

            conn.commit()
            cursor.close()
            conn.close()


"""

def make_query(user_query,dbSchema):
  print("user query : ------------------  ",user_query)
  prompt=f"""
    You are a sqlite database expert
    your task is to get the user intent and make sqlite3 query  for database_schema based on user_query
    you will make sqlite3 query to perform on of (create, read, update or delete operation) also provide which operation is it
    Only provide sqlite3 query do not provide any explanation or any other inofrmation and also provide type
    provide the query in json format
    if there is any information which do not fit in database_schema , then ignore that informaation 

    user_query: {user_query}

    database_schema:
    {
        dbschema
    }
    example :
    user_query:
      which pizza do you have in range 800-900
    query:
  """+"""
      {
          "query": "SELECT name FROM pizza_info WHERE price BETWEEN 800 AND 900",
          "type": "read"
      }
  """
  response=model.generate_content(prompt)
  return response.text


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        
        print("text--------- : ",text)
        st.write("You said: " + text)
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand audio")
    except sr.RequestError as e:
        st.write("Request failed; {0}".format(e))
    return None

def convert_text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def show_table():
  connection_string = "sqlite:///pizza_db.db"

  # Establish connection
  engine = sa.create_engine(connection_string)

  # Fetch data from a table
  query = "SELECT * FROM customer_info"
  df = pd.read_sql(query, engine)
  new_column_names = ["Customer ID","Name","Phone Number","Address"]  # Provide names for all columns
  df.columns = new_column_names
  # Display the DataFrame
  st.dataframe(df)

def main():
    st.title("AI Receptionist")
    if st.button("Say something"):
        text = recognize_speech()
        if text:
            llm_response=make_query(text,dbschema)
            print("----------     llm response : ",llm_response)
            print("--------       llm response type : ",type(llm_response))
            query=json.loads(llm_response)
            print(f"Sql query  : {query} ---------------------------------")
            response = check_calling(query["type"],query["query"])
            if type(response) == list:
                for i in response:
                    st.text(i)
            else:
                st.text(str(response))
            convert_text_to_speech(response)
        
    



if __name__ == "__main__":
    main()
