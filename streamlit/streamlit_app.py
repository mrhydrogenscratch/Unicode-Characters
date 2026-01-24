import streamlit as st
import requests

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
                st.subheader(f"Character Details for ID: {character_id}")
                st.image(data.get("Image"), width=500)
                st.write(f"**Name:** {data.get('Name')}")
                st.write(f"**Category:** {data.get('Category')}")
                st.write(f"**Gender:** {data.get('Gender')}")
                st.write(f"**Colour:** {data.get('Colour')}")
                st.write(f"**Description:** {data.get('Description')}")
            else:
                st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Unable to connect to the API. Make sure the FastAPI server is running: {e}")

st.title("List of Characters")
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
st.title("Submit New Unicode Character Data")
st.write("Fill out the form below to add a new Unicode character.")
with st.form("character_form"):
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
        new_character_desc = st.text_area(
            "Enter Character Description:",
            help="Provide the description of the Unicode character."
        )
        new_character_image = st.file_uploader(
            "Upload Character Image:",
            type=["png", "jpg", "jpeg"],
            help="Upload an image file for the character."
        )

        submitted = st.form_submit_button("Submit Character Data")
        if submitted:
            if new_character_id and new_character_name and new_character_category and new_character_gender and new_character_colour:
                with st.spinner("Submitting character data..."):
                    try:
                        # Convert image to base64 if uploaded
                        image_path = None
                        if new_character_image:
                            image_path = f"images/{new_character_id}_{new_character_image.name}"
                            with open(image_path, "wb") as f:
                                f.write(new_character_image.getbuffer())

                        # Prepare payload
                        payload = {
                            "ID": new_character_id,
                            "Name": new_character_name,
                            "Category": new_character_category,
                            "Gender": new_character_gender,
                            "Colour": new_character_colour,
                            "Description": new_character_desc,
                            "Image": image_path
                        }

                        # Send POST request to API
                        response = requests.post("http://127.0.0.1:8000/characters", json=payload)
                        if response.status_code == 200:
                            st.success("Character submitted successfully!")
                        else:
                            st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Unable to connect to the API. Make sure the FastAPI server is running: {e}")
            else:
                st.warning("Please fill out all required fields.")