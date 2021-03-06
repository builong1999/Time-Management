from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.project_management.utils.time_parsing import convert_second_to_log_format, convert_log_format_to_second, get_date_range
from Crypto.Cipher import AES
import base64
import json


class JiraTimeLog(models.Model):
    _name = "jira.time.log"
    _description = "JIRA Time Log"
    _order = 'start_date desc'
    _rec_name = 'ticket_id'

    time = fields.Char(string='Time Logging', compute='_compute_time_data', store=True)
    description = fields.Text(string='Description', required=True)
    ticket_id = fields.Many2one('jira.ticket', string='Ticket', ondelete="cascade")
    duration = fields.Integer(string='Duration', required=True)
    cluster_id = fields.Many2one('jira.work.log.cluster')
    state = fields.Selection([('progress', 'In Progress'), ('done', 'Done')], string='Status', default='progress')
    source = fields.Char(string='Source')
    user_id = fields.Many2one('res.users', string='User')
    start_date = fields.Datetime("Start Date")
    encode_string = fields.Char(string="Hash String", compute='_compute_encode_string')
    project_id = fields.Many2one(string='Project', related="ticket_id.project_id", store=True)
    duration_hrs = fields.Float(string="Duration(hrs)", compute="_compute_duration_hrs", store=True)
    filter_date = fields.Char(string="Filter", store=False, search='_search_filter_date')

    def _search_filter_date(self, operator, operand):
        if operator == "=":
            start_date, end_date = get_date_range(self, operand)
            ids = self.search([('start_date', '>=', start_date), ('start_date', '<', end_date)])
            return [('id', 'in', ids.ids)]
        raise UserError(_("Search operation not supported"))

    @api.depends("duration")
    def _compute_duration_hrs(self):
        for record in self:
            record.duration_hrs = record.duration/3600

    @api.depends('duration')
    def _compute_time_data(self):
        for record in self:
            if record.duration:
                record.time = convert_second_to_log_format(record.duration)

    def unlink(self):
        cluster_ids = self.mapped('cluster_id')
        work_log_ids = self.mapped('ticket_id').mapped('work_log_ids').filtered(lambda r: r.cluster_id in cluster_ids)
        work_log_ids.write({'state': 'cancel'})
        work_log_ids.filtered(lambda r: not r.end).write({'end': datetime.now()})
        return super().unlink()

    @api.model
    def create(self, values):
        if 'time' in values:
            values['duration'] = convert_log_format_to_second(values['time'])
            values.pop('time')
        if 'start_date' not in values:
            values['start_date'] = datetime.now()
        return super().create(values)

    def _compute_encode_string(self):
        cipher = AES.new(b'Bui Phi Long LML', AES.MODE_EAX)
        nonce = base64.decodebytes(cipher.nonce)
        one_time_link_env = self.env['one.time.link'].sudo()
        for record in self:
            ciphertext, tag = cipher.encrypt_and_digest(json.dumps({
                "record_id": record.id,
                "uid": record.user_id.id
            }))
            record.encode_string = base64.decodebytes(ciphertext)
            one_time_link_env.create({
                'key': record.encode_string,
                'value': nonce
            })
