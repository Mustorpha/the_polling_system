from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views import View
from django.db.models import Sum
from .models import Lga, PollingUnit, AnnouncedPuResults

def index(request):
    return render(request, 'collation/index.html')


class PollingUnitListView(ListView):
    model = PollingUnit
    template_name = 'collation/poll_total.html'
    context_object_name = 'selected_polling_unit'

    def get_queryset(self):
        return PollingUnit.objects.exclude(polling_unit_number__exact='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polling_unit_id = self.request.GET.get('polling_unit_id')
        # print("Polling Unit ID:", polling_unit_id)
        
        if polling_unit_id and polling_unit_id.lower() != 'all':
            selected_polling_unit = PollingUnit.objects.filter(pk=polling_unit_id).first()
            context['selected_polling_unit'] = selected_polling_unit
            results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=polling_unit_id)
            context['results'] = results
        elif polling_unit_id and polling_unit_id.lower() == 'all':
            all_results = AnnouncedPuResults.objects.values('party_abbreviation').annotate(total_score=Sum('party_score'))
            context['all_results'] = all_results

        context['polling_units'] = PollingUnit.objects.exclude(polling_unit_number__exact='')

        return context

class LgaTotalResultView(TemplateView):
    template_name = 'collation/lga_sum_total.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lgas'] = Lga.objects.all()
        selected_lga_id = self.request.GET.get('lga_id')

        if selected_lga_id:
            selected_lga = Lga.objects.filter(uniqueid=selected_lga_id).first()
            context['selected_lga'] = selected_lga
            total_results = (
                AnnouncedPuResults.objects
                .filter(polling_unit_uniqueid__in=PollingUnit.objects.filter(lga_id=selected_lga_id).values('uniqueid'))
                .values('party_abbreviation')
                .annotate(total_score=Sum('party_score'))
            )
            context['total_results'] = total_results

        return context

class AddPollUnitResultView(View):
    template_name = 'collation/poll_add.html'

    def get(self, request, *args, **kwargs):
        polling_units = PollingUnit.objects.all()
        return render(request, self.template_name, {'polling_units': polling_units})

    def post(self, request, *args, **kwargs):
        polling_unit_number = request.POST.get('polling_unit_number')
        ward_id = request.POST.get('ward_id')
        lga_id = request.POST.get('lga_id')
        uniquewardid = request.POST.get('uniquewardid')
        polling_unit_name = request.POST.get('polling_unit_name')
        polling_unit_description = request.POST.get('polling_unit_description')
        lat = request.POST.get('lat')
        long = request.POST.get('long')

        party_abbreviation = request.POST.get('party_abbreviation')
        party_score = request.POST.get('party_score')
        entered_by_user = request.POST.get('entered_by_user')
        if (
            polling_unit_number and ward_id and lga_id and party_abbreviation and party_score and
            entered_by_user
        ):
            new_polling_unit = PollingUnit(
                polling_unit_number=polling_unit_number,
                ward_id=ward_id,
                lga_id=lga_id,
                uniquewardid=uniquewardid,
                polling_unit_name=polling_unit_name,
                polling_unit_description=polling_unit_description,
                lat=lat,
                long=long,
                entered_by_user=entered_by_user,
            )
            new_polling_unit.save()
            new_result = AnnouncedPuResults(
                polling_unit_uniqueid=new_polling_unit.uniqueid,
                party_abbreviation=party_abbreviation,
                party_score=party_score,
                entered_by_user=entered_by_user,
            )
            new_result.save()

            return redirect('poll_result') 

        polling_units = PollingUnit.objects.all()
        return render(request, self.template_name, {'polling_units': polling_units})
