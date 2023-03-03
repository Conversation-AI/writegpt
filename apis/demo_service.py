import asyncio
import nest_asyncio
from flask import Blueprint, request
from bs4 import BeautifulSoup
import openai
import os
import aiohttp
from helpers.google_search import google_search
import json
import datetime

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
    # if prompt is provided, use it; otherwise set it to empty string
    if 'prompt' not in request_data:
        prompt = ''
    else:
        prompt = request_data['prompt']
    word_count = request_data['word_count']
    # if template is provided, use it; otherwise set it to empty string
    if 'template' not in request_data:
        template = ""
    else:
        template = request_data['template']
    
    # knowledge_base = request_data['knowledge_base']
    # knowledge_base is an array of objects, each containing a title and description
    if 'knowledge_base' not in request_data:
        knowledge_base = []
    else:
        knowledge_base = request_data['knowledge_base']

    if 'search_on_google' not in request_data:
        search_on_google = False
    else:
        search_on_google = request_data['search_on_google']


    # parse knowledge base and add to prompt
    knowledge=parse_knowledge_base(knowledge_base)
    summarized_search_results = "Nothing found on Google."
    # searches url on google and get report back
    if search_on_google:
        search_results = google_search(url)
        # get domain from url
        domain = url.split('/')[2:]
        summarized_search_results = summarize_google_search_results(domain, search_results)

    # get the visible text for the website
    visible_text = get_visible_text(url)

    instructions = generate_instructions_v2(sender_info, recipient_info, prompt, word_count, template)

    # # generate the email using OpenAI's GPT-3
    # response = openai.Completion.create(model="text-davinci-003", prompt=visible_text + "\n" + instructions, temperature=0.7, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
    # output = response["choices"][0]["text"]

    # get current date and time in human readable format, with month in words, and day of the week, and hours in 12-hour, as a string
    current_date_time = datetime.datetime.now().strftime("%B %d, %Y %I:%M %p")

    # generate the email using OpenAI's ChatGPT API
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a highly exprienced outbound sales lead generation expert who writes cold emails that appears to be hyper-personalized based on the recipient's context. Your emails appear to be from thorough research and personal. You are good at writing high conversion emails that make people want to book meetings. You don't write emails that appear to be mass generated or spam."},
            {"role": "system", "content": "You can only use information provided to you by the user. You cannot make up numbers which you do not know is true. "},
            {"role": "system", "content": "You will write email within the word limit. You will not write more than required words."},
            {"role": "system", "content": f"Currently it is {current_date_time}."},
            {"role": "system", "content": f"Here is important factual information: {visible_text}"},
            {"role": "system", "content": f"Here is knowledge base information you can use as facts: {knowledge}"},
            {"role": "system", "content": f"Recent news you can use as factual information: {summarized_search_results}\n"},
            {"role": "user", "content": "If a template is provided to you, you will only replace content within the template which is inside a placeholder bracket, usually in [] or {}. You will not change the template structure or add new content outside of placeholders. You will not say things differently than the template's exact words."},
            {"role": "user", "content": "If the prompt goes against the template, strictly follow the template."},
            {"role": "user", "content": "You will only use the factual information in your writing."},
            {"role": "user", "content": "You cannot output things other than the email content. Do not output word count. End with the email."},
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

@demo_service_bp.route('/search_on_google', methods=['POST'])
def search_on_google():
    # get the request data
    data = request.json
    query = data['query']
    # get the search results
    search_results = google_search(query)

    return summarize_google_search_results(query, search_results)


@demo_service_bp.route('/google', methods=['POST'])
def google():
    # get the request data
    data = request.json
    query = data['query']
    # get the search results
    search_results = google_search(query)

    return search_results
    

# summarize google search results
def summarize_google_search_results(query, search_results):
    search_results_string = json.dumps(search_results)
    # generate the summary using OpenAI's ChatGPT API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize a list of things you learned about {query} in specific details, and when each event happened from this list. Sorted most recent on top."},
            # {"role": "user", "content": f"Output a summary of everything you learned about them from this list, only including most recent information that's newsworthy and positive."},
            {"role": "user", "content": f"There are often many things with the same name. Pick only the most relevant one and ignore information potentially about unrelated entities or persons than what we want to learn about. Only list newsworthy and positive things."},
            {"role": "user", "content": f"Here is the list: {search_results_string}"},
        ]
    )
    output = completion["choices"][0]["message"]["content"]
    return output
    

# knowledgebase parsing
def parse_knowledge_base(knowledge_base):
    parsed_knowledge_base = ""
    for item in knowledge_base:
        parsed_knowledge_base += f"{item['title']}: {item['description']}.\n"
    return parsed_knowledge_base

# here's another version, simplified
def generate_instructions_v2(sender_info, recipient_info, prompt, word_count, template):
    template_instructions="\n"
    if template:
        template_instructions = f"Use this template: {template}.\n\n"
    prompt_instructions="\n"
    if prompt: 
        prompt_instructions = f"Prompt: {prompt}.\n\n"
    instructions = f"You are {sender_info}. Write an email to {recipient_info}. Follow the template, and when appropriate inside placeholders only: {prompt_instructions}. Make it under {word_count} words long. {template_instructions}"
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