# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class DraftOrder(models.Model):

	_inherit = 'stock.move'

	def draft_order(self):
		stock_move = self.env['stock.move'].browse(self._context.get('active_ids'))
		for order in stock_move:
			order.write({'state':'draft'})

	def delete_order(self):
		stock_move = self.env['stock.move'].browse(self._context.get('active_ids'))
		for order in stock_move:
			order.write({'state':'cancel'})
			for move in order.move_line_ids:
				move.write({'state':'draft'}) 
			order.unlink()

	def cancel_order(self):
		stock_move = self.env['stock.move'].browse(self._context.get('active_ids'))
		for order in stock_move:
			order.write({'state':'cancel'})