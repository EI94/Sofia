from ..policy.language_support import T

def run(ctx, user_msg):
    return T("route_active_app", ctx.lang) 