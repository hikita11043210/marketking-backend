from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...services.translator import TranslatorService

class TranslatorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        テキストを翻訳する

        Request Body:
            - text: str - 翻訳対象のテキスト
            - target_lang: str - 翻訳先の言語コード（オプション、デフォルト: 'EN-US'）

        Returns:
            ApiResponse形式のレスポンス
        """
        text = request.query_params.get('text')
        target_lang = request.query_params.get('target_lang', 'EN-US')

        if not text:
            return Response({
                'success': True,
                'message': '翻訳するテキストを指定してください。',
                'data': {
                    'translated_text': text,
                    'target_lang': target_lang
                }
            })

        try:
            service = TranslatorService(request.user)
            result = service.translate_text(text, target_lang)

            return Response({
                'success': True,
                'message': '翻訳が完了しました。',
                'data': result
            })

        except ValueError as e:
            return Response({
                'success': True,
                'message': str(e),
                'data': {
                    'translated_text': text,
                    'target_lang': target_lang
                }
            })

        except Exception as e:
            return Response({
                'success': True,
                'message': str(e),
                'data': {
                    'translated_text': text,
                    'target_lang': target_lang
                }
            }) 