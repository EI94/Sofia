from ..policy.language_support import T

def run(ctx, text):
    ctx.state = "ASK_NAME"
    return T("greet_intro", ctx.lang) 