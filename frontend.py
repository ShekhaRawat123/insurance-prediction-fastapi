import streamlit  as st
import requests

API_URL = "http://127.0.0.1:8000/predict"
st.title("insorance predict company")
st.markdown("enter your detail below")
age = st.number_input("age", min_value=1, max_value=100, value=30 )
weight = st.number_input("wait", min_value= 0 , max_value=100, value =45) 
height = st.number_input("height" , min_value=1 , max_value= 300, value= 10)
income_lpa = st.number_input("salari in lpa", min_value=1 , value= 1)
smoker = st.selectbox("are smoker", options=[True, False] )
city = st.text_input("enter your  city name", value= "Mumbai")
occupation =st.selectbox("occupation" , [ "retired", "freelancer", "student",  'government_job', 'business_owner', 'unemployed', 'private_job' ,  ])

if st.button("predict input detail"):
    input_data = {
        "age" : age,
        "weight" : weight,
        "height" : height,
        "income_lpa" : income_lpa,
        "smoker" : smoker,
        "city" : city,
        "occupation" : occupation 
    }

    try:
        response = requests.post(API_URL, json = input_data)
        result = response.json()
        
        if response.status_code == 200 :
            predicted_value = result["predicted_category"]
            st.success(f"Predicted Premium Category: **{predicted_value}**")
            

            
        else:
            st.error(f"API Error: {response.status_code}")
            

    except requests.exceptions.ConnectionError:
        st.error(" Could not connect to the FastAPI server. Make sure it's running.")



