from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
app = Flask(__name__)

# Configure your OpenAI key
# openai.api_key = os.getenv('OPENAI_API_KEY')

def init_app(app):
  @app.route('/generate', methods=['POST'])
  def generate():
    data = request.json
    user_input = data.get('userInput')
    print("user input: ", user_input)

    try:
      synopsis = gen_synopsis(user_input)
      title = gen_title(synopsis['synopsis'])
      img_prompt = gen_img_prompt(title['title'], synopsis['synopsis'])
      imgURL = gen_img(img_prompt['img_prompt'])
      return jsonify({'synopsis': synopsis['synopsis'], 'title': title['title'], 'imgURL': imgURL['image_url']})
    except Exception as e:
      print(e)
      return jsonify({'error': str(e)})
      
def gen_synopsis(user_input):
  response = client.completions.create(
          model="text-davinci-003",
          prompt=f""" 
          ###
          outline: A big-headed daredevil fighter pilot goes back to school only to be sent on a deadly mission.
          synopsis: The Top Gun Naval Fighter Weapons School is where the best of the best train to refine their 
          elite flying skills. When hotshot fighter pilot Maverick (Tom Cruise) is sent to the school, 
          his reckless attitude and cocky demeanor put him at odds with the other pilots, especially the cool and 
          collected Iceman (Val Kilmer). But Maverick isn't only competing to be the top fighter pilot, 
          he's also fighting for the attention of his beautiful flight instructor, Charlotte Blackwood (Kelly McGillis). 
          Maverick gradually earns the respect of his instructors and peers - and also the love of Charlotte, 
          but struggles to balance his personal and professional life. As the pilots prepare for a mission against 
          a foreign enemy, Maverick must confront his own demons and overcome the tragedies rooted deep in his past 
          to become the best fighter pilot and return from the mission triumphant.
          ###
          outline: {user_input}
          synopsis: 
          """,
          max_tokens=500
        )
  print("reached here")
  synopsis = response.choices[0].text.strip()
  # print(synopsis)
  # return jsonify({"response": response})
  return {'synopsis': synopsis}

def gen_title(synopsis):
  response = client.completions.create(
          model="text-davinci-003",
          prompt=f"""
          Create a SHORT, crisp, compelling, professional, gripping and enthralling title utilizing the provided synopsis: {synopsis}
        """,
          max_tokens=500
        )
  print("reached here")
  title = response.choices[0].text.strip()
  # print(title)
  # return jsonify({"response": response})
  return  {'title': title}

def gen_img_prompt(title, synopsis):
  response = client.completions.create(
          model="text-davinci-003",
          prompt=f"""
          Give a short description of an image which could be used to advertise a movie based on a title and synopsis. 
          The description should be rich in visual detail but contain no names.
          ###
          title: Love's Time Warp
          synopsis: When scientist and time traveller Wendy (Emma Watson) is sent back to the 1920s to assassinate a future dictator, she never expected to fall in love with them. As Wendy infiltrates the dictator's inner circle, she soon finds herself torn between her mission and her growing feelings for the leader (Brie Larson). With the help of a mysterious stranger from the future (Josh Brolin), Wendy must decide whether to carry out her mission or follow her heart. But the choices she makes in the 1920s will have far-reaching consequences that reverberate through the ages.
          image description: A silhouetted figure stands in the shadows of a 1920s speakeasy, her face turned away from the camera. In the background, two people are dancing in the dim light, one wearing a flapper-style dress and the other wearing a dapper suit. A semi-transparent image of war is super-imposed over the scene.
          ###
          title: zero Earth
          synopsis: When bodyguard Kob (Daniel Radcliffe) is recruited by the United Nations to save planet Earth from the sinister Simm (John Malkovich), an alien lord with a plan to take over the world, he reluctantly accepts the challenge. With the help of his loyal sidekick, a brave and resourceful hamster named Gizmo (Gaten Matarazzo), Kob embarks on a perilous mission to destroy Simm. Along the way, he discovers a newfound courage and strength as he battles Simm's merciless forces. With the fate of the world in his hands, Kob must find a way to defeat the alien lord and save the planet.
          image description: A tired and bloodied bodyguard and hamster standing atop a tall skyscraper, looking out over a vibrant cityscape, with a rainbow in the sky above them.
          ###
          title: {title}
          synopsis: {synopsis}
          image description: 
          """,
          max_tokens=500
        )
  print("reached here")
  img_prompt = response.choices[0].text.strip()
  return  {'img_prompt': img_prompt}

def gen_img(img_prompt):
  response = client.images.generate(
  model="dall-e-2",
  prompt=img_prompt,
  size="512x512",
  quality="standard",
  n=1,
  )
  print("reached here")
  image_url = response.data[0].url
  return  {'image_url': image_url}
