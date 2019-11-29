from django.test import TestCase
from base.models import OnOffStatusModel
from .mixins import AbstractModelMixinTestCase


class TestOnOffStatusModel(AbstractModelMixinTestCase):
    
    mixin = OnOffStatusModel

    def setUp(self):
        self.model_on = self.model.objects.create()
        self.model_off = self.model.objects.create(status=self.model.OFF)

    def test_correct_status_fields(self):
        self.assertEqual(self.model_on.status, self.model.ON)
        self.assertEqual(self.model_off.status, self.model.OFF)

    def test_objects_on_manager(self):
        self.assertEqual(self.model.objects_on.count(), 1)
        self.assertEqual(self.model.objects_on.all()[0], self.model_on)