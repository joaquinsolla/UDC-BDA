#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Autores:
#   - Joaquín Solla Vázquez (joaquin.solla@udc.es)
#   - Lucas Campos Camiña (lucas.campos@udc.es)

# Data de creación: 03-05-2022
#

import json
import sys
import psycopg2
import psycopg2.extras
import psycopg2.errorcodes
import psycopg2.extensions
from datetime import datetime


## AUX_FUNCS---------------------------------------------------
def read_config(file):
    """
    Lee a config da BD
    :param file: path do arquivo config
    :return: config da BD
    """
    with open(file) as f:
        cfg = json.load(f)
    return cfg


def request_keyword():
    """
    Solicita ó usuario o campo código
    :return: o código introducido ou None no seu defecto
    """
    keyword = input("[OP] Palabra clave (string): ")
    if keyword != "":
        return keyword
    else:
        return None


def request_id():
    """
    Solicita ó usuario o campo código
    :return: o código introducido ou None no seu defecto
    """
    id = input("[OB] Id (int): ")
    if id != "":
        return int(id)
    else:
        return None


def request_nombre():
    """
    Solicita ó usuario o campo nome
    :return: o nome introducido ou None no seu defecto
    """
    nome = input("[OB] Nome (string): ")
    if nome != "":
        return nome
    else:
        return None


def request_trabajo():
    """
    Solicita ó usuario o campo traballo
    :return: o traballo introducido ou None no seu defecto
    """
    traballo = input("[OB] Traballo (string): ")
    if traballo != "":
        return traballo
    else:
        return None


def request_salario():
    """
    Solicita ó usuario o campo salario
    :return: o salario introducido ou None no seu defecto
    """
    salario = input("[OB] Salario (float): ")
    if salario != "":
        return float(salario)
    else:
        return None


def request_comision():
    """
    Solicita ó usuario o campo comision
    :return: a comisión introducida ou None no seu defecto
    """
    comision = input("[OP] Comisión (float): ")
    if comision != "":
        return float(comision)
    else:
        return None


def request_id_of(text):
    """
    Solicita ó usuario o campo id (de xefe ou de departamento)
    :return: o id (de xefe ou de departamento) introducido ou None no seu defecto
    """
    id = input("[OP] Id " + text + " (int): ")
    if id != "":
        return int(id)
    else:
        return None


def request_localidade():
    """
    Solicita ó usuario o campo localidade
    :return: a localidade introducida ou None no seu defecto
    """
    localidade = input("[OB] Localidade (string): ")
    if localidade != "":
        return localidade
    else:
        return None


def request_changes_confirmation():
    """
    Solicita ó usuario confirmación para aplicar os cambios
    :return: True ou False
    """
    cambios = input("[OB] Confirmar cambios? (S/n): ")
    if cambios == "N" or cambios == "n":
        return False
    else:
        return True


def request_horas():
    """
    Solicita ó usuario o campo horas
    :return: o código introducido ou None no seu defecto
    """
    horas = input("[OB] Horas (int): ")
    if horas != "":
        return int(horas)
    else:
        return None


## ------------------------------------------------------------
def connect_db():
    """
    Establece conexión ca BD
    :return: conexión ca BD
    """
    try:
        config = read_config('dbconfig.json')
        conn = psycopg2.connect(cursor_factory=psycopg2.extras.DictCursor, **config)
        conn.autocommit = False
        print('[✓] Conectado.')
        return conn
    except psycopg2.OperationalError as e:
        print(f"[✗] Imposible conectar: {e}")
        sys.exit(-1)


## ------------------------------------------------------------
def disconnect_db(conn):
    """
    Pecha a conexión ca BD
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    conn.commit()
    conn.close()
    print('[✓] Conexión pechada.')


## ------------------------------------------------------------
def get_emp_by_id(conn):
    """
    Pide por teclado ao usuario o id dalgún empleado
    :param conn: a conexion aberta á bd
    :return: o codigo do empleado se exsite (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None

    sentenza_select = """select * from empleado where id=%(id)s"""

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentenza_select, {'id': id})
            row = cur.fetchone()

            if row is None:
                print(f"[✓] Non existe o empregado con id {id}")
                conn.commit()
                return None
            else:
                comision = row['comision']
                if comision is None:
                    comision = '-'

                id_xefe = row['id_jefe']
                if id_xefe is None:
                    id_xefe = '-'

                id_departamento = row['id_departamento']
                if id_departamento is None:
                    id_departamento = '-'

                print(f"[✓] 1 empregado atopado:")
                print(f"\tId: {row['id']}")
                print(f"\tNome: {row['nombre']}")
                print(f"\tTraballo: {row['trabajo']}")
                print(f"\tData contratación: {row['fecha_contratacion']}")
                print(f"\tSalario: {row['salario']}")
                print(f"\tComision: {comision}")
                print(f"\tId xefe: {id_xefe}")
                print(f"\tId departamento: {id_departamento}")

                conn.commit()
                return row[0]

        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()
            return None


## ------------------------------------------------------------
def get_dept_by_id(conn):
    """
    Pide por teclado ao usuario o id dalgún departamento
    :param conn: a conexion aberta á bd
    :return: o codigo do departamento se exsite (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None

    sentenza_select = """select * from departamento where id=%(id)s"""

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentenza_select, {'id': id})
            row = cur.fetchone()

            if row is None:
                print(f"[✓] Non existe o departamento con id {id}")
                conn.commit()
                return None
            else:
                print(f"[✓] 1 departamento atopado:")
                print(f"\tId: {row['id']}")
                print(f"\tNome: {row['nombre']}")
                print(f"\tLocalidade: {row['localidad']}")

                conn.commit()
                return row[0]

        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()
            return None


## ------------------------------------------------------------
def get_pro_by_id(conn):
    """
    Pide por teclado ao usuario o id dalgún proxecto
    :param conn: a conexion aberta á bd
    :return: o codigo do proxecto se exsite (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None

    sentenza_select = """select * from proyecto where id=%(id)s"""

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentenza_select, {'id': id})
            row = cur.fetchone()

            if row is None:
                print(f"[✓] Non existe o proxecto con id {id}")
                conn.commit()
                return None
            else:
                print(f"[✓] 1 proxecto atopado:")
                print(f"\tId: {row['id']}")
                print(f"\tNome: {row['nombre']}")
                print(f"\tLocalidade: {row['localidad']}")

                conn.commit()
                return row[0]

        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()
            return None


## ------------------------------------------------------------
def get_emps_by_sal(conn):
    """
    Pide por teclado ao usuario o salario dalgún empleado
    :param conn: a conexión aberta á bd
    :return: Devolve os detalles dos empleados que cumpren a restricción
    de salario indicada (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    salario = request_salario()
    if salario is None:
        print(f"[✗] É obrigatorio especificar o salario")
        return None

    sentencia_select = """
        select id, nombre, salario from empleado where salario>%(salario)s
        """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_select, {'salario': salario})
            row = cur.fetchone()
            while row:
                print(f"\tFila {cur.rownumber}: [id: {row[0]}, nome: {row[1]}, salario: {row[2]}]")
                row = cur.fetchone()
            print(f"[✓] Total de empregados: {cur.rowcount}")
            conn.commit()
        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def get_depts_by_loc(conn):
    """
    Pide por teclado ao usuario a localidade dalgún departamento
    :param conn: a conexión aberta á bd
    :return: Devolve os detalles dos departamentos que cumpren a restricción
    de localidade indicada (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    localidade = request_localidade()
    if localidade is None:
        print(f"[✗] É obrigatorio especificar a localidade")
        return None

    sentencia_select = """
        select id, nombre from departamento where localidad=%(localidade)s
        """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_select, {'localidade': localidade})
            row = cur.fetchone()
            while row:
                print(f"\tFila {cur.rownumber}: [id: {row[0]}, nome: {row[1]}]")
                row = cur.fetchone()
            print(f"[✓] Total de departamentos: {cur.rowcount}")
            conn.commit()
        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def get_pros_by_loc(conn):
    """
    Pide por teclado ao usuario a localidade dalgún proxecto
    :param conn: a conexión aberta á bd
    :return: Devolve os detalles dos departamentos que cumpren a restricción
    de localidade indicada (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    localidade = request_localidade()
    if localidade is None:
        print(f"[✗] É obrigatorio especificar a localidade")
        return None

    sentencia_select = """
        select id, nombre from proyecto where localidad=%(localidade)s
        """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_select, {'localidade': localidade})
            row = cur.fetchone()
            while row:
                print(f"\tFila {cur.rownumber}: [id: {row[0]}, nome: {row[1]}]")
                row = cur.fetchone()
            print(f"[✓] Total de departamentos: {cur.rowcount}")
            conn.commit()
        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def update_emp_sal_by_percentage(conn):
    """
    Pide por teclado ao usuario un porcentaxe para incrementar o salario
    dun empleado
    :param conn: a conexión aberta á bd
    :return: Devolve os detalles do usuario co cambio aplicado (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    id = get_emp_by_id(conn)

    if id is None:
        conn.rollback()
        return

    porcentaxeStr = input("Introduce unha porcentaxe de aumento de salario (float): ")
    porcentaxe = float(porcentaxeStr)

    sentencia_update = "update empleado set salario = salario + salario * %(porc)s / 100 where id = %(id)s"

    sentencia_select = """
            select id, nombre, salario from empleado where id=%(id)s
            """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_select, {'id': id})
            row = cur.fetchone()
            print(f"RESULTADO: [id: {row[0]}, nome: {row[1]}, novo salario: {row[2] + row[2] * porcentaxe / 100}]")
            confirmacion = request_changes_confirmation()
            if confirmacion:
                cur.execute(sentencia_update, {'id': id, 'porc': porcentaxe})
                conn.commit()
                print(f"[✓] Salario actualizado")
            else:
                conn.rollback()
                print(f"[✗] Actualización cancelada polo usuario")

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("[✗]ERRO: O salario debe ser positivo")
            else:
                print(f"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def update_emp_comm(conn):
    """
    Pide por teclado ao usuario unha nova comisión para cambiarsela
    ao usuario
    :param conn: a conexión aberta á bd
    :return: Devolve os detalles do usuario co cambio aplicado (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    id = get_emp_by_id(conn)

    if id is None:
        conn.rollback()
        return

    commStr = input("Introduce a nova comisión (float): ")
    if commStr == '':
        comm = None
    else:
        comm = float(commStr)

    sentencia_update = "update empleado set comision = %(comm)s where id = %(id)s"

    sentencia_select = """
            select id, nombre, comision from empleado where id=%(id)s
            """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_select, {'id': id})
            row = cur.fetchone()
            print(f"RESULTADO: [id: {row[0]}, nome: {row[1]}, nova comisión: {comm}]")
            confirmacion = request_changes_confirmation()
            if confirmacion:
                cur.execute(sentencia_update, {'id': id, 'comm': comm})
                conn.commit()
                print(f"[✓] Comisión actualizada")
            else:
                conn.rollback()
                print(f"[✗] Actualización cancelada polo usuario")

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("[✗]ERRO: A comisión debe ser positiva")
            else:
                print(f"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def insert_emp(conn):
    """
    Pide por teclado os datos dun empleado e inserta a fila
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None
    nome = request_nombre()
    if nome is None:
        print(f"[✗] É obrigatorio especificar o nome")
        return None
    traballo = request_trabajo()
    if traballo is None:
        print(f"[✗] É obrigatorio especificar o traballo")
        return None

    now = datetime.now()
    data_contratacion = now.strftime("%Y/%m/%d")

    salario = request_salario()
    if salario is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None
    comision = request_comision()
    id_xefe = request_id_of("do xefe")
    id_departamento = request_id_of("do departamento")

    sentenza_select_xefe = """
            select id from empleado where (id = %(id_xefe)s)
        """

    sentenza_select_departamento = """
            select id from departamento where (id = %(id_departamento)s)
        """

    sentenza_insert = """
        insert into empleado(id, nombre, trabajo, fecha_contratacion, salario, comision, id_jefe, id_departamento)
        values(%(id)s, %(nome)s, %(traballo)s, %(data_contratacion)s, %(salario)s, %(comision)s, %(id_xefe)s, %(id_departamento)s)
    """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if id_xefe is not None:
                cur.execute(sentenza_select_xefe, {'id_xefe': id_xefe})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o empregado con id " + str(id_xefe) + " para engadir coma xefe")
                    return None
            if id_departamento is not None:
                cur.execute(sentenza_select_departamento, {'id_departamento': id_departamento})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o departamento con id " + str(id_departamento))
                    return None

            cur.execute(sentenza_insert,
                        {'id': id, 'nome': nome, 'traballo': traballo, 'data_contratacion': data_contratacion,
                         'salario': salario, 'comision': comision, 'id_xefe': id_xefe,
                         'id_departamento': id_departamento})

            conn.commit()
            print(f"[✓] Empregado insertado")

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print(f"[✗] O salario e a comisión deben ser positivos")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"[✗] Xa existe un empregado co id " + str(id))
            else:
                print(F"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def insert_dept(conn):
    """
    Pide por teclado os datos dun departamento e inserta a fila
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None
    nome = request_nombre()
    if nome is None:
        print(f"[✗] É obrigatorio especificar o nome")
        return None
    localidade = request_localidade()
    if localidade is None:
        print(f"[✗] É obrigatorio especificar a localidade")
        return None

    sentenza_insert = """
        insert into departamento(id, nombre, localidad)
        values(%(id)s, %(nome)s, %(localidade)s)
    """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentenza_insert, {'id': id, 'nome': nome, 'localidade': localidade})
            conn.commit()
            print(f"[✓] Departamento insertado")

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"[✗] Xa existe un departamento co id " + str(id))
            else:
                print(F"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def insert_pro(conn):
    """
    Pide por teclado os datos dun proxecto e inserta a fila
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None
    nome = request_nombre()
    if nome is None:
        print(f"[✗] É obrigatorio especificar o nome")
        return None
    localidade = request_localidade()
    if localidade is None:
        print(f"[✗] É obrigatorio especificar a localidade")
        return None

    sentenza_insert = """
        insert into proyecto(id, nombre, localidad)
        values(%(id)s, %(nome)s, %(localidade)s)
    """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentenza_insert, {'id': id, 'nome': nome, 'localidade': localidade})
            conn.commit()
            print(f"[✓] Proxecto insertado")

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"[✗] Xa existe un proxecto co id " + str(id))
            else:
                print(F"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def delete_emp_by_id(conn):
    """
    Elimina unha fila na táboa empleado polo seu id
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return

    sentencia_delete = """
        delete from empleado where id=%(id)s
        """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_delete, {'id': id})
            conn.commit()
            print(f"[✓] {cur.rowcount} fila(s) eliminadas")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print(f"[✗] Non se pode eliminar ao empregado {id} porque é director dalgún departamento")
            else:
                print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def delete_depts_by_keyword(conn):
    """
    Elimina unha fila na táboa departamento polo seu id
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    keyword = request_keyword()
    if keyword is None:
        print(f"[✗] É obrigatorio especificar a palabra clave")
        return

    sentencia_delete = """
            delete from departamento where nombre like %(keyword)s
            """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_delete, {'keyword': "%" + keyword + "%"})
            conn.commit()
            print(f"[✓] {cur.rowcount} fila(s) eliminadas")
        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def delete_pros_by_loc(conn):
    """
    Elimina unha fila na táboa proxecto pola sua localidade
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    loc = request_localidade()
    if loc is None:
        print(f"[✗] É obrigatorio especificar a localidade")
        return

    sentencia_delete = """
        delete from proyecto where localidad like %(loc)s
        """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sentencia_delete, {'loc': loc})
            conn.commit()
            print(f"[✓] {cur.rowcount} fila(s) eliminadas")
        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def insert_rel_emp_pro(conn):
    """
    Pide por teclado os datos dun empregado e dun proxecto e os
    relaciona
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    emp_id = request_id_of("do empregado")
    if emp_id is None:
        print(f"[✗] É obrigatorio especificar o id do empregado")
        return None
    pro_id = request_id_of("do proxecto")
    if pro_id is None:
        print(f"[✗] É obrigatorio especificar o id do proxecto")
        return None

    sentenza_select_emppro = """
                select id_empleado from EmpleadoProyecto where (id_empleado = %(emp_id)s) and (id_proyecto = %(pro_id)s)
            """

    sentenza_select_empregado = """
            select id from empleado where (id = %(emp_id)s)
        """

    sentenza_select_proxecto = """
            select id from proyecto where (id = %(pro_id)s)
        """

    sentenza_insert = """
        insert into EmpleadoProyecto(id_empleado, id_proyecto, horas)
        values(%(emp_id)s, %(pro_id)s, 0)
    """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if emp_id is not None:
                cur.execute(sentenza_select_empregado, {'emp_id': emp_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o empregado con id " + str(emp_id))
                    return None
            if pro_id is not None:
                cur.execute(sentenza_select_proxecto, {'pro_id': pro_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o proxecto con id " + str(pro_id))
                    return None

            cur.execute(sentenza_select_emppro, {'emp_id': emp_id, 'pro_id': pro_id})
            if cur.rowcount > 0:
                conn.rollback()
                print(f"[✗] Xa existe esta relación")
                return None

            cur.execute(sentenza_insert, {'emp_id': emp_id, 'pro_id': pro_id})

            conn.commit()
            print(f"[✓] Relación creada")

        except psycopg2.Error as e:
            print(F"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def insert_rel_dept_pro(conn):
    """
    Pide por teclado os datos dun departametno e dun proxecto e os
    relaciona
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    dept_id = request_id_of("do departamento")
    if dept_id is None:
        print(f"[✗] É obrigatorio especificar o id do departamento")
        return None
    pro_id = request_id_of("do proxecto")
    if pro_id is None:
        print(f"[✗] É obrigatorio especificar o id do proxecto")
        return None

    sentenza_select_deptpro = """
                select id_departamento from DepartamentoProyecto where (id_departamento = %(dept_id)s) and (id_proyecto = %(pro_id)s)
            """

    sentenza_select_departamento = """
            select id from departamento where (id = %(dept_id)s)
        """

    sentenza_select_proxecto = """
            select id from proyecto where (id = %(pro_id)s)
        """

    sentenza_insert = """
        insert into DepartamentoProyecto(id_departamento, id_proyecto)
        values(%(dept_id)s, %(pro_id)s)
    """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if dept_id is not None:
                cur.execute(sentenza_select_departamento, {'dept_id': dept_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o departamento con id " + str(dept_id))
                    return None
            if pro_id is not None:
                cur.execute(sentenza_select_proxecto, {'pro_id': pro_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o proxecto con id " + str(pro_id))
                    return None

            cur.execute(sentenza_select_deptpro, {'dept_id': dept_id, 'pro_id': pro_id})
            if cur.rowcount > 0:
                conn.rollback()
                print(f"[✗] Xa existe esta relación")
                return None

            cur.execute(sentenza_insert, {'dept_id': dept_id, 'pro_id': pro_id})

            conn.commit()
            print(f"[✓] Relación creada")

        except psycopg2.Error as e:
            print(F"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def get_pros_of_emp(conn):
    """
    Pide por teclado o id de empregado
    :param conn: a conexion aberta á bd
    :return: Proxectos no que traballa o empleado (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    id = request_id_of("do empregado")
    if id is None:
        print(f"[✗] É obrigatorio especificar o id do empregado")
        return None

    sentenza_select_empregado = """
            select id from empleado where (id = %(id)s)
        """

    sentenza_select_principal = """select EmpleadoProyecto.id_proyecto, Proyecto.nombre, EmpleadoProyecto.horas from EmpleadoProyecto 
                            left join proyecto on EmpleadoProyecto.id_proyecto=Proyecto.id
                            where EmpleadoProyecto.id_empleado=%(id)s"""

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if id is not None:
                cur.execute(sentenza_select_empregado, {'id': id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o empregado con id " + str(id))
                    return None

            cur.execute(sentenza_select_principal, {'id': id})

            row = cur.fetchone()
            while row:
                print(f"\tFila {cur.rownumber}: [id: {row[0]}, nome: {row[1]} , horas: {row[2]}]")
                row = cur.fetchone()
            print(f"[✓] Total de proxectos: {cur.rowcount}")
            conn.commit()

        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()
            return None


## ------------------------------------------------------------
def get_depts_of_pro(conn):
    """
    Pide por teclado o id de proxecto
    :param conn: a conexion aberta á bd
    :return: Departamentos que traballan nos proxectos (None se no existe)
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    id = request_id_of("do proxecto")
    if id is None:
        print(f"[✗] É obrigatorio especificar o id do proxecto")
        return None

    sentenza_select_proxecto = """
            select id from proyecto where (id = %(id)s)
        """

    sentenza_select_principal = """select DepartamentoProyecto.id_departamento, Departamento.nombre from DepartamentoProyecto 
                            left join departamento on DepartamentoProyecto.id_departamento=Departamento.id
                            where DepartamentoProyecto.id_proyecto=%(id)s """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if id is not None:
                cur.execute(sentenza_select_proxecto, {'id': id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o proxecto con id " + str(id))
                    return None

            cur.execute(sentenza_select_principal, {'id': id})

            row = cur.fetchone()
            while row:
                print(f"\tFila {cur.rownumber}: [id: {row[0]}, nome: {row[1]}]")
                row = cur.fetchone()
            print(f"[✓] Total de departamentos: {cur.rowcount}")
            conn.commit()

        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()
            return None


## ------------------------------------------------------------
def update_hours_emppro(conn):
    """
    Pide por teclado o id de empregado, o id de proxecto e
    as horas que traballa nel
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    emp_id = request_id_of("do empregado")
    if emp_id is None:
        print(f"[✗] É obrigatorio especificar o id do empregado")
        return None
    pro_id = request_id_of("do proxecto")
    if pro_id is None:
        print(f"[✗] É obrigatorio especificar o id do proxecto")
        return None
    horas = request_horas()
    if horas is None:
        print(f"[✗] É obrigatorio especificar as horas a sumar")
        return None

    sentenza_select_emppro = """
                select horas from EmpleadoProyecto where (id_empleado = %(emp_id)s) and (id_proyecto = %(pro_id)s)
            """

    sentenza_select_empregado = """
            select id from empleado where (id = %(emp_id)s)
        """

    sentenza_select_proxecto = """
            select id from proyecto where (id = %(pro_id)s)
        """

    sentenza_update = """
        update EmpleadoProyecto set horas = horas + %(horas)s where (id_empleado = %(emp_id)s) and (id_proyecto = %(pro_id)s)
    """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if emp_id is not None:
                cur.execute(sentenza_select_empregado, {'emp_id': emp_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o empregado con id " + str(emp_id))
                    return None
            if pro_id is not None:
                cur.execute(sentenza_select_proxecto, {'pro_id': pro_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o proxecto con id " + str(pro_id))
                    return None

            cur.execute(sentenza_select_emppro, {'emp_id': emp_id, 'pro_id': pro_id})
            if cur.rowcount == 0:
                conn.rollback()
                print(f"[✗] Non existe a relación entre empregado " + str(emp_id) + " e proxecto " + str(pro_id))
                return None

            row = cur.fetchone()
            print(f"RESULTADO: [id_empregado: {emp_id}, id_proxecto: {pro_id}, horas resultantes: {row[0] + horas}]")
            confirmacion = request_changes_confirmation()

            if confirmacion:
                cur.execute(sentenza_update, {'horas': horas, 'emp_id': emp_id, 'pro_id': pro_id})
                conn.commit()
                print(f"[✓] Horas actualizadas")
            else:
                conn.rollback()
                print(f"[✗] Actualización cancelada polo usuario")

        except psycopg2.Error as e:
            print(F"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def update_reemplazar_emp_emppro(conn):
    """
    Pide por teclado os ids dos empregados a reemplazar no proxecto
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    emp_out_id = request_id_of("do empregado a retirar do proxecto")
    if emp_out_id is None:
        print(f"[✗] É obrigatorio especificar o id do empregado a retirar")
        return None
    emp_in_id = request_id_of("do empregado sustituto")
    if emp_in_id is None:
        print(f"[✗] É obrigatorio especificar o id do empregado sustituto")
        return None
    if emp_in_id == emp_out_id:
        print(f"[✗] Un empregado no se pode sustituír a sí mesmo")
        return None
    pro_id = request_id_of("do proxecto")
    if pro_id is None:
        print(f"[✗] É obrigatorio especificar o id do proxecto")
        return None

    sentenza_select_emppro_out = """
                select id_empleado from EmpleadoProyecto where (id_empleado = %(emp_out_id)s) and (id_proyecto = %(pro_id)s)
            """

    sentenza_select_emppro_in = """
                select id_empleado from EmpleadoProyecto where (id_empleado = %(emp_in_id)s) and (id_proyecto = %(pro_id)s)
            """

    sentenza_select_empregado_out = """
            select id from empleado where (id = %(emp_out_id)s)
        """

    sentenza_select_empregado_in = """
            select id from empleado where (id = %(emp_in_id)s)
        """

    sentenza_select_proxecto = """
            select id from proyecto where (id = %(pro_id)s)
        """

    sentenza_delete_out = """
        delete from EmpleadoProyecto where id_empleado=%(emp_out_id)s and id_proyecto=%(pro_id)s
    """

    sentenza_insert_in = """
        insert into EmpleadoProyecto(id_empleado, id_proyecto, horas)
        values(%(emp_in_id)s, %(pro_id)s, 0)
    """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if emp_out_id is not None and emp_in_id is not None:
                cur.execute(sentenza_select_empregado_out, {'emp_out_id': emp_out_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o empregado con id " + str(emp_out_id))
                    return None
                cur.execute(sentenza_select_empregado_in, {'emp_in_id': emp_in_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o empregado con id " + str(emp_out_id))
                    return None

            if pro_id is not None:
                cur.execute(sentenza_select_proxecto, {'pro_id': pro_id})
                if cur.rowcount == 0:
                    conn.rollback()
                    print(f"[✗] Non existe o proxecto con id " + str(pro_id))
                    return None

            cur.execute(sentenza_select_emppro_out, {'emp_out_id': emp_out_id, 'pro_id': pro_id})
            if cur.rowcount == 0:
                conn.rollback()
                print(f"[✗] Non existe a relación entre empregado " + str(emp_out_id) + " e proxecto " + str(pro_id))
                return None

            cur.execute(sentenza_select_emppro_in, {'emp_in_id': emp_in_id, 'pro_id': pro_id})
            if cur.rowcount > 0:
                conn.rollback()
                print(f"[✗] Xa existe a relación entre empregado " + str(emp_out_id) + " e proxecto " + str(pro_id))
                return None

            cur.execute(sentenza_delete_out, {'emp_out_id': emp_out_id, 'pro_id': pro_id})
            cur.execute(sentenza_insert_in, {'emp_in_id': emp_in_id, 'pro_id': pro_id})

            conn.commit()
            print(f"[✓] Empregado reemprazado")

        except psycopg2.Error as e:
            print(F"[✗]Error xenérico: {e.pgcode}: {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
def get_directed_depts_by_id(conn):
    """
    Pide por teclado ao usuario o id do empregado do que queremos ver
    os departamentos que dirixe
    :param conn: a conexion aberta á bd
    :return: nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    id = request_id()
    if id is None:
        print(f"[✗] É obrigatorio especificar o id")
        return None

    sentenza_select_emp = """select id from empleado where id=%(id)s"""
    sentenza_select_depts = """select id, nombre from departamento where id_director=%(id)s"""

    with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
        try:

            cur.execute(sentenza_select_emp, {'id': id})
            row = cur.fetchone()
            if row is None:
                print(f"[✓] Non existe o empregado con id {id}")
                conn.commit()
                return None
            else:
                cur.execute(sentenza_select_depts, {'id': id})
                row = cur.fetchone()

                if row is None:
                    print(f"[✓] O empregado {id} non dirixe ningún departamento")
                    conn.commit()
                    return None
                else:
                    while row:
                        print(f"\tFila {cur.rownumber}: [id: {row[0]}, nome: {row[1]}]")
                        row = cur.fetchone()
                    print(f"[✓] Total de departamentos dirixidos polo empregado {id}: {cur.rowcount}")

                    conn.commit()
                    return None

        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()
            return None

## ------------------------------------------------------------
def update_dept_director(conn):
    """
    Pide por teclado ao usuario o id do departamento e o id do empregado
    que vai a ser o novo director do departamento
    :param conn: a conexion aberta á bd
    :return: nada
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    id_dept = request_id_of("do departamento")
    if id_dept is None:
        print(f"[✗] É obrigatorio especificar o id do departamento")
        return None
    id_emp = request_id_of("do novo director")
    if id_dept is None:
        print(f"[✗] É obrigatorio especificar o id do novo director")
        return None

    sentenza_select_dept = """select id from departamento where id=%(id)s"""
    sentenza_select_emp = """select id from empleado where id=%(id)s"""
    sentenza_update = """update departamento set id_director = %(id_emp)s where (id = %(id_dept)s)"""

    with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
        try:

            cur.execute(sentenza_select_dept, {'id': id_dept})
            row = cur.fetchone()
            if row is None:
                print(f"[✓] Non existe o departamento {id_dept}")
                conn.commit()
                return None

            cur.execute(sentenza_select_emp, {'id': id_emp})
            row = cur.fetchone()
            if row is None:
                print(f"[✓] Non existe o empregado con id {id_emp}")
                conn.commit()
                return None

            cur.execute(sentenza_update, {'id_emp': id_emp, 'id_dept': id_dept})

            conn.commit()
            print(f"[✓] Director actualizado")
            return None

        except psycopg2.Error as e:
            print(f"[✗] Erro xeral de postgres: {e.pgcode} - {e.pgerror}")
            conn.rollback()
            return None

## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """

    MENU_TEXT = """
    -- MENÚ --
    1  - Obter toda a info dun empregado polo seu id
    2  - Obter toda a info dun departamento polo seu id
    3  - Obter toda a info dun proxecto polo seu id
    4  - Obter empregados con salario maior ao introducido
    5  - Obter os departamentos dunha localidade
    6  - Obter os proxectos dunha localidade
    7  - Obter os proxectos dun empregado
    8  - Obter os departamentos participantes nun proxecto
    9  - Obter os departamentos que dirixe un empregado
    10 - Insertar un novo empregado
    11 - Insertar un novo departamento
    12 - Insertar un novo proxecto
    13 - Incrementar o salario dun empregado por porcentaxe
    14 - Actualizar a comisión dun empregado
    15 - Actualizar o director dun empregado
    16 - Sumar horas traballadas dun empregado nun proxecto
    17 - Reemprazar empregado nun proxecto
    18 - Eliminar un empregado polo seu id
    19 - Eliminar os departamentos que conteñan no seu nome o introducido
    20 - Eliminar os proxectos cuxa localidade sexa a indicada
    21 - Relacionar empregado con proxecto
    22 - Relacionar departamento con proxecto
    q  - Saír   
    """
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            get_emp_by_id(conn)
        elif tecla == '2':
            get_dept_by_id(conn)
        elif tecla == '3':
            get_pro_by_id(conn)
        elif tecla == '4':
            get_emps_by_sal(conn)
        elif tecla == '5':
            get_depts_by_loc(conn)
        elif tecla == '6':
            get_pros_by_loc(conn)
        elif tecla == '7':
            get_pros_of_emp(conn)
        elif tecla == '8':
            get_depts_of_pro(conn)
        elif tecla == '9':
            get_directed_depts_by_id(conn)
        elif tecla == '10':
            insert_emp(conn)
        elif tecla == '11':
            insert_dept(conn)
        elif tecla == '12':
            insert_pro(conn)
        elif tecla == '13':
            update_emp_sal_by_percentage(conn)
        elif tecla == '14':
            update_emp_comm(conn)
        elif tecla == '15':
            update_dept_director(conn)
        elif tecla == '16':
            update_hours_emppro(conn)
        elif tecla == '17':
            update_reemplazar_emp_emppro(conn)
        elif tecla == '18':
            delete_emp_by_id(conn)
        elif tecla == '19':
            delete_depts_by_keyword(conn)
        elif tecla == '20':
            delete_pros_by_loc(conn)
        elif tecla == '21':
            insert_rel_emp_pro(conn)
        elif tecla == '22':
            insert_rel_dept_pro(conn)

## ------------------------------------------------------------
def main():
    """
    Función principal. Conecta á bd e executa o menú.
    Cando sae do menú, desconecta da bd e remata o programa
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    menu(conn)
    disconnect_db(conn)


## ------------------------------------------------------------
if __name__ == '__main__':
    main()
