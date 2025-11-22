from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import find_all_orders, create_customer_service, update_customer_service, find_all_customers
from django.db import DatabaseError


class SearchOrdersView(APIView):
    def get(self, request):

        # parámetros
        customer_name = request.query_params.get("customer_name")
        employee_name = request.query_params.get("employee_name")

        # Convertimos a int
        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 10))

        # obtenemos datos desde service
        rows = find_all_orders(
            customer_name,
            employee_name,
            page,
            size
        )

        if not rows:
            return Response({
                "content": [],
                "page": page,
                "pageSize": size,
                "totalElements": 0,
                "totalPages": 0,
                "numberOfElements": 0
            })

        # total_count viene repetido en cada fila → tomamos la primera
        total_elements = rows[0]["total_count"]

        total_pages = (total_elements + size -
                       1) // size  # redondeo

        content = []
        for row in rows:
            r = row.copy()
            del r["total_count"]  # lo sacamos del contenido
            content.append(r)

        response = {
            "content": content,
            "page": page,
            "pageSize": size,
            "totalElements": total_elements,
            "totalPages": total_pages,
            "numberOfElements": len(content)
        }

        return Response(response, status=status.HTTP_200_OK)


class SearchCustomersView(APIView):
    def get(self, request):

        # obtener filtros
        company_name = request.query_params.get("company_name")
        contact_name = request.query_params.get("contact_name")

        # paginación
        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 10))

        rows = find_all_customers(
            company_name,
            contact_name,
            page,
            size
        )

        # Sin resultados
        if not rows:
            return Response({
                "content": [],
                "page": page,
                "pageSize": size,
                "totalElements": 0,
                "totalPages": 0,
                "numberOfElements": 0
            })

        # total_count viene repetido en cada fila
        total_elements = rows[0]["total_count"]
        total_pages = (total_elements + size - 1) // size

        # limpiar cada fila (remover total_count)
        content = []
        for row in rows:
            item = row.copy()
            del item["total_count"]
            content.append(item)

        response = {
            "content": content,
            "page": page,
            "pageSize": size,
            "totalElements": total_elements,
            "totalPages": total_pages,
            "numberOfElements": len(content)
        }

        return Response(response, status=status.HTTP_200_OK)


class CreateCustomerView(APIView):
    def post(self, request):
        data = request.data

        try:
            customer = create_customer_service(
                data.get("customerid"),
                data.get("companyname"),
                data.get("contactname"),
                data.get("contacttitle"),
                data.get("address"),
                data.get("city"),
                data.get("region"),
                data.get("postalcode"),
                data.get("country"),
                data.get("phone"),
                data.get("fax"),
            )

            return Response(customer, status=status.HTTP_201_CREATED)

        except DatabaseError as e:
            return Response({"error": str(e)}, status=400)


class UpdateCustomerView(APIView):
    def put(self, request, customerid):
        data = request.data

        try:
            updated = update_customer_service(
                customerid,
                data.get("companyname"),
                data.get("contactname"),
                data.get("contacttitle"),
                data.get("address"),
                data.get("city"),
                data.get("region"),
                data.get("postalcode"),
                data.get("country"),
                data.get("phone"),
                data.get("fax"),
            )

            return Response(updated, status=status.HTTP_200_OK)

        except DatabaseError as e:
            return Response({"error": str(e)}, status=400)
