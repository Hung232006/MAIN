from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        nameusers="admin",
        email="admin@gmail.com",
        is_admin=True
    )
    admin.set_password("123456")
    db.session.add(admin)
    db.session.commit()
    print("Admin đã được tạo!")
