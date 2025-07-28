from ..policy.language_support import T

def run(ctx, user_msg):
    return T("ask_payment", ctx.lang) 