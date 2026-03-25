## Step 1 — Perfect. Fixed shift blocks makes this *way* more buildable

Having mostly standardized shifts is a gift because it turns scheduling from “infinite possibilities” into a clean **constraint problem**.

Your default shift templates are basically:

* **Open:** 9–5
* **Mid:** 10–6 *or* 11–7
* **Close:** 1:15–9:15

And “custom shifts” are exceptions we can ignore in MVP (or treat as manual overrides later).

That’s exactly how you keep this project **tight** and still impressive.

---

## Step 2 — MVP scope that demos your whole stack (and stays realistic)

### MVP goal

**Handle disruptions** (call-outs / availability changes) for a single day and suggest replacements that respect Twin Liquors rules.

### Core rules (v1)

* Must fill: **1 opener + 1 closer** minimum
* On **Friday/Saturday**: must have **2 closers**
* Prefer replacements in this order:

  1. **Floaters**
  2. Dedicated employees at **same store**
  3. Dedicated employees at **other stores** (last resort)
  4. **Managers** (emergency last resort)
* Employee must be **available** for that shift block

That alone is a strong demo.

---

## Step 3 — Where each tech fits (so you can “check the boxes” from job posts)

### Postgres (system of record)

Tables (minimal):

* `employees` (phone, role: floater/dedicated/manager, home_store)
* `availability` (date + shift_type or time windows)
* `schedule` (date, store_id, shift_type, employee_id)
* `events` (callout, late, availability_change)
* `recommendations` (ranked suggestions + reasoning)

### Chroma (RAG)

Store:

* store rules (“Fri/Sat needs 2 closers”, “closers always 1:15–9:15”)
* policies (“custom shifts must be approved”)
* maybe “notes” about employees (optional)

Then for a call-out, you run a retrieval like:

> “Twin Liquors coverage rules for Friday close shift”

…and feed that context to the AI explanation + message drafting.

### OpenAI (LLM)

Use it for:

* **intent classification** of text (“call-out” vs “late” vs “swap”)
* **entity extraction** (which day/shift/store if mentioned)
* **explanations** (“why Maria is the best choice”)
* **message drafting** (group message asking for coverage)

### n8n (orchestration)

Workflow example:

1. Receive event webhook from FastAPI (call-out)
2. HTTP → FastAPI “get recommendations”
3. HTTP → FastAPI “draft group text”
4. Slack → notify manager with ranked list + draft message
5. (later) optional: send SMS via Twilio

### Docker

Run locally with:

* FastAPI
* Postgres
* n8n
* (Chroma embedded or small service)

This is the “AI integration engineer” stack in a nutshell.

---

## Step 4 — The exact demo scenario you’ll show in interviews

**Input:** (simulated SMS)

> “Can’t make it tonight, sorry”

System:

1. Maps phone → employee
2. Looks up schedule: they were the **closer**
3. Applies rule: if Fri/Sat, ensure **2 closers**
4. Finds replacements based on floater/dedicated/manager ladder
5. Produces:

* **Top 3 candidates**
* **Reasoning**
* **Draft group text**

Then n8n posts to Slack:

> “Call-out detected for Store 2 close (1:15–9:15). Suggested: Maria (floater)… Draft text: ‘Anyone available to cover…’”

That’s a clean, end-to-end AI workflow.

---

## Step 5 — One key design decision (and I’ll pick a default)

Since you’re SMS-based today, but SMS integration adds setup, the MVP should do:

✅ **Simulated SMS endpoint**
`POST /sms/incoming { phone, message }`

Later you swap that for Twilio with almost no changes.

---

## Step 6 — Two small questions to finalize your “Twin Liquors model”

1. **Store hours:** is 9–9:15 consistent for all stores every day, or do some stores close earlier on some days?
2. For Friday/Saturday “2 closers” — does that mean **two people on the close shift**, or **one closer + one mid that stays late**?

Answer those and I’ll write your “v1 spec” in a tight format:

* constraints
* tables
* endpoints
* n8n workflow nodes
  So when you get back to your computer, you can execute immediately.
