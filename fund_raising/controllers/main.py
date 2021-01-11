from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
import werkzeug
import json
import time

# List of content types that will be opened in browser
OPEN_BROWSER_TYPES = ['application/pdf']


######################
# Report Controllers #
######################
class PrtReportController(http.Controller):
    @http.route([
        '/page/test',
    ], type='http', auth='user', website=True)
    def report_routes(self, **data):
        print(data)