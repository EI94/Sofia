from ..policy.language_support import T

def run(ctx, user_msg):
    return T("ask_channel", ctx.lang) 