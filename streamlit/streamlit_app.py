import streamlit as st
import requests

# Streamlit app
st.title("Unicode API")
st.write("Retrieve information about Unicode characters by entering their decimal ID.")

# Input for character ID
character_id = st.number_input(
    "Enter Unicode Character ID in Decimal:",
    min_value=0,
    step=1,
    help="Provide a valid Unicode character ID (e.g., 65 for 'A')."
)

# Automatically retrieve and display character data
if character_id is not None:
    with st.spinner("Fetching character data..."):
        try:
            response = requests.get(f"http://127.0.0.1:8000/characters/{character_id}")
            if response.status_code == 200:
                data = response.json()
                print(data)
                for key, value in data.items():
                    print(key)
                    if key == "Image":
                        st.image(value, width=500)
                    else:
                        display_key = "ID" if key == "ID" else key.capitalize()
                        st.write(f"**{display_key}:** {value}")
            else:
                st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Unable to connect to the API. Make sure the FastAPI server is running: {e}")

with st.expander("### List of Characters"):
    with st.spinner("Fetching character data..."):
        try:
            response = requests.get(f"http://127.0.0.1:8000/list_characters/")
            if response.status_code == 200:
                data = response.json()
                for character in data:
                        st.write(f"{character['ID']} - {character['Name']}")
            else:
                st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Unable to connect to the API. Make sure the FastAPI server is running: {e}")


# Section for submitting new Unicode character data
with st.expander("### Submit New Unicode Character Data"):
    new_character_id = st.number_input(
        "Enter New Unicode Character ID in Decimal:",
        min_value=0,
        step=1,
        help="Provide a valid Unicode character ID for submission."
    )
    new_character_name = st.text_input(
        "Enter Character Name:",
        help="Provide the name of the Unicode character."
    )
    new_character_category = st.text_input(
        "Enter Character Category:",
        help="Provide the category of the Unicode character."
    )
    new_character_gender = st.text_input(
        "Enter Character Gender:",
        help="Provide the gender of the Unicode character."
    )
    new_character_colour = st.text_input(
        "Enter Character Colour:",
        help="Provide the colour of the Unicode character."
    )
    new_character_desc = st.text_input(
        "Enter Character Description:",
        help="Provide the description of the Unicode character."
    )

    if st.button("Submit Character Data"):
        if new_character_id is not None and new_character_name and new_character_category and new_character_gender and new_character_colour:
            print("submitting character now")
            with st.spinner("Submitting character data..."):
                try:
                    payload = {"ID": new_character_id, "Name": new_character_name, "Category": new_character_category, "Gender": new_character_gender, "Colour": new_character_colour, "Description": new_character_desc}
                    response = requests.post("http://127.0.0.1:8000/characters", json=payload)
                    if response.status_code == 200:
                        st.success("Character data submitted successfully!")
                    else:
                        st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Unable to connect to the API. Make sure the FastAPI server is running.")
        else:
            st.warning("Please provide both a valid ID, name, gender, and colour for the character.")