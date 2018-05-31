class DeepReplyError(ValueError):
    # 如果一个评论的父评论为一个子评论，弹出这个错误
    pass


class IsolateReplyError(ValueError):
    # 如果一个评论指向另一个评论，却没有相应的父评论，弹出这个错误
    pass


class PointError(ValueError):
    # 如果一个评论回复的评论或它的父评论与这个评论不属于同一个讨论，弹出这个错误
    pass
