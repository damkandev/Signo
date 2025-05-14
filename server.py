from mcp.server.fastmcp import FastMCP
import psycopg2
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pdfkit
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

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
def crear_contrato(nombre_empleado: str, dni_empleado: str, objeto_contrato:str, empleado_pago:int, nombre_proyecto: str, nombre_empresa: str, horas_semanales:int, fecha_inicio:str, fecha_fin:str) -> str:
    """Genera un contrato en formato PDF con la información del empleado y el proyecto"""
    try:
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        template_name = "plantilla.html"
        output_dir = r"C:\contratos"

        os.makedirs(output_dir, exist_ok=True)
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)

        contexto = {
            'nombre_empleado': nombre_empleado,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'horas_semanales': horas_semanales,
            'nombre_empresa': nombre_empresa,
            'dni_empleado': dni_empleado,
            'objeto_contrato': objeto_contrato,
            'empleado_pago': empleado_pago,
            'nombre_proyecto': nombre_proyecto
        }

        html_renderizado = template.render(contexto)

        html_temp_path = os.path.join(output_dir, "temp.html")
        with open(html_temp_path, "w", encoding="utf-8") as f:
            f.write(html_renderizado)

        filename = f"contrato_{nombre_empleado.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        output_pdf_path = os.path.join(output_dir, filename)

        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_file(html_temp_path, output_pdf_path, configuration=config)

        return output_pdf_path

    except Exception as e:
        return f"Error al generar el contrato: {str(e)}"
