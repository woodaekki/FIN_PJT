from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import openai
import os
from dotenv import load_dotenv

# 상위 폴더로 이동하여 .env 호출
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path)
openai.api_key = os.getenv('OPENAI_API_KEY')
# print(openai.api_key)

@api_view(['POST'])
def chatbot(request):
    message = request.data.get('message')
    response = openai.ChatCompletion.create(
        # model="gpt-4o",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": 
                "당신은 최신 금융 정보를 제공하는 챗봇입니다. "
                "사용 대상은 금융 지식이 부족한 사회 초년생입니다. "
                "따라서 한국의 금융 특성을 반영하여 20~30대가 쉽게 이해할 수 있도록 설명해주세요. "
                "답변은 짧고 요약된 형태로 제공하되, 사용자가 요청할 경우 자세히 설명해주세요. "
                "한국어로 대답하고, 가독성을 높이기 위해 적절한 줄바꿈을 사용하세요."
             },
            {"role": "user", "content": message}
        ]
    )

    # OpenAI API가 준 전체 응답 객체의 첫번째 메시지만 반환
    answer = response.choices[0].message['content']
    return Response({'response': answer}, status=status.HTTP_200_OK)
