from google import genai

client = genai.Client(api_key="AIzaSyCkNyt3QUfzGiveZZzDicMK6p6RabJ55gA")

response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="Give me 3 hopeful book quotes"
)

print(response.text)

# i cannot get the key to work, Rumaisa or Maya can create one from their laptop
# when they are done then we can re-test it 