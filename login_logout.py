#Enable the REST API:
import requests
from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

#Configure API access rights = security

class LoginLogout(models.Model):
    _name = 'login.logout'

    user_id = fields.Many2one(comodel_name='res.users', string='User', required=True, ondelete='restrict')
    authenticated = fields.Boolean(default=True)
    name = fields.Char(string='Request Code', readonly=True)
    request_date = fields.Datetime(string='Request Date', required=True)
    request_method = fields.Char(string='Method', readonly=True)
    request_body = fields.Text(string='Request Body', help="Optional, not yet used", readonly=True)
    url_login = fields.Char(string='Login', readonly=True, compute='_compute_url_login')
    url_logout = fields.Char(string='Logout', readonly=True, compute='_compute_url_logout')
    url_base = fields.Char(string='URL Base', default='http://localhost:8070/')
    url_path_login = fields.Char(string='URL Login', readonly=True, default='web/session/authenticate')
    url_path_logout = fields.Char(string='URL Logout', readonly=True, default='web/session/destroy')
    sequence = fields.Char(string='Code', default='New', readonly='True')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    
    def done(self):
        if self.state == 'draft':
            if self.sequence == 'New':
                seq = self.env['ir.sequence'].next_by_code('login.logout') or '/'
                self.sequence = seq
            self.state = 'done'

    @api.depends('url_base', 'url_path_login')
    def _compute_url_login(self):
        self.url_login = self.url_base + self.url_path_login
            
    @api.depends('url_base', 'url_path_logout')
    def _compute_url_logout(self):
        self.url_logout = self.url_base + self.url_path_logout

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            (
                "Request Code must be unique!"
            ),
        )
    ]

    def cron_auto_delete_log_error(self):
        today = datetime.now()
        last_check = today - timedelta(days=20)
        records = self.env['request.log'].sudo().search([
            ('request_date', '<', last_check)
        ], limit=10000)
        if records.exists():
            _logger.info('--> Cron delete request log')
            _logger.info(len(records))
            records.sudo().unlink()
    
    @api.model
    def login(self):
    #Obtain an authentication token #replace url with actual url & port of instance
        data = {
            'jsonrpc': '2.0',
            'params': {
                'login': self.user_id.login,
                #'password': self.user_id.password,
            },
        }
        #Make API requests: .post .get -  PUT, PATCH, and DELETE
        response = requests.post(self.url_login, json=data)
        result = response.json().get('result')

        if result and result.get('session_id'):  # Successful login
            self.env.user.session_token = result['session_id']
            self.authenticated = True
        else:  # Failed login
            raise ValueError('Invalid username or password.')
        #session_id = authentication token store for subsequent requests
    
        self.env['request.log'].create({ # Create a request log entry
            'name': self.user_id.login,
            'request_date': self.request_date,
            'url': self.url_login,
        })

    @api.model
    def logout(self):
        headers = {
            'Authorization': f'Bearer {self.env.user.session_token}',
        }
        response = requests.post(self.url_logout, headers=headers)

        if response.status_code == 204:  # Successful logout
            self.env.user.session_token = False
            self.authenticated = False
        else:  # Failed logout
            raise ValueError('Logout failed.')
            
        self.request_log_id.write({ # Update the request log entry
            'request_date': self.request_date,
        })

    @api.model
    def create(self, vals):
        record = super(LoginLogout, self).create(vals)
        record.login()  # Perform login when creating a new record
        return record

    def unlink(self):
        self.logout()  # Perform logout when deleting a record
        return super(LoginLogout, self).unlink()
