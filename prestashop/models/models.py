import requests
from bs4 import BeautifulSoup
from requests import RequestException

from odoo import models, fields, api


class prestashop(models.Model):
    _name = 'prestashop.prestashop'
    _description = 'prestashop.prestashop'

    name = fields.Char(string='Nom')
    price = fields.Integer(string='Prix')
    description = fields.Text(string='Description')
    reference = fields.Char(string='Reference')
    odoo_product_id = fields.Many2one('product.product', string='Produit Odoo')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100


    def import_products_from_prestashop(self):
        # Méthode pour récupérer et importer les produits depuis Prestashop
        prestashop_url = 'https://mlka-market.com/api/products/?display=[id,price,name,description_short,reference]'
        params = {
            'ws_key': 'CJ4HF5A7PHNNUHI243YCZR71V1VCM5UF',
            'output_format': 'JSON'
        }
        try:
            response = requests.get(f"{prestashop_url}", params=params)
            response.raise_for_status()  # Vérifie si la requête a réussi
            imported_count=0
            updated_count=0

            if response.status_code == 200:
                products_data = response.json()["products"]
                #print("produits", products_data)
                for product_data in products_data:
                    product_reference = product_data.get('reference')
                    if not product_reference:
                        continue
                    #print("Name",product_data.get('name'))
                    product_name = product_data.get('name')
                    product_price = float(product_data.get('price'))
                    product_description_html = product_data.get('description_short')
                    soup = BeautifulSoup(product_description_html, 'html.parser')
                    product_description = soup.get_text()
                    #product_reference = product_data.get('reference')
                    # Vérifie si le produit existe déjà dans Odoo
                    existing_product = self.search([('reference', '=', product_data['reference'])], limit=1)
                    if existing_product:
                        # Met à jour le produit existant
                        existing_product.write({
                            'name': product_name,
                            'description':  product_description,
                            'price': product_price,
                            #'reference':product_reference
                            # Mise à jour d'autres champs si nécessaire
                        })
                        updated_count +=1
                    else:
                        # Crée un nouveau produit dans Odoo
                        new_product = self.create({
                            'name': product_name,
                            'description':  product_description,
                            'price': product_price,
                            'reference':product_reference
                            # Autres champs nécessaires
                        })
                        imported_count +=1

                        product_model = self.env['product.product']
                        try:
                            odoo_product = product_model.create({
                                'name': product_name,
                                'description': product_description,
                                'list_price': product_price,
                                'default_code':product_reference
                                # Autres champs si nécessaire
                            })
                            # Associez le produit d'Odoo au produit importé de Prestashop
                            new_product.odoo_product_id = odoo_product.id
                        except RequestException as e:
                            print("Error creating product in Odoo:", e)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Importation réussie',
                        'message': f"{imported_count} produits importés, {updated_count} produits mis à jour.",
                        'sticky': False,
                    }
                }
            else:
                # Gère les erreurs de statut de la réponse de l'API Prestashop
                response.raise_for_status()
        except RequestException as e:
            # Gère les erreurs de requête à l'API Prestashop
            print("Error fetching data from Prestashop API:", e)
            #self.env.user.notify_warning(f"Error fetching data from Prestashop API: {e}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur',
                    'message': f"Erreur lors de la récupération des données de l'API Prestashop : {e}",
                    'sticky': False,
                }
            }



