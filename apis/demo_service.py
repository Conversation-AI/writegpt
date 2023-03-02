import asyncio
import nest_asyncio
from flask import Blueprint, request
from bs4 import BeautifulSoup
import openai
import os
import aiohttp

# set up OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

demo_service_bp = Blueprint('demo_service', __name__)

@demo_service_bp.route('/generate_email', methods=['POST'])
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

    # # generate the email using OpenAI's GPT-3
    # response = openai.Completion.create(model="text-davinci-003", prompt=visible_text + "\n" + instructions, temperature=0.7, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
    # output = response["choices"][0]["text"]

    # generate the email using OpenAI's ChatGPT API
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a highly exprienced outbound sales lead generation expert who writes cold emails that appears to be hyper-personalized based on the recipient's context. Your emails appear to be from thorough research and personal. You are good at writing high conversion emails that make people want to book meetings. You don't write emails that appear to be mass generated or spam."},
            {"role": "system", "content": "You can only use information provided to you by the user. You cannot make up numbers which you do not know is true. "},
            {"role": "system", "content": "You will write email within the word limit. You will not write more than required words."},
            {"role": "user", "content": instructions}
        ]
    )
    print("completion:", completion)
    output = completion["choices"][0]["message"]["content"]

    return output

@demo_service_bp.route('/summarize_website', methods=['POST'])
def summarize_website():
    # get the request data
    data = request.json

    # get the visible text for the website
    visible_text = get_visible_text(data['url'])

    # generate the summary using OpenAI's GPT-3
    # response = openai.Completion.create(model="text-davinci-003", prompt="Correct this to standard English and then summarize what this company does in great details:\n" + visible_text, temperature=0, max_tokens=data['word_count'], top_p=1, frequency_penalty=0, presence_penalty=0)
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": f"Correct this website content to standard English and then summarize what this company does, the market it's in, it's main target customers, and value propositions, in great details (under 500 words):\n{visible_text}"}
        ]
    )
    print("completion:", completion)
    output = completion["choices"][0]["message"]["content"]

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