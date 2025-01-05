# Python 3.12 이미지를 기반으로 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일들을 컨테이너로 복사
COPY requirements.txt .
COPY app.py .
COPY templates templates/

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# AWS CLI 설치 (Boto3 사용을 위해)
RUN apt-get update && apt-get install -y awscli

# 5000 포트 노출 (Flask의 기본 포트)
EXPOSE 5000

# 환경 변수 설정
ENV AWS_DEFAULT_REGION=us-east-1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 애플리케이션 실행
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
