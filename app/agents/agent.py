from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_gigachat.chat_models import GigaChat


text = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"


llm_model = GigaChat(
    base_url="https://ngw.devices.sberbank.ru:9443/api/v2",
    access_token="18880c81-bbb1-449e-a277-40edecf6ea38",
    model='GigaChat-2-Max',
    verbose=False,
    temperature=0.1
)

system_prompt = "Ты банковский помошник"
agent = create_react_agent(
    model=llm_model,
    tools=[],

    prompt=system_prompt,  # Подключаем системный контекст
    checkpointer=MemorySaver()  # Добавляем объект из библиотеки LangGraph для сохранения памяти агента
)

query = 'Какова основная цель документа? Опишите ключевые выводы.'
config = {"configurable": {"thread_id": "main"}}

response = agent.invoke({"messages": [("user", query.encode('utf-8', errors='replace').decode('utf-8'))]},
                        config=config)
print("🤖 :", response["messages"][-1].content)
