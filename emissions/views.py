import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    EmissionRecord,
    DataSource
)

from .serializers import (
    EmissionRecordSerializer
)


@api_view(['GET'])
def get_records(request):

    records = EmissionRecord.objects.all()

    serializer = EmissionRecordSerializer(
        records,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def upload_csv(request):

    if request.method == 'GET':
        return Response({
            "message":
            "Upload CSV using POST request"
        })

    uploaded_file = request.FILES.get('file')

    if uploaded_file is None:
        return Response(
            {"error": "No file uploaded"},
            status=400
        )

    try:
        df = pd.read_csv(uploaded_file)

        source = DataSource.objects.create(
            source_type='SAP'
        )

        for _, row in df.iterrows():

            EmissionRecord.objects.create(
                source=source,
                category=row.get(
                    'category',
                    'Unknown'
                ),
                quantity=row.get(
                    'quantity',
                    0
                ),
                unit=row.get(
                    'unit',
                    'N/A'
                ),
                date=row.get(
                    'date'
                )
            )

        return Response({
            "message":
            "CSV uploaded successfully"
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=500
        )
@api_view(['POST'])
def update_status(request, record_id):

    try:
        record = EmissionRecord.objects.get(
            id=record_id
        )

        status = request.data.get(
            'status'
        )

        if status:
            record.status = status
            record.save()

        serializer = EmissionRecordSerializer(
            record
        )

        return Response(serializer.data)

    except EmissionRecord.DoesNotExist:
        return Response(
            {"error": "Record not found"},
            status=404
        )