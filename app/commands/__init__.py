def register_commands(app):
    """Register CLI commands with the Flask application"""
    from app.commands.import_csv import import_csv
    app.cli.add_command(import_csv)