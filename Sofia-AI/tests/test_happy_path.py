from app.agents.context import Context
from app.agents import planner, validator, executor
from app.middleware import llm
ctx=Context("123")
def fake_llm(messages,model="gpt-4o-mini"):
    # route by keywords
    user=messages[-1]["content"].lower()
    if "ciao" in user:   return '{"intent":"GREET","reason":""}'
    if "mario" in user:  return '{"intent":"ASK_SERVICE","reason":""}'
    if "permesso" in user: return '{"intent":"PROPOSE_CONSULT","reason":""}'
    return '{"intent":"CLARIFY","reason":""}'
llm.chat_completion=fake_llm
def test_flow():
    assert executor.dispatch(validator.validate(ctx,"GREET"),ctx,"ciao")      # greet
    assert executor.dispatch(validator.validate(ctx,"ASK_NAME"),ctx,"Mario") # name
    assert executor.dispatch(validator.validate(ctx,"ASK_SERVICE"),ctx,"permesso di soggiorno") 