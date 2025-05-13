from mcp.server.fastmcp import FastMCP
import psycopg2
import os
from jinja2 import Template
import subprocess

mcp = FastMCP("Signo")

def establecer_conexion():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD")
    )

@mcp.tool()
def select(query: str) -> str:
    """Ejecuta una consulta SELECT en la base de datos"""
    if not query.strip().lower().startswith("select"):
        return "Error: Solo se aceptan consultas SELECT"
    try:
        conn = establecer_conexion()
        cursor = conn.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return str(resultados)
    except Exception as e:
        return f"Error al ejecutar la consulta: {str(e)}"

@mcp.tool()
def listar_tablas() -> str:
    """Lista las tablas disponibles en la base de datos"""
    try:
        conn = establecer_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema, table_name;")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return str(resultados)
    except Exception as e:
        return f"Error al ejecutar la consulta: {str(e)}"

@mcp.tool()
def crear_contrato() -> str:
    pass