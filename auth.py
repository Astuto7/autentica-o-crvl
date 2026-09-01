from flask import Blueprint, render_template, abort
from models import AuthRecord

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/v/<token>')
def view_record(token):
    registro = AuthRecord.query.filter_by(token=token).first()
    if not registro:
        abort(404)
    return render_template('auth/view.html', registro=registro)
