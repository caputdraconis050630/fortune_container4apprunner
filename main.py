import streamlit as st
import boto3
import json
from datetime import datetime

st.title("엉터리 신년 운세")

# Amazon Bedrock 클라이언트 설정
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # 사용하는 리전에 맞게 변경하세요
)

# 사용자 입력 받기
name = st.text_input("이름을 입력하세요")
birth_date = st.date_input("생년월일을 선택하세요", min_value=datetime(1900, 1, 1))
calendar_type = st.radio("달력 유형", ["양력", "음력"])
birth_time = st.time_input("태어난 시각을 선택하세요")
fortune_type = st.selectbox("보고 싶은 운세를 선택하세요", ["종합운", "재물운", "연애운", "건강운", "학업운"])

if st.button("운세 보기"):
    if name and birth_date and birth_time and fortune_type:
        # 입력 데이터 준비
        input_data = f"이름: {name}, 생년월일: {birth_date} ({calendar_type}), 태어난 시각: {birth_time}, 운세 유형: {fortune_type}"
        
        # Bedrock에 요청할 프롬프트 생성
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

        # Bedrock에 요청 보내기
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",  # 또는 다른 적절한 모델 ID
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

        # 응답 처리
        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        fortune = model_response["content"][0]["text"]

        # 결과 표시
        st.markdown(fortune)
    else:
        st.warning("모든 필드를 입력해주세요.")
