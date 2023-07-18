from .throttling import ThrottlingMiddleware
from .cq_bug_fix import CQBugFix
from loader import dp


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CQBugFix())