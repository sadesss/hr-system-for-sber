from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_gigachat.chat_models import GigaChat
from gigachat.models import AccessToken, ChatCompletion

from app.agents.GigaCredentials import GigaCredentials

def get_reqest(query, system_prompt):
    base_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"


    giga_credentials: GigaCredentials = GigaCredentials()
    giga: GigaChat = GigaChat(credentials=giga_credentials.get_base_encoded(),
                              verify_ssl_certs=False)
    token: AccessToken = giga.get_token()


    llm_model = GigaChat(
        base_url=base_url,
        access_token=token,
        model='GigaChat-2-lite',
        verbose=False,
        temperature=0.1,
        max_tokens=100,
    )
    agent = create_react_agent(
        model=llm_model,
        tools=[],

        prompt=system_prompt,  # Подключаем системный контекст
        checkpointer=MemorySaver()  # Добавляем объект из библиотеки LangGraph для сохранения памяти агента
    )

    config = {"configurable": {"thread_id": "main"}}

    response = agent.invoke(
        {"messages": [("user", query.encode('utf-8', errors='replace').decode('utf-8'))]},
                            config=config)
    return response["messages"][-1].content
