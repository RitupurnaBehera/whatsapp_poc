import requests
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class CreateFlowView(View):
    def post(self, request):
        try:
            breakpoint()
            body = json.loads(request.body.decode('utf-8'))
            flow_name = body.get('name')
            categories = body.get('categories')
            clone_flow_id = body.get('clone_flow_id')
            endpoint_uri = request.build_absolute_uri('/handle-flow-response/')

            url = f"{settings.BASE_URL}/{settings.WABA_ID}/flows"

            headers = {
                'Authorization': f'Bearer {settings.ACCESS_TOKEN}',
                'Content-Type': 'application/json'
            }

            data = {
                'name': flow_name,
                'categories': categories,
                'clone_flow_id': clone_flow_id,
                'endpoint_uri': endpoint_uri
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return JsonResponse(response.json(), status=200)
            else:
                return JsonResponse(response.json(), status=response.status_code)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        
@method_decorator(csrf_exempt, name='dispatch')    
def handle_flow_response(request):
    breakpoint()
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # Example: Handle sign-up flow response
        if 'flow_name' in data and data['flow_name'] == 'sign_up':
            customer_name = data.get('customer_name')
            customer_email = data.get('customer_email')
            # Process sign-up data, e.g., save to the database

        # Handle other types of flows as needed

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failure'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class WebhookVerificationView(View):
    def get(self, request):
        breakpoint()
        # Webhook verification process
        verify_token = 'Reetu'
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == verify_token:
                return HttpResponse(challenge, status=200)
            else:
                return HttpResponse("Bad Request", status=403)

        return HttpResponse(status=404)
    
    def post(self, request):
        try:
            breakpoint()
            body = json.loads(request.body.decode('utf-8'))
            print(f"Received POST data: {body}")

            # Handle the incoming JSON payload
            if 'message' in body:
                message = body['message']
                print(f"Message: {message}")

            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            print("Failed to decode JSON")
            return JsonResponse({'status': 'invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error handling webhook: {e}")
            return JsonResponse({'status': 'error'}, status=500)