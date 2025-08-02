#!/usr/bin/env python3
from api.app.config import settings
from sqlalchemy import create_engine, inspect
import sys
import os

# Agregar el directorio de la aplicación al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))


def check_table_structure():
    engine = create_engine(settings.database_url)
    inspector = inspect(engine)

    # Verificar si la tabla users existe
    tables = inspector.get_table_names()
    print(f"Tablas existentes: {tables}")

    if 'users' in tables:
        print("\nEstructura de la tabla 'users':")
        columns = inspector.get_columns('users')
        for column in columns:
            print(
                f"  - {column['name']}: {column['type']} (nullable: {column['nullable']})")
    else:
        print("La tabla 'users' no existe")


if __name__ == "__main__":
    check_table_structure()
