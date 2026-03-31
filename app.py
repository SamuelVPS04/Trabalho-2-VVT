from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

load_dotenv()


def _configuracao_mysql(
    host: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
    port: Optional[int] = None,
) -> dict[str, str | int | bool]:
    return {
        "host": host or os.getenv("MYSQL_HOST", "localhost"),
        "user": user or os.getenv("MYSQL_USER", "root"),
        "password": password if password is not None else os.getenv("MYSQL_PASSWORD", ""),
        "database": database or os.getenv("MYSQL_DATABASE", "db_vvt"),
        "port": port or int(os.getenv("MYSQL_PORT", "3306")),
        "autocommit": False,
    }


def inicializar_banco(config: dict[str, str | int | bool]) -> None:
    registros_iniciais = [
        ("BRC0001A", 1, "C", "A", "BR"),
        ("BRD0001I", 1, "D", "I", "BR"),
        ("BRA0001K", 1, "A", "K", "BR"),
        ("BRF0001F", 1, "F", "F", "BR"),
        ("BRG0001A", 1, "G", "A", "BR"),
        ("BRC0002A", 2, "C", "A", "BR"),
        ("BRD0002K", 2, "D", "K", "BR"),
        ("BRF0002A", 2, "F", "A", "BR"),
        ("BRC0003C", 3, "C", "C", "BR"),
    ]

    database = str(config["database"])
    admin_config = {key: value for key, value in config.items() if key != "database"}
    conn = mysql.connector.connect(**admin_config)
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.execute(f"USE `{database}`")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS codigos_sequenciais (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(8) NOT NULL UNIQUE,
                sec INT NOT NULL,
                Grupo CHAR(1) NOT NULL,
                Tipo_Alimento CHAR(1) NOT NULL,
                Pais CHAR(2) NOT NULL,
                CONSTRAINT chk_sec_positivo CHECK (sec > 0),
                CONSTRAINT uq_pais_grupo_sec UNIQUE (Pais, Grupo, sec)
            ) ENGINE=InnoDB
            """
        )
        cursor.execute("SELECT COUNT(*) FROM codigos_sequenciais")
        total_registros = int(cursor.fetchone()[0])
        if total_registros == 0:
            cursor.executemany(
                """
                INSERT INTO codigos_sequenciais (codigo, sec, Grupo, Tipo_Alimento, Pais)
                VALUES (%s, %s, %s, %s, %s)
                """,
                registros_iniciais,
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def conectar_mysql(
    host: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
    port: Optional[int] = None,
) -> MySQLConnection:
    config = _configuracao_mysql(host, user, password, database, port)

    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as exc:
        if exc.errno != errorcode.ER_BAD_DB_ERROR:
            raise

        inicializar_banco(config)
        return mysql.connector.connect(**config)


def normalizar_parametros(grupo: str, tipo_alimento: str, pais: str) -> tuple[str, str, str]:
    grupo_normalizado = (grupo or "").strip().upper()
    tipo_normalizado = (tipo_alimento or "").strip().upper()
    pais_normalizado = (pais or "").strip().upper()
    return grupo_normalizado, tipo_normalizado, pais_normalizado


def validar_parametros(grupo: str, tipo_alimento: str, pais: str) -> tuple[str, str, str]:
    grupo, tipo_alimento, pais = normalizar_parametros(grupo, tipo_alimento, pais)

    if len(grupo) != 1:
        raise ValueError("O parâmetro 'grupo' deve conter exatamente 1 caractere não vazio.")

    if len(tipo_alimento) != 1:
        raise ValueError("O parâmetro 'tipo_alimento' deve conter exatamente 1 caractere não vazio.")

    if len(pais) != 2:
        raise ValueError("O parâmetro 'pais' deve conter exatamente 2 caracteres.")

    return grupo, tipo_alimento, pais


def gerar_codigo(cursor: MySQLCursor, grupo: str, tipo_alimento: str, pais: str) -> tuple[str, int]:
    grupo, tipo_alimento, pais = validar_parametros(grupo, tipo_alimento, pais)

    cursor.execute(
        """
        SELECT COALESCE(MAX(sec), 0)
        FROM codigos_sequenciais
        WHERE Grupo = %s AND Pais = %s
        FOR UPDATE
        """,
        (grupo, pais),
    )
    row = cursor.fetchone()
    maior_sec = int(row[0]) if row and row[0] is not None else 0

    sec = maior_sec + 1
    codigo = f"{pais}{grupo}{sec:04d}{tipo_alimento}"

    cursor.execute(
        "SELECT COUNT(1) FROM codigos_sequenciais WHERE codigo = %s",
        (codigo,),
    )
    count_row = cursor.fetchone()
    if count_row and int(count_row[0]) > 0:
        raise ValueError(f"Código já existe: {codigo}")

    return codigo, sec


def inserir_codigo(conn: MySQLConnection, grupo: str, tipo_alimento: str, pais: str) -> tuple[int, str, int]:
    cursor = conn.cursor()

    try:
        conn.start_transaction()
        grupo, tipo_alimento, pais = validar_parametros(grupo, tipo_alimento, pais)
        codigo, sec = gerar_codigo(cursor, grupo, tipo_alimento, pais)

        cursor.execute(
            """
            INSERT INTO codigos_sequenciais (codigo, sec, Grupo, Tipo_Alimento, Pais)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (codigo, sec, grupo, tipo_alimento, pais),
        )

        conn.commit()
        return cursor.lastrowid, codigo, sec

    except mysql.connector.Error as exc:
        conn.rollback()
        if getattr(exc, "errno", None) == 1062:
            raise ValueError("Duplicidade detectada ao inserir registro.") from exc
        raise

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()


def listar_codigos(conn: MySQLConnection) -> list[tuple]:
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, codigo, sec, Grupo, Tipo_Alimento, Pais
            FROM codigos_sequenciais
            ORDER BY id
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()


def buscar_por_codigo(conn: MySQLConnection, codigo: str) -> tuple | None:
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, codigo, sec, Grupo, Tipo_Alimento, Pais
            FROM codigos_sequenciais
            WHERE codigo = %s
            """,
            (codigo,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()


if __name__ == "__main__":
    conn = conectar_mysql()
    try:
        inserted_id, codigo, sec = inserir_codigo(conn, grupo="C", tipo_alimento="A", pais="BR")
        print(f"Registro inserido com sucesso: id={inserted_id}, codigo={codigo}, sec={sec}")

        registro = buscar_por_codigo(conn, codigo)
        print("Query de validação do registro inserido:")
        print(registro)

        print("\nÚltimos registros:")
        for item in listar_codigos(conn)[-5:]:
            print(item)

    finally:
        conn.close()
