# Project TODOs & Enhancements

## 1. Architectural & Code Improvements
- [x] **Settings Management with Pydantic:** Refactor configuration to use Pydantic's `BaseSettings` for environment variables to ensure type safety and easy testing.
- [x] **Migrate to Native SQLAlchemy 2.0 Async:** Replace the `databases` library with SQLAlchemy 2.0 native `AsyncSession` or Async Core for better long-term maintainability.
- [x] **Dependency Injection for Database/CRUD:** Use FastAPI's `Depends()` to inject database sessions into route handlers. This improves testability by removing the need to monkeypatch `crud` functions.
- [x] **Implement Alembic for Migrations:** Set up `alembic` to manage database schema changes instead of relying on `metadata.create_all(engine)` on app startup.

## 2. Database Optimizations
- [x] **Add Database Indexes:** Add indexes to columns frequently used in filtering and sorting (e.g., `created_date`, `completed`). Consider text search indexes for `title` and `description` if search becomes heavily used.
- [x] **Connection Pooling:** Configure the database engine with appropriate connection pool limits (`pool_size`, `max_overflow`).

## 3. Feature Additions
- [x] **Soft Deletes:** Add an `is_deleted` boolean column to soft-delete records instead of permanently dropping them.
- [x] **Tags & Categories:** Add the ability to organize notes using tags (e.g., an `ARRAY(String)` column or a separate relationship table).
- [x] **Authentication & Authorization:** Implement user accounts using OAuth2 and JWT tokens, allowing users to manage their own private notes.

## 4. Frontend (Vue.js) Enhancements
- [x] **Complete CRUD UI:** Add forms and buttons to create, update, and delete notes from the Vue application.
- [x] **Environment Configuration:** Update `Api.js` to use Vite environment variables (`import.meta.env.VITE_API_URL`) instead of hardcoding `http://localhost:8002`.
- [x] **State Management & UI Polish:** Introduce a state manager (like Pinia) and a UI library (like Tailwind CSS) to improve the frontend's architecture and look.
