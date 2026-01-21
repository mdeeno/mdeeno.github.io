import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 내 API 키로 사용 가능한 모델 리스트:")
print("-" * 30)
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"👉 {m.name}")
except Exception as e:
    print(f"❌ 목록 조회 실패: {e}")
print("-" * 30)