from . import bp

@bp.route('/')
def site():
    return "This is a new spot from the blueprint!"
