See the steps to run locally below after examples --

1. success resp
<img width="1005" height="696" alt="image" src="https://github.com/user-attachments/assets/b949bf25-8ceb-41e2-b247-1a4e570f29b5" />

2. invalid resp
<img width="1005" height="696" alt="image" src="https://github.com/user-attachments/assets/27265819-0598-4aab-b830-b7c4186f402d" />

3. programmer bug handled by central handler
return row  
return {"id": row[0], "session_id": row[1]}
<img width="1005" height="696" alt="image" src="https://github.com/user-attachments/assets/6052de14-ca05-4815-bccc-847db71882ae" />

4. succcess resp 
<img width="1005" height="696" alt="image" src="https://github.com/user-attachments/assets/ef4323c5-3844-4598-936e-cf47b619d7a3" />

5. wrong model llm error 
_gem_model = "gemini-1.5-flash"
<img width="1566" height="225" alt="image" src="https://github.com/user-attachments/assets/23eb97aa-bdac-4bbe-8d14-5a92ac3643d1" />
<img width="1022" height="623" alt="image" src="https://github.com/user-attachments/assets/0aef7f9e-7bc2-4f62-8c9b-5a14ee56bc23" />

<img width="1025" height="694" alt="image" src="https://github.com/user-attachments/assets/0d37d416-a2c0-41e7-a559-467221e50106" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="458" height="687" alt="image" src="https://github.com/user-attachments/assets/929c4bc4-23ea-4391-9019-816ab8564d42" />
<img width="456" height="269" alt="image" src="https://github.com/user-attachments/assets/db380b60-2c4b-4fe4-bef3-70d123842ac7" />

-----------------------------------------------------------------------------------------------------------------------------------

Steps --

---

# AI Live Chat Agent – 

This project implements a minimal AI-powered customer support chat widget using a real LLM.
Right now it is a chat agent . But it can  be a small part of a big product .
(Part of big product how ? )It kinda simulates --
1. To be used by ecom brand owners , creators to send automatic replies to end users when they receive messages on whatsapp , instagram etc.
2. it can be integrated with whatsapp and other chat apps to give automatic replies to end users for  incoming chat messages, persists conversations, and generates AI replies in a clean, extensible backend architecture.


---

## Features

* Simple chat API (`POST /chat/message`)
* Conversation + message persistence
* Session-based chat continuity( acts as idempotency anchor sent from client side and unique contraint in db)
* Real LLM integration (Google Gemini)
* Domain knowledge embedded in prompt
* Graceful handling of LLM/API failures
* Clean separation of concerns (API, services, DB)
* don't break ux on llm errros , log actual errors cleanly and save response as system in case of llm errors and to client return generically we cannot respond now
* break ux(raise errros in ux) only on system violation or programmer bugs , but ignore it on llm based errors for this chat based system .

---

## Tech Stack

* **Backend**: FastAPI (Python)
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy (async)
* **LLM**: Google Gemini (via SDK)
* **Frontend**: React -vite

---

---

## Data Model

### conversations

* `id` (internal PK)
* `session_id` (public identifier, unique)
* `created_at`

### messages

* `id`
* `conversation_id`
* `sender` (`user` | `ai`)
* `text`
* `created_at`

Messages belong to a conversation (1:N).
The `session_id` is used by the client to continue a chat across requests.

---

## API Contract

### `POST /chat/message`

**Request**

```json
{
  "message": "What is your return policy?",
  "sessionId": "optional-session-id"
}
```

* `sessionId` is optional on first request.
* If not provided, the server creates a new conversation.

**Response**

```json
{
  "reply": "We accept returns within 30 days if the item is unused.",
  "sessionId": "session-id-to-use-next-time"
}
```

---

## LLM Integration

* Uses **Google Gemini** (`gemini-1.5-flash`)
* API key loaded via environment variables
* Prompt includes:

  * System role (“helpful support agent”)
  * Hardcoded domain knowledge (shipping, returns, support hours)
  * Recent conversation history (last N messages)

The LLM logic is fully encapsulated in a service layer (`services/llm.py`).

---

## Error Handling Strategy

* **LLM/API failures** (timeouts, empty responses, SDK issues):

  * Caught and normalized via a custom `LLMError`
  * User receives a friendly fallback message
  * Backend does not crash
* **Invalid input**:

  * Handled via request validation
* **Unexpected bugs / invariant violations**:

  * Bubble to a global exception handler
  * Logged with stack trace
  * Returned as generic 500 errors

Graceful failure is preferred over silent failure or crashes.

---

## Setup & Running Locally

### 1. Clone the repository

```bash
git clone <repo-url>
cd <repo>
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SYNC_DB_URL=postgresql://user:password@localhost/dbname   #for alembic migs
```

---

### 5. Run migrations

```bash
alembic upgrade head
```
---

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

Server will run at:

```
http://localhost:8000
```

---

## Design Decisions & Trade-offs

* **Session ID from client**:
  Accepted as per assignment. In production, this would be generated server-side as a public conversation identifier.

* **Domain knowledge in prompt**:
  Hardcoded for simplicity. In production, this could be replaced with a RAG setup using embeddings and a vector database.

* **Synchronous LLM SDK**:
  Used for simplicity as i earlier tested sdk version for free chats. In production, calls would be replaced with async HTTP calls or offloaded to a threadpool on same server but most certainly better to use async http callls to llm .

* **No auth**:
  Omitted intentionally to keep focus on chat flow and LLM integration.

---

## If I Had More Time…

* Add retry & backoff for transient LLM failures
* Add WebSocket support for real-time UI updates
* Introduce RAG for domain knowledge
* Make history context better insated of just using recent 5-8 chats 
* Add metrics, tracing, and structured logging
* Implement channel abstraction (Web / WhatsApp / IG)


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 1️ How this assignment connects to the *real* full chat system

### What we’re building **now**

We are building a **local simulation** of one slice :

> “A backend that can take a message, persist it, call an LLM, and return a reply, while maintaining conversation continuity.”

There is:

* no WhatsApp
* no Instagram
* no webhooks
* no real external users

So the browser client **pretends** to be the message source.

That’s why:

* the client sends `sessionId`
* the backend accepts it
* the backend returns it

---

### What exists in the **real system**

In production, full product backend does **not** rely on browser session IDs.

Instead, messages come from **external channels** (WhatsApp, IG, etc.) via webhooks.

So the identity and conversation continuity come from **outside**, not from the UI.

---

## 2️ Real production message flow 

### Step 1: Brand connects a channel

A product user (brand / creator) connects WhatsApp, IG, etc.

This creates a record like:

```
channel_account
- id
- spur_user_id
- channel_type (whatsapp, instagram, etc.)
- external_account_id (business number, page ID)
```

### Step 2: End user sends a message

An end user sends a message to the brand on WhatsApp.

WhatsApp sends a webhook to Spur backend containing:

* business number (identifies channel_account)
* sender phone number (end user identity)
* message text

---

### Step 3: Backend identifies the conversation (THIS is key)

At this point, Spur backend identifies the conversation using:

```
(product_user_id, channel_type, external_user_id)
```

Where:

* `product_user_id` → the brand
* `channel_type` → WhatsApp / IG
* `external_user_id` → sender phone number / IG user ID

👉 **This triple is the real unique anchor.**

---

## 3️⃣ The real unique anchor (important)

### ✅ Production unique anchor

```
UNIQUE (product_user_id, channel_type, external_user_id)
```

This means:

* One active conversation per end user per channel per brand
* Messages append to the same conversation over time

---

## 4️ Where does the “session ID” fit in production?

### Internal identity

* Conversations are identified internally by:

  * DB primary key
  * `(product_user_id, channel, external_user_id)`
  * id

### External / UI identity

* The **UI must not** see phone numbers or internal IDs
* So generates a **public conversation ID**

Example:

```
conversation
- id (internal PK)
- public_id (UUID / ULID)
- product_user_id
- channel
- external_user_id
```

This `public_id` is what:

* the product dashboard uses
* APIs expose
* clients send back

👉 This is what your `sessionId` becomes in production.

---

## 5️⃣ Mapping this back to the assignment (very important)

| Assignment                | Production                                  |
| ------------------------- | ------------------------------------------- |
| `sessionId` from client   | `conversation.public_id` from server        |
| Browser is message source | WhatsApp / IG webhook                       |
| One chat widget           | Many channels                               |
| No auth                   | Brand-scoped conversations                  |
| Simple unique constraint  | `(spur_user_id, channel, external_user_id)` |

So in the assignment:

* you **accept sessionId from client**
* you **unique it**
* you **persist messages under it**

In production:

* backend **generates sessionId**
* backend **never trusts client identity**
* sessionId is derived from real external identity

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Error Handling & Robustness

This service is designed to **fail gracefully for AI-related issues** while **failing loudly for system invariants**, keeping the chat UX stable without hiding real bugs.

### Error Categories & Handling Strategy

#### 1. LLM / AI Generation Errors (Graceful Degradation)

Failures related to AI response generation are treated as **non-fatal**. These include:

* LLM provider timeouts or rate limits
* Empty or invalid LLM responses
* Prompt construction bugs
* SDK / provider-level exceptions

**Handling approach:**

* All AI-related logic (prompt building, LLM call, response parsing) is wrapped inside a dedicated `generate_agent_reply` function.
* Any unexpected exception inside this boundary is converted into a domain-level `LLMError`.
* The API **does not return an HTTP error** for these cases.
* Instead, a friendly fallback message is returned to the user (e.g. *“Having trouble responding right now.”*).
* Full error details and stack traces are logged server-side for debugging.

**Rationale:**
LLM failures are not user-actionable, and the chat experience should not break due to transient or provider-side issues.

---

#### 2. System / Invariant Errors (Fail Loudly)

Errors that indicate a broken system state are **not swallowed**. These include:

* Invalid or malformed `session_id`
* Database errors (conversation creation, message persistence)
* History fetch failures
* Transaction or invariant violations

**Handling approach:**

* These errors are allowed to bubble up naturally.
* The request fails with an HTTP 500 response.
* The frontend can surface a generic error message.
* No partial or inconsistent state is silently persisted.

**Rationale:**
If core system invariants are broken, continuing the chat would risk data corruption or misleading behavior. Failing loudly makes such issues immediately visible and debuggable.

---

### Design Principle

> Graceful handling is applied only to unreliable external dependencies (LLMs),
> not to internal system invariants.

This separation ensures:

* A stable and user-friendly chat experience
* Clear operational visibility for real bugs
* No silent corruption or hidden failures

---

### Frontend Impact

* All successful API responses are treated as AI messages.
* Frontend-generated `"system"` messages are used only for network or request-level failures.
* No provider-specific or sensitive error details are exposed to users.

---

### Future Improvements

With more time, this design can be extended to:

* Structured error codes for observability
* Retry with backoff for specific LLM failures
* Metrics and alerting around AI failure rates

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


















