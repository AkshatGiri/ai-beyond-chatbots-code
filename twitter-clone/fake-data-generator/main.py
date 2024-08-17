from pydantic import BaseModel
from openai import OpenAI
import json_fix


client = OpenAI(api_key="<your-api-key>")

class Persona(BaseModel):
    name: str
    age: int
    occupation: str
    behaviour: str
    
    def __json__(self):
        return {
            "name": self.name,
            "age": self.age,
            "occupation": self.occupation,
            "behaviour": self.behaviour
        }

class Tweet(BaseModel):
    content: str
    likes: int
    retweets: int
    
    def __json__(self):
      return {
        "content": self.content,
        "likes": self.likes,
        "retweets": self.retweets
      }
    
def generatePersona():
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a persona geneartor. You make up a human character, with their name, age, occupation and their behavioural characteristics."},
            {"role": "user", "content": "Generate a persona."},
        ],
        response_format=Persona,
    )

    persona = completion.choices[0].message.parsed
    
    print(persona)

    return Persona(name=persona.name, age=persona.age, occupation=persona.occupation, behaviour=persona.behaviour)
  

personas = []
for i in range(5):
    personas.append(generatePersona())
    
for persona in personas:
    print(persona)
    print('--------------------')


def generateTweet(persona: Persona, event: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a tweet generator. You have to generate a tweet for a given persona and a current event."},
            {"role": "user", "content": f"Generate a tweet for the following persona: \n Name - {persona.name} \n Age - {persona.age} \n Occupation - {persona.occupation} \n Behaviour - {persona.behaviour} \n Event - {event}"},
        ],
        response_format=Tweet,
    )

    tweet = completion.choices[0].message.parsed
    
    print(tweet)

    return Tweet(content=tweet.content, likes=tweet.likes, retweets=tweet.retweets)
  
users = []


event = "The halvening from the Avengers franchise has just taken place. Half of all living organisms are now gone."

for persona in personas:
    tweet = generateTweet(persona, event)
    users.append({ "persona": persona, "tweets": [tweet]})


for user in users:
  print(user)
  
# save users to json
import json

with open('users.json', 'w') as f:
    json.dump(users, f)