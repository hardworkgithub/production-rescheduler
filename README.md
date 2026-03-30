#  Production Rescheduler

## What is this project?

This project is about solving a real problem in manufacturing.

In factories, multiple projects run at the same time but machines are limited. Sometimes priority changes or machines are not available, so scheduling becomes difficult.

So I built a system which automatically creates the best schedule using AI (optimization).

---

## What I have done

I created a full working system using:

* React (frontend UI)
* Django (backend API)
* OR-Tools (for optimization logic)

When user clicks a scenario in UI, the data goes to backend, optimization runs, and the best schedule is returned with delay and cost.

---

## How it works (simple)

The system tries to:

👉 minimize total delay cost

It considers:

* project priority (low / medium / high)
* delay penalty per day
* machine availability
* maintenance time
* operation duration

---

## Logic used

* High priority + high penalty → scheduled first
* Machine cannot run 2 operations at same time
* Maintenance time is blocked
* If delay is unavoidable → low priority project is delayed

---

## Example Input

Projects:

* P1 → medium priority, due day 10, penalty ₹5000
* P2 → high priority, due day 7, penalty ₹20000
* P3 → low priority, due day 12, penalty ₹2000

Machines:

* M1 → CNC (maintenance Day 5–6)
* M2 → CNC
* M3 → VMC

Operations:

* OP1_P1 → duration 6 days
* OP1_P2 → duration 6 days
* OP1_P3 → duration 6 days

---

## Example Output

```
P2 → Day 0–6 → no delay  
P3 → Day 6–12 → no delay  
P1 → Day 6–12 → delay 2 days → cost ₹10,000
```

Total Cost = ₹10,000

---

## Why this output comes

Total work is more than machine capacity, so delay is unavoidable.

The system schedules P2 first because it has highest penalty.
Then P3 and P1 are scheduled.

P1 is delayed because its penalty is lower compared to P2.

---

## Features

* Automatic scheduling using optimization
* Handles priority changes
* Handles machine constraints
* Shows delay and cost clearly

---

## API Endpoint

POST request:

/api/reschedule/

---

## Tech Used

* React
* Django
* OR-Tools

---

## How to Run

Backend:

pip install -r requirements.txt
python manage.py runserver

Frontend:

npm install
npm start

---

## Final

This project shows how AI can be used to solve real scheduling problems instead of manual planning.
