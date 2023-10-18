import pyperclip
from colorama import Fore
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessage,
    AIMessage,
    HumanMessage,
)

# What will be the flow?
"""

Vector search models require similarity between your query and the retrieved data.
This is not always the case, you can chunk text and omit relevant results in a table if you chunk incorrectly. Instead of dealing with the chunking problem, we can use a large context model and do question and answer directly on a paper.

Ideally, we programmatically can ask the same question of many papers and then store the results.

# Data Extraction
e.g. This paper reports on the antibacterial performance of various polymer formulations or variations. Please extract all polymer formulations:

for those formulations you've extracted, extract ALL information.  Return a json with an entry for each polymer formulation with values that are another json that contains all of the properties found in the paper.

# Data storage?

store the json with the name == paper title .json

"""
from typing import List, Union, Optional

from paperscrape.utils import get_formatted_text, grab_user_input, llm_call


class ChatAssistant:
    def __init__(
            self,
            orienting_message: str,
            LLM=ChatOpenAI(model_name='gpt-3.5-turbo', max_tokens=2000),
            custom_context: Optional[str] = None
    ):

        self.LLM = LLM
        self.system_message_prompt = SystemMessage(content=orienting_message)
        self.conversation: List[Union[AIMessage, SystemMessage, HumanMessage]] = [self.system_message_prompt]

        if custom_context is not None:
            self.conversation.append(SystemMessage(content=custom_context))


    @staticmethod
    def execute_human_tasks(human_input: str, conversation: List[Union[AIMessage, SystemMessage, HumanMessage]]):
        if human_input.lower() in ['copy', 'copy to clipboard']:
            text_to_copy = conversation[-1].content
            pyperclip.copy(text_to_copy)
            print(f'{Fore.RED}\n\tCopied to clipboard!')
            print(f'Text Copied: {text_to_copy[:20]} ... {text_to_copy[-20:]}')
            return True
        else:
            return False

    def chat(self, initial_question=None):
        if initial_question is not None:
            human_input = initial_question
        else:
            human_input = ''

        while human_input != 'quit':
            if not human_input:
                human_input = grab_user_input()

            executed: bool = self.execute_human_tasks(human_input, self.conversation)
            if executed:
                continue

            if human_input.lower() == 'quit':
                print('EXITING')
                break

            human_message_prompt = HumanMessage(content=human_input)
            human_input = ''

            self.conversation.append(human_message_prompt)

            output = llm_call(self.LLM, self.conversation).content
            
            print('  ', get_formatted_text(output).replace('\n', '\n  '))
            if output.lower().strip() == 'Have a nice day!!!'.lower():
                print('EXITING')
                break
            ai_message_prompt = AIMessage(content=output)
            self.conversation.append(ai_message_prompt)


def grab_paper_context(fp):
    from paperscrape.pdf_reader import parse_pdf

    pages = parse_pdf(fp)

    return pages


if __name__ == '__main__':
    system_message = """I'm a helpful assistant that helps you perform literature reviews. I will return only information based on the paper that you provide.
    I will follow your instructions for extracting the information that you need from this scientific article. 
    
    """

    file = '/Users/hectorlopezhernandez/Downloads/s41524-023-01016-5.pdf'
    pages = grab_paper_context(fp=file)
    scientific_article = '\n'.join(pages[:1])
    custom_context = f"The scientific article is: {scientific_article}"

    model: str = 'gpt-3.5-turbo'

    from langchain.chat_models import ChatAnthropic

    if model in ['claude-2.0']:
        LLM = ChatAnthropic(model="claude-2.0", max_tokens=90000)
    elif model in ['gpt-3.5-turbo']:
        LLM = ChatOpenAI(model_name=model, max_tokens=2000)
    else:
        raise ValueError('Incorrect Model Selected')

    chat_assistant = ChatAssistant(
        orienting_message=system_message,
        LLM=LLM,
        custom_context=custom_context
    )

    question = """
    This paper reports on the antibacterial performance of various polymer formulations or variations. Please extract all polymer formulations. For those formulations you've extracted, extract ALL information.  Return a json with an entry for each polymer formulation with values that are another json that contains all of the properties found in the paper.
    """
    chat_assistant.chat(initial_question='What is this about?')
