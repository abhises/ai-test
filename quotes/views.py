from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuoteRequestSerializer, GeneratedQuoteSerializer
from .models import GeneratedQuote
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os

# Load HuggingFace token
HF_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_API_TOKEN is missing! Please set it in your .env file.")

# Initialize HuggingFace model
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.7,
    max_new_tokens=256,
)
model = ChatHuggingFace(llm=llm)


class GenerateQuoteView(APIView):
    def post(self, request):
        serializer = QuoteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        topic = serializer.validated_data["topic"]
        tone = serializer.validated_data.get("tone", "inspirational")

        prompt = f"Generate one {tone} quote about {topic}. Keep it to one sentence."

        try:
            response = model.invoke(prompt)
            quote_text = response.content.strip()

            saved = GeneratedQuote.objects.create(
                topic=topic,
                tone=tone,
                quote=quote_text
            )

            # Serialize and return the saved object
            output_serializer = GeneratedQuoteSerializer(saved)
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            print("\n\n------ LLM ERROR ------")
            traceback.print_exc()
            print("------ END ERROR ------\n\n")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuoteListView(APIView):
    def get(self, request):
        quotes = GeneratedQuote.objects.all().order_by("-created_at")
        serializer = GeneratedQuoteSerializer(quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
