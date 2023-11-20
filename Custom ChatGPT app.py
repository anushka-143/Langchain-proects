#step 1 : importing
from secretkeys import pinecone_key,pinecone_env, openai_api_key
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory

#step 2: memory object

llm = ChatOpenAI(model_name = 'gpt-3.5-turbo', temperature = 1)
history = FileChatMessageHistory('chat_history.json')
memory = ConversationBufferMemory(
    memory_key = 'chat_history',
    chat_memory = history,
    return_messages =True
)

#step 3: prompt
prompt = ChatPromptTemplate(
    input_variables = ["content"],
    messages = [
        SystemMessage(content = 'You are a chatbot having conversation with human'),
        MessagesPlaceholder(variable_name='chat_history'), # where the memory will be stored
        HumanMessagePromptTemplate.from_template('{content}')
    ]
)

#step 4: creating chain and adding memory to it

chain = LLMChain(llm=llm, prompt = prompt,memory = memory, verbose =False)
while True:
    content = input("Please enter your prompt:\n")
    if content in ['quit','exit','bye']:
        print('Goodbye!')
        break

    response = chain.run({'content':content})
    print(response)
    print('-'*50)

