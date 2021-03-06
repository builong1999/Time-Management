from odoo import models, api, fields, _


class AgileSprint(models.Model):
    _inherit = "agile.sprint"

    id_on_jira = fields.Integer(string="ID on JIRA")
    updated = fields.Boolean(string="Updated?")