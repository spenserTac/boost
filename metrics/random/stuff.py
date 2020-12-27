from boost.metrics.models import SignUpMetricModel

stuff = SignUpMetricModel.objects.all()

for i in stuff:
    print(i.date)
