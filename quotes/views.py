import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuoteRequestSerializer
from .models import GeneratedQuote

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


# --------------------------------------------------------
# Load HF Token
# --------------------------------------------------------
HF_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_API_TOKEN is missing! Please set it in your .env file.")


# --------------------------------------------------------
# Initialize HuggingFace Chat Model
# --------------------------------------------------------
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",   # <-- FIXED MODEL
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.7,
    max_new_tokens=256,
)

model = ChatHuggingFace(llm=llm)


# --------------------------------------------------------
# Generate Quote View
# --------------------------------------------------------
class GenerateQuoteView(APIView):
    def post(self, request):
        serializer = QuoteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        topic = serializer.validated_data["topic"]
        tone = serializer.validated_data.get("tone", "inspiring")

        prompt = f"Generate one {tone} quote about {topic}. Keep it to one sentence."

        try:
            response = model.invoke(prompt)
            quote_text = response.content.strip()

            saved = GeneratedQuote.objects.create(
                topic=topic,
                tone=tone,
                quote=quote_text
            )

            return Response(
                {"id": saved.id, "quote": quote_text},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            import traceback
            print("\n\n------ LLM ERROR ------")
            traceback.print_exc()
            print("------ END ERROR ------\n\n")

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# --------------------------------------------------------
# List Quotes View
# --------------------------------------------------------
class QuoteListView(APIView):
    def get(self, request):
        data = list(
            GeneratedQuote.objects.all().order_by("-created_at").values()
        )
        return Response(data, status=status.HTTP_200_OK)
