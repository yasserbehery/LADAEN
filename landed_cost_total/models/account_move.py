from odoo import fields, models, api


class StockValuationAdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    move_ids = fields.Many2one('stock.landed.cost')
    is_computes = fields.Boolean()


class AccountMoveInherit(models.Model):
    _inherit = 'stock.landed.cost'

    totals = fields.One2many('stock.valuation.adjustment.lines', 'move_ids', string='Landed Cost Total')
    amount_total = fields.Monetary(string="Landed Cost Total")
    # custom_total = fields.Monetary(compute="compute_total")
    custom_total = fields.Monetary(compute="compute_total_new")

    # @api.depends('amount_total', 'totals.is_computes', 'custom_total')
    # def compute_total(self):
    #     for rec in self:
    #         if rec.valuation_adjustment_lines.filtered(lambda line: line.is_computes).mapped('former_cost'):
    #             rec.custom_total = sum(rec.valuation_adjustment_lines.filtered(lambda line: line.is_computes).mapped('former_cost'))
    #         else:
    #             rec.custom_total = False

    @api.onchange('amount_total', 'totals.is_computes', 'custom_total', 'totals.final_cost')
    def compute_total_new(self):
        for rec in self:
            sum = 0
            if rec.valuation_adjustment_lines:
                for line in rec.valuation_adjustment_lines:
                    if line.final_cost and line.is_computes:
                        sum += line.final_cost
            rec.custom_total = sum + rec.amount_total
