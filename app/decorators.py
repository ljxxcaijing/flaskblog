from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .models import Permission
from decorators import admin_required, permission_required
from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*arg, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return decorated_function
        return decorator

    def admin_required(f):
        return permission_required(Permission,ADMINISTER)(f)

@main.route('/admin')
@login_required
@admin_required
def for _admins_ only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"
