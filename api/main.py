from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()


def get_characters():
    # Load the JSON data
    file_path = Path(__file__).parent / "characters.json"
    with open(file_path, "r") as file:
        characters = json.load(file)
    return characters

@app.get("/characters/{character_id}")
def get_character(character_id: int):
    # Check if the character exists
    characters = get_characters()
    character = characters.get(str(character_id))
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.post("/characters")
def add_character(character: dict):
    character_id = str(character.get("ID"))
    characters = get_characters()
    if not character_id or not character.get("Name"):
        raise HTTPException(status_code=400, detail="Missing required fields: id or name.")
    
    # Check for duplicate ID
    if character_id in characters:
        raise HTTPException(status_code=400, detail="Character with this ID already exists.")
    
    # Add the new character
    characters[character_id]={
        "ID": character_id,
        "Name": character.get("Name"),
        "Category": character.get("Category"),
        "Gender": character.get("Gender"),
        "Colour": character.get("Colour"),
        "Description": character.get("Description")
    }

    # Save dictionary to a JSON file
    file_path = Path(__file__).parent / "characters.json"
    with open(file_path, "w") as json_file:
        json.dump(characters, json_file, indent=4)  # `indent=4` makes the JSON file more readable


