import asyncio
import nest_asyncio
from flask import Blueprint, request
from bs4 import BeautifulSoup
import openai
import os
import aiohttp
from apis.decorators import api_key_required
from helpers.record_usage import update_usage_record_by_user

# set up OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

service_bp = Blueprint('service', __name__)

@service_bp.route('/generate_email', methods=['POST'])
@api_key_required
def generate_email(user):
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

    # update the usage record for the user
    update_usage_record_by_user(user)

    return output

@service_bp.route('/summarize_website', methods=['POST'])
@api_key_required
def summarize_website(user):
    # get the request data
    data = request.json

    # get the visible text for the website
    visible_text = get_visible_text(data['url'])

    # # generate the summary using OpenAI's GPT-3
    # response = openai.Completion.create(model="text-davinci-003", prompt="Correct this to standard English and then summarize what this company does in great details:\n" + visible_text, temperature=0, max_tokens=data['word_count'], top_p=1, frequency_penalty=0, presence_penalty=0)
    # output = response["choices"][0]["text"]

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": f"Correct this website content to standard English and then summarize what this company does in great details:\n{visible_text}"}
        ]
    )
    output = completion["choices"][0]["message"]["content"]

    # update the usage record for the user
    update_usage_record_by_user(user)

    return output

# here's another version, simplified
def generate_instructions_v2(sender_info, recipient_info, prompt, word_count):
    instructions = f"You are {sender_info}. Write an email to {recipient_info}. {prompt}. Write it below {word_count} words."
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