# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    contract_id = fields.Many2one('sale.contract', 'Contract', copy=False, check_company=True)
