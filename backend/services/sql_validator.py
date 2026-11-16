
import re


def validate_sql(sql_query):

    # Remove extra spaces
    query = sql_query.strip()

    # Remove trailing semicolon
    query = query.rstrip(";").strip()

    # Allow only SELECT statements
    if not re.match(r"^SELECT\b", query, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")

    # Block multiple SQL statements
    if ";" in query:
        raise ValueError("Multiple SQL statements are not allowed.")

    # Block dangerous SQL operations and commands
    forbidden = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "ATTACH",
        "DETACH",
        "COPY",
        "EXPORT",
        "IMPORT",
        "INSTALL",
        "LOAD",
        "CALL",
        "PRAGMA",
        "SET",
        "RESET"
    ]

    pattern = r"\b(" + "|".join(forbidden) + r")\b"

    if re.search(pattern, query, re.IGNORECASE):
        raise ValueError("Unsafe SQL operation detected.")

    # Allow access only to uploaded_data
    tables = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        query,
        re.IGNORECASE
    )

    if not tables:
        raise ValueError("Query must read from uploaded_data.")

    if any(table.lower() != "uploaded_data" for table in tables):
        raise ValueError("Only uploaded_data table is allowed.")

    return query


if __name__ == "__main__":

    test_query = "SELECT SUM(Sales) FROM uploaded_data;"

    try:
        result = validate_sql(test_query)
        print("SQL VALIDATION SUCCESSFUL!")
        print("Validated Query:", result)

    except ValueError as error:
        print("SQL REJECTED:", error)
