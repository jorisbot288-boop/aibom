import json
import click
from pathlib import Path
from datetime import datetime
from .scanner import scan_project
from . import __version__

@click.group()
def cli():
    """AIBOM: Generate EU AI Act Annex IV compliance documentation."""
    pass

@cli.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False, writable=True),
    help="Output file (default: stdout)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "markdown"]),
    default="json",
    help="Output format",
)
def scan(path, output, format):
    """Scan a Python project for datasets, models, and APIs."""
    result = scan_project(Path(path))
    
    if format == "json":
        content = json.dumps(result, indent=2)
    else:
        content = generate_markdown(result)
    
    if output:
        Path(output).write_text(content)
        click.echo(f"Report written to {output}")
    else:
        click.echo(content)

@cli.command()
def version():
    """Show the AIBOM version."""
    click.echo(__version__)

def generate_markdown(data):
    """Convert scan result to markdown tables."""
    lines = [
        f"# AIBOM Report",
        f"Generated at: {data['generated_at']}",
        f"Project path: {data['project_path']}",
        f"AIBOM version: {data['aibom_version']}",
        "",
    ]
    
    if data["datasets"]:
        lines.extend(["## Datasets", "| Name | Source | Source URL | Detected In |", "|------|--------|------------|-------------|"])
        for ds in data["datasets"]:
            lines.append(f"| {ds['name']} | {ds['source']} | {ds['source_url'] or ''} | {ds['detected_in']} |")
        lines.append("")
    
    if data["models"]:
        lines.extend(["## Models", "| Name | Provider | Model Card URL | Detected In |", "|------|----------|----------------|-------------|"])
        for model in data["models"]:
            lines.append(f"| {model['name']} | {model['provider']} | {model['model_card_url'] or ''} | {model['detected_in']} |")
        lines.append("")
    
    if data["apis"]:
        lines.extend(["## APIs", "| Provider | Endpoint Pattern | Detected In |", "|----------|------------------|-------------|"])
        for api in data["apis"]:
            lines.append(f"| {api['provider']} | {api['endpoint_pattern']} | {api['detected_in']} |")
        lines.append("")
    
    if not data["datasets"] and not data["models"] and not data["apis"]:
        lines.append("No datasets, models, or APIs detected.")
    
    return "\n".join(lines)

if __name__ == "__main__":
    cli()