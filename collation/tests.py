from django.test import TestCase
from django.urls import reverse
from .models import PollingUnit, AnnouncedPuResults

class PollingUnitListViewTest(TestCase):
    def setUp(self):
        PollingUnit.objects.create(polling_unit_number='001', ward_id=1, lga_id=1, entered_by_user='Admin')

    def test_polling_unit_list_view(self):
        response = self.client.get(reverse('yourapp:polling_unit_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '001') 
        self.assertTemplateUsed(response, 'polling_unit_list.html')

class AddPollingUnitResultViewTest(TestCase):
    def setUp(self):
        # Create test data for PollingUnit
        PollingUnit.objects.create(polling_unit_number='001', ward_id=1, lga_id=1, entered_by_user='Admin')

    def test_add_polling_unit_result_view(self):
        data = {
            'polling_unit_number': '002',
            'ward_id': 2,
            'lga_id': 2,
            'uniquewardid': None,
            'polling_unit_name': 'Test Polling Unit',
            'polling_unit_description': 'Test Description',
            'lat': '40.7128',
            'long': '-74.0060',
            'party_abbreviation': 'TEST',
            'party_score': 50,
            'entered_by_user': 'Admin',
        }

        response = self.client.post(reverse('yourapp:add_polling_unit_result'), data)
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check if the new PollingUnit and AnnouncedPuResults have been created
        self.assertEqual(PollingUnit.objects.count(), 2)
        self.assertEqual(AnnouncedPuResults.objects.count(), 1)

