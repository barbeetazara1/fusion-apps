# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging


import odoo
import odoo.modules.registry
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.service import security
from odoo.tools import ustr
from odoo.tools.translate import _
from .utils import ensure_db, _get_login_redirect_url, is_user_internal
from werkzeug.utils import redirect as u_redirect


_logger = logging.getLogger(__name__)


# Shared parameters for all login/signup flows
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'signup_email'}
LOGIN_SUCCESSFUL_PARAMS = set()


class Home(http.Controller):

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        if request.db and request.session.uid and not is_user_internal(request.session.uid):
            return request.redirect_query('/web/login_successful', query=request.params)
        return request.redirect_query('/web', query=request.params)

    # ideally, this route should be `auth="user"` but that don't work in non-monodb mode.
    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):

        # Ensure we have both a database and a user
        ensure_db()                
        # Ambil session ID dari cookie Django
        django_sessionid = request.httprequest.cookies.get('session_id')
        _logger.info(f'SESSION START {django_sessionid}')
            
        if django_sessionid:
            # Verifikasi session ID dengan Django
            uid = self._get_uid_from_django_session(django_sessionid)
            if uid:
                # Set session Odoo dengan uid yang didapat
                request.session.uid = uid
                _logger.info(f'Set {uid} to cookie')
                request.update_env(user=request.session.uid)                    
                context = request.env['ir.http'].webclient_rendering_context()
                response = request.render('web.webclient_bootstrap', qcontext=context)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
            else:
                _logger.error(f'Fail redirect to landing')
                # Session tidak valid, arahkan ke login Odoo
                return u_redirect('https://internal-fusion-erp.site/')
        else:
            # Tidak ada sessionid, arahkan ke login Odoo
            _logger.error(f'Oops no cookie set')
            return u_redirect('https://systema.id/')
            

    @http.route('/web/webclient/load_menus/<string:unique>', type='http', auth='user', methods=['GET'])
    def web_load_menus(self, unique, lang=None):
        """
        Loads the menus for the webclient
        :param unique: this parameters is not used, but mandatory: it is used by the HTTP stack to make a unique request
        :param lang: language in which the menus should be loaded (only works if language is installed)
        :return: the menus (including the images in Base64)
        """
        if lang:
            request.update_context(lang=lang)

        menus = request.env["ir.ui.menu"].load_web_menus(request.session.debug)
        body = json.dumps(menus, default=ustr)
        response = request.make_response(body, [
            # this method must specify a content-type application/json instead of using the default text/html set because
            # the type of the route is set to HTTP, but the rpc is made with a get and expects JSON
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'public, max-age=' + str(http.STATIC_CACHE_LONG)),
        ])
        return response

    def _login_redirect(self, uid, redirect=None):
        return _get_login_redirect_url(uid, redirect)

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        return u_redirect('https://internal-fusion-erp.site/login/')  

    @http.route('/web/login_successful', type='http', auth='user', website=True, sitemap=False)
    def login_successful_external_user(self, **kwargs):
        """Landing page after successful login for external users (unused when portal is installed)."""
        valid_values = {k: v for k, v in kwargs.items() if k in LOGIN_SUCCESSFUL_PARAMS}
        return request.render('web.login_successful', valid_values)

    @http.route('/web/become', type='http', auth='user', sitemap=False)
    def switch_to_admin(self):
        uid = request.env.user.id
        if request.env.user._is_system():
            uid = request.session.uid = odoo.SUPERUSER_ID
            # invalidate session token cache as we've changed the uid
            request.env.registry.clear_cache()
            request.session.session_token = security.compute_session_token(request.session, request.env)

        return request.redirect(self._login_redirect(uid))

    @http.route('/web/health', type='http', auth='none', save_session=False)
    def health(self):
        data = json.dumps({
            'status': 'pass',
        })
        headers = [('Content-Type', 'application/json'),
                   ('Cache-Control', 'no-store')]
        return request.make_response(data, headers)

    @http.route(['/robots.txt'], type='http', auth="none")
    def robots(self, **kwargs):
        return "User-agent: *\nDisallow: /\n"
    
    def _get_uid_from_django_session(self, sessionid):
        """
        Verifikasi sessionid dengan Django dan dapatkan user ID (uid) Odoo.
        """
        
        # Verifikasi session_id
        _logger.info(f'Mencoba cari sesi tabel sesi {sessionid}')
        user = request.env['res.users'].sudo().browse(request.session.uid)

        if user and user.id:
            # If a valid session is found, fetch the associated user
            _logger.info(f'Dapat uid {user.id}')
            return user.id
        _logger.error(f'UID Tidak ada')
        return None

    def _decode_django_session(self, session_data):
        """
        Dekode session_data dari format Django.
        """
        # Metode ini tergantung pada bagaimana Django menyimpan session
        # Jika menggunakan signed_cookies atau database sessions dengan serializer JSON
        # Contoh untuk database sessions dengan serializer JSON:

        import base64
        import json

        try:
            decoded_data = base64.b64decode(session_data)
            session_dict = json.loads(decoded_data)
            return session_dict
        except Exception as e:
            # Tangani exception
            pass
        return {}
