from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductSerializer, MaterialSerializer, ProductMaterialSerializer, WarehouseSerializer

class InventoryCheckView(APIView):
    def get(self, request, format=None):
        products_data = request.query_params.get('products', None)
        if products_data:
            products_data = eval(products_data)  
        else:
            return Response({"error": "No products data provided"}, status=400)

        result = []
        for product_info in products_data:
            product_id = product_info['product_id']
            product_qty = product_info['product_qty']
            product = Product.objects.get(id=product_id)
            materials = ProductMaterial.objects.filter(product=product)

            product_result = {
                "product_name": product.name,
                "product_qty": product_qty,
                "product_materials": []
            }

            for material in materials:
                material_qty_needed = material.quantity * product_qty
                warehouses = Warehouse.objects.filter(material=material.material)
                material_result = []
                for warehouse in warehouses:
                    if material_qty_needed <= 0:
                        break
                    if warehouse.remainder >= material_qty_needed:
                        material_result.append({
                            "warehouse_id": warehouse.id,
                            "material_name": material.material.name,
                            "qty": material_qty_needed,
                            "price": warehouse.price
                        })
                        material_qty_needed = 0
                    else:
                        material_result.append({
                            "warehouse_id": warehouse.id,
                            "material_name": material.material.name,
                            "qty": warehouse.remainder,
                            "price": warehouse.price
                        })
                        material_qty_needed -= warehouse.remainder

                if material_qty_needed > 0:
                    material_result.append({
                        "warehouse_id": None,
                        "material_name": material.material.name,
                        "qty": material_qty_needed,
                        "price": None
                    })

                product_result['product_materials'].extend(material_result)

            result.append(product_result)

        return Response({"result": result})

