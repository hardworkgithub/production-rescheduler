from rest_framework.decorators import api_view
from rest_framework.response import Response
from .optimizer import reschedule_full

@api_view(['POST'])
def api_reschedule(request):
    data = request.data
    schedule, analysis = reschedule_full(
        data.get('projects', []),
        data.get('machines', []),
        data.get('operations', []),
        data.get('disruption')
    )
    return Response({
        'schedule': schedule,
        'analysis': analysis,
        'input_summary': {
            'projects': len(data.get('projects', [])),
            'machines': len(data.get('machines', [])),
            'operations': len(data.get('operations', []))
        }
    })