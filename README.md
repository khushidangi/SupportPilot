# SupportPilot

SupportPilot is a lightweight customer support assistant demonstrating OOP design, a Flask backend, a Supabase database backend, and a small frontend built with HTML/CSS/JS.

## Features
- Create and view tickets
- Rule-based ticket categorization
- Rule-based sentiment analysis
- Auto-reply templates and simple summarization
- FAQ knowledge base with search

## Architecture
- Frontend: static HTML/CSS/JS in `supportpilot/frontend`
- Backend: Flask app in `supportpilot/backend/app.py` exposing REST endpoints
- Database: Supabase (Postgres) with tables for `users`, `tickets`, `messages`, `faq`
- OOP modules located in `supportpilot/backend/models`

## Project Structure

```
supportpilot/
	backend/
		app.py
		models/
			user.py
			customer.py
			agent.py
			ticket.py
			knowledge_base.py
			faq_kb.py
			sentiment_analyzer.py
			chat_engine.py
			router.py
		services/
			supabase_client.py
			ticket_service.py
			user_service.py
	frontend/
		index.html
		dashboard.html
		ticket.html
		faq.html
		static/
			css/
				style.css
			js/
				main.js
requirements.txt
```

## Supabase Setup
1. Create a Supabase project at supabase.com and note `SUPABASE_URL` and `SUPABASE_KEY`.
2. Create the following tables (SQL snippets):

```sql
create table users(id text primary key, name text, email text, type text);
create table tickets(id text primary key, user_id text, category text, sentiment jsonb, status text, assigned_agent text, subject text, created_at double precision);
create table messages(id bigserial primary key, ticket_id text, sender text, message text, timestamp double precision);
create table faq(id bigserial primary key, question text, answer text);
```

## Environment
Create a `.env` file in your environment root with:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-or-anon-key
PORT=5000
```

## Run Locally
1. Create and activate a virtualenv:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the backend (from repository root):

```bash
python supportpilot/backend/app.py
```

4. Open `supportpilot/frontend/index.html` in your browser or serve the `frontend` folder with a static server.

## API Endpoints
- `POST /create_ticket` - create a ticket with JSON `{user_id, subject, message}`
- `GET /get_tickets?user_id=...` - list tickets
- `POST /analyze_sentiment` - analyze text `{text}`
- `POST /auto_reply` - get auto reply `{text, role}`
- `POST /assign_agent` - assign agent `{ticket_id, agent_id}`
- `GET /get_faq?q=term` - search FAQ

## Notes
- The AI features are rule-based and lightweight; no external model dependencies.
- Adjust Supabase client usage in `supportpilot/backend/services/supabase_client.py` as needed for production keys.

If you want, I can run a quick smoke-check or help populate the FAQ table with example entries.