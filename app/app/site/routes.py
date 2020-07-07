from . import bp

@bp.route('/')
def site():
    return "This is where the site lives!"
