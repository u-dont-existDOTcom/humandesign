FROM python:3.12-slim
WORKDIR /app
COPY apps/life-patterns-participant/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY apps/life-patterns-participant/participant /app/participant
COPY tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md /app/authority/
COPY tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json /app/authority/
COPY tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json /app/authority/
COPY tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md /app/authority/
ENV PYTHONUNBUFFERED=1
CMD ["sh", "-c", "exec uvicorn participant.app:factory --factory --host 0.0.0.0 --port ${PORT:-8000} --workers 1 --no-access-log"]
