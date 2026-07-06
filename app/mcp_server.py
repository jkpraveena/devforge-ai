from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("devforge-server")

@mcp.tool()
def validate_package_structure(structure: list[str]) -> str:
    """Validates the proposed directory structure list of files and folders for completeness.
    
    Args:
        structure: A list of paths representing the proposed folder layout.
    """
    required = ["README.md", "tests", "app"]
    missing = [req for req in required if not any(req in path for path in structure)]
    if missing:
        return f"Warning: The structure is missing important components: {', '.join(missing)}"
    return "Success: The proposed structure includes all standard project files and folders."

@mcp.tool()
def estimate_development_time(features_count: int, tables_count: int, endpoints_count: int) -> str:
    """Estimates the total development time (in developer hours) based on scope parameters.
    
    Args:
        features_count: The number of features planned for the application.
        tables_count: The number of database tables in the design.
        endpoints_count: The number of REST API endpoints planned.
    """
    base_hours = features_count * 8
    db_hours = tables_count * 4
    api_hours = endpoints_count * 6
    total_hours = base_hours + db_hours + api_hours
    
    return f"Total estimated development time is {total_hours} developer-hours (Features: {base_hours}h, DB: {db_hours}h, API: {api_hours}h)."

@mcp.tool()
def generate_boilerplate_structure(tech_stack: str) -> str:
    """Generates standard project structure guidelines for a specific technology stack.
    
    Args:
        tech_stack: The technology stack name (e.g., 'FastAPI', 'React', 'Django').
    """
    stack = tech_stack.lower()
    if "fastapi" in stack:
        return """Proposed FastAPI project structure:
- app/
  - __init__.py
  - main.py
  - config.py
  - api/
    - endpoints/
  - models/
  - schemas/
- tests/
- README.md
- pyproject.toml"""
    elif "react" in stack:
        return """Proposed React project structure:
- src/
  - assets/
  - components/
  - hooks/
  - pages/
  - App.jsx
  - main.jsx
- public/
- package.json
- README.md"""
    else:
        return f"""Proposed generic stack project structure for {tech_stack}:
- src/
- tests/
- docs/
- README.md
- requirements.txt"""

if __name__ == "__main__":
    mcp.run(transport="stdio")
