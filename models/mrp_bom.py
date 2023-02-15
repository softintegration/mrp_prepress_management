# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof',readonly=True)
    cutting_die_id = fields.Many2one('prepress.cutting.die', string="Cutting Die")
    exposure_nbr = fields.Integer('Exposure Nbr', related='cutting_die_id.exposure_nbr', readonly=False,store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(MrpBom, self)._onchange_product_id()
        self._update_prepress_proof()
        return res

    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        res = super(MrpBom, self).onchange_product_tmpl_id()
        self._update_prepress_proof(product_tmpl=self.product_tmpl_id)
        return res

    def _update_prepress_proof(self,product_tmpl=False):
        if not self.product_id and not product_tmpl:
            return
        if not product_tmpl:
            prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        else:
            prepress_proof = self.env['prepress.proof']._get_by_product_tmpl_id(product_tmpl.id)
        self.update({'prepress_proof_id': prepress_proof and prepress_proof.ids[0] or False})

    @api.model
    def create(self,vals):
        mrp_boms = super(MrpBom, self).create(vals)
        for bom in mrp_boms:
            if not bom.prepress_proof_id:
                if bom.product_id:
                    prepress_proof = self.env['prepress.proof']._get_by_product(bom.product_id)
                elif bom.product_tmpl_id:
                    prepress_proof = self.env['prepress.proof']._get_by_product_tmpl_id(bom.product_tmpl_id.id)
                bom.prepress_proof_id = prepress_proof and prepress_proof.ids[0] or False
        return mrp_boms


    @api.constrains('exposure_nbr','cutting_die_id')
    def _check_exposure_nbr(self):
        for each in self.filtered(lambda e:e.cutting_die_id and e.exposure_nbr):
            if each.exposure_nbr > each.cutting_die_id.exposure_nbr:
                raise ValidationError(_("Exposure Nbr must be less than or equal to Cutting die Exposure Nbr"))



class MrpByProduct(models.Model):
    _inherit = 'mrp.bom.byproduct'

    prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(MrpByProduct,self)._onchange_product_id()
        self._update_prepress_proof()
        return res

    def _update_prepress_proof(self):
        if not self.product_id:
            return
        prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        self.update({'prepress_proof_id': prepress_proof and prepress_proof.ids[0] or False})




