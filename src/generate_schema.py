"""
Schema visualization generator for the Real Estate Database
Uses ERAlchemy to generate visual database schema diagrams
"""

import os
import sys

try:
    from eralchemy import render_er

    print("ERAlchemy is available")
except ImportError:
    print("ERAlchemy not found. Installing...")
    os.system("pip install eralchemy")
    try:
        from eralchemy import render_er

        print("ERAlchemy installed successfully")
    except ImportError:
        print(
            "Failed to install ERAlchemy. Please install manually: pip install eralchemy"
        )
        sys.exit(1)


def generate_schema_diagram():
    """Generate ER diagram from the SQLite database"""

    # database file path
    db_path = "database/real_estate.db"

    # create schemas directory
    schema_dir = "schemas"
    if not os.path.exists(schema_dir):
        os.makedirs(schema_dir)
        print(f"Created directory: {schema_dir}")

    # check if database exists
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found.")
        print("Please run 'python src/createdb.py' first to create the database.")
        return

    print("Generating database schema diagram...")

    # generate basic schema files
    try:
        # generate DOT file
        print("Creating DOT file...")
        basic_dot = os.path.join(schema_dir, "real_estate_schema.dot")
        render_er(f"sqlite:///{db_path}", basic_dot)
        print(f"✓ Successfully created {basic_dot}")

        # generate PNG file
        print("Creating PNG file...")
        basic_png = os.path.join(schema_dir, "real_estate_schema.png")
        render_er(f"sqlite:///{db_path}", basic_png)
        print(f"✓ Successfully created {basic_png}")

    except Exception as e:
        print(f"✗ Failed to create schema files: {str(e)}")

    print("\nSchema generation complete!")
    print(f"\nGenerated files in {schema_dir}/ directory:")

    # list generated files
    generated_files = ["real_estate_schema.dot", "real_estate_schema.png"]

    for file_name in generated_files:
        full_path = os.path.join(schema_dir, file_name)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  - {file_name} ({size:,} bytes)")


def print_table_info():
    """Print information about tables in the database"""
    import sqlite3

    db_path = "database/real_estate.db"

    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"\nDatabase: {db_path}")
        print(f"Total tables: {len(tables)}")
        print("\nTable Information:")
        print("-" * 60)

        for (table_name,) in tables:
            # get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            # get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]

            print(f"\n{table_name}:")
            print(f"  Columns: {len(columns)}")
            print(f"  Rows: {row_count:,}")

            # print column details
            print("  Schema:")
            for col in columns:
                col_id, name, data_type, not_null, default_val, primary_key = col
                pk_marker = " (PK)" if primary_key else ""
                null_marker = " NOT NULL" if not_null else ""
                print(f"    - {name}: {data_type}{null_marker}{pk_marker}")

        conn.close()

    except Exception as e:
        print(f"Error reading database: {str(e)}")


def main():
    """Main function to generate schema and print database info"""

    print("=" * 70)
    print("Real Estate Database Schema Generator")
    print("=" * 70)

    # print database information
    print_table_info()

    print("\n" + "=" * 70)

    # generate schema diagrams
    generate_schema_diagram()

    print("\n" + "=" * 70)
    print("Schema generation process completed!")

    # additional instructions
    print("\nTo view the schema diagram:")
    print("1. Open 'schemas/real_estate_schema.png' to view the database schema")
    print(
        "2. Use 'schemas/real_estate_schema.dot' with Graphviz tools for customization"
    )
    print(f"\nAll schema files are organized in the 'schemas/' directory.")


if __name__ == "__main__":
    main()
