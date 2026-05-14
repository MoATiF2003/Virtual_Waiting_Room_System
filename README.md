# Virtual Waiting Room System

A real-time virtual waiting room simulation built using **FastAPI**, **Python OOP**, **HTML**, **CSS**, and **JavaScript**.

This project simulates how large-scale platforms manage heavy incoming traffic using:
- active session limits
- FIFO waiting queues
- controlled admission rates
- automatic session expiration
- live dashboard monitoring

---

# Features

## Gateway Admission Logic
Users are admitted only if server capacity is available.

```python
if active_users < MAX_CAPACITY:
    allow user
else:
    send to waiting queue