import asyncio
import nest_asyncio
from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import openai
import os
import aiohttp
from datetime import datetime
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# set up the Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# register the blueprints
from apis.auth import auth_bp
from apis.user import user_bp
from apis.billing import billing_bp
from webhooks.stripe import stripe_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(billing_bp, url_prefix='/api/billing')
app.register_blueprint(stripe_bp, url_prefix='/webhooks/stripe')

# set up OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# set up the session
session = aiohttp.ClientSession()

@app.route('/generate_email', methods=['POST'])
def generate_email():
    # get the request data
    request_data = request.get_json()

    # extract the necessary values from the request data
    url = request_data['url']
    sender_info = request_data['sender_info']
    recipient_info = request_data['recipient_info']
    prompt = request_data['prompt']
    word_count = request_data['word_count']

    # get the visible text for the website
    visible_text = get_visible_text(url)

    instructions = generate_instructions_v2(sender_info, recipient_info, prompt, word_count)

    # generate the email using OpenAI's GPT-3
    response = openai.Completion.create(model="text-davinci-003", prompt=visible_text + "\n" + instructions, temperature=0.7, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
    output = response["choices"][0]["text"]

    return output

@app.route('/summarize_website', methods=['POST'])
def summarize_website():
    # get the request data
    data = request.json

    # get the visible text for the website
    visible_text = get_visible_text(data['url'])

    # generate the summary using OpenAI's GPT-3
    response = openai.Completion.create(model="text-davinci-003", prompt="Correct this to standard English and then summarize what this company does in great details:\n" + visible_text, temperature=0, max_tokens=data['word_count'], top_p=1, frequency_penalty=0, presence_penalty=0)
    output = response["choices"][0]["text"]

    return output

# here's another version, simplified
def generate_instructions_v2(sender_info, recipient_info, prompt, word_count):
    instructions = f"You are {sender_info}. Write an email to {recipient_info}. {prompt}. Make it {word_count} words long."
    return instructions

async def scrape_website(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=60) as response:
            # create a BeautifulSoup object with the HTML content of the website
            soup = BeautifulSoup(await response.text(), 'html.parser')

            # find all HTML elements that contain visible text
            text_elements = soup.find_all(text=True)

            # extract the visible text from the text elements
            visible_text = ''
            for element in text_elements:
                if element.parent.name not in ['script', 'style', 'meta', '[document]'] and "<!--" not in str(element) and "-->" not in str(element):
                    visible_text += element.strip() + ' '

            # return the visible text
            return visible_text


def get_visible_text(url):
    # check if an event loop is already running
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # run the scraper in an event loop
    nest_asyncio.apply()
    visible_text = loop.run_until_complete(scrape_website(url))
    return visible_text[:5000]


# website routes
@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/')
@app.route('/playground')
def playground():
    return render_template('playground.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')