from app.agents.context import Context
from app.agents import planner, validator, executor
from app.utils import name_extract

class DummyLLM:
    def chat_completion(self, msgs, model="gpt-4o-mini"):
        u=msgs[-1]["content"].lower()
        if "ciao" in u: return '{"intent":"GREET","reason":""}'
        if "permesso" in u: return '{"intent":"ASK_SERVICE","reason":""}'
        return '{"intent":"UNKNOWN","reason":""}'
llm=DummyLLM()

def handle(msg,ctx):
    intent,_=planner.plan(ctx,msg,llm)
    intent=validator.validate(ctx,intent)
    return executor.dispatch(intent,ctx,msg)

def test_name_asking():
    ctx=Context(phone="1")
    r1=handle("Ciao",ctx)
    assert "Piacere! Come ti chiami?" in r1 and ctx.state=="ASK_NAME"
    # user gives name
    r2=handle("Mi chiamo Luca",ctx)
    assert ctx.name=="Luca" and ctx.state=="ASK_SERVICE"
    # another message, should NOT ask name again
    r3=handle("permesso di soggiorno",ctx)
    assert "60" in r3 and ctx.state=="PROPOSE_CONSULT" 