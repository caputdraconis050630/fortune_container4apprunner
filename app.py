from flask import Flask, render_template, request, jsonify
import boto3
import json
from datetime import datetime

app = Flask(__name__)

# Amazon Bedrock 클라이언트 설정
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # 사용하는 리전에 맞게 변경하세요
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        calendar_type = request.form['calendar_type']
        birth_time = request.form['birth_time']
        fortune_type = request.form['fortune_type']

        input_data = f"이름: {name}, 생년월일: {birth_date} ({calendar_type}), 태어난 시각: {birth_time}, 운세 유형: {fortune_type}"

        prompt = f"""
        다음은 신년 운세를 알아보고자 하는 사람의 정보입니다:
        {input_data}
        이 정보를 바탕으로 2025년의 {fortune_type}에 대한 상세한 운세를 작성해주세요.
        운세는 긍정적이고 희망적인 내용으로, 구체적인 조언과 함께 작성해주세요.
        결과는 다음 형식으로 제시해주세요:

        ## 2025년 {name}님의 {fortune_type}

        [여기에 상세한 운세 내용을 작성해주세요]

        ### 행운의 숫자: [1에서 99 사이의 숫자]
        ### 행운의 색: [색상]
        ### 행운의 방향: [동서남북 중 하나]
        """

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "temperature": 0.5,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            })
        )

        model_response = json.loads(response["body"].read())
        fortune = model_response["content"][0]["text"]

        return jsonify({'fortune': fortune})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

