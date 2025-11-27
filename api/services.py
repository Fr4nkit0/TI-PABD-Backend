from django.db import connection


def find_all_orders(customer_name, employee_name, page, page_size):
    """
    Service que llama a la función search_orders() de PostgreSQL.
    """

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM search_orders(%s, %s, %s, %s);
        """, [
            customer_name,
            employee_name,
            page,
            page_size
        ])

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    results = [dict(zip(columns, row)) for row in rows]

    return results


def find_all_customers(company_name, contact_name, page, page_size):
    """
    Llama a la función search_customers() de PostgreSQL.
    """

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM search_customers(%s, %s, %s, %s);
        """, [
            company_name,
            contact_name,
            page,
            page_size
        ])

        # nombres de columnas
        columns = [col[0] for col in cursor.description]

        # filas reales
        rows = cursor.fetchall()

    # Convertimos filas a diccionario
    results = [dict(zip(columns, row)) for row in rows]

    return results


def create_customer_service(
    customerid,
    companyname,
    contactname,
    contacttitle,
    address,
    city,
    region=None,
    postalcode=None,
    country=None,
    phone=None,
    fax=None
):
    """
    Llama a la función create_customer() en PostgreSQL.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM create_customer(
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s
            );
        """, [
            customerid,
            companyname,
            contactname,
            contacttitle,
            address,
            city,
            region,
            postalcode,
            country,
            phone,
            fax
        ])

        columns = [c[0] for c in cursor.description]
        row = cursor.fetchone()

    return dict(zip(columns, row))


def update_customer_service(
    customerid,
    companyname=None,
    contactname=None,
    contacttitle=None,
    address=None,
    city=None,
    region=None,
    postalcode=None,
    country=None,
    phone=None,
    fax=None
):
    """
    Llama a la función update_customer() en PostgreSQL.
    """

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM update_customer(
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s
            );
        """, [
            customerid,
            companyname,
            contactname,
            contacttitle,
            address,
            city,
            region,
            postalcode,
            country,
            phone,
            fax
        ])

        columns = [c[0] for c in cursor.description]
        row = cursor.fetchone()

    return dict(zip(columns, row))


def delete_customer_service(customerid):
    """
    Llama a la función delete_customer() en PostgreSQL.
    """

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM delete_customer(%s);
        """, [customerid])

        columns = [c[0] for c in cursor.description]
        row = cursor.fetchone()

    return dict(zip(columns, row))
