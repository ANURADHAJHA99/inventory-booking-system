from app import create_app, db

app = create_app()

# In modern Flask, use this pattern instead of before_first_request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)