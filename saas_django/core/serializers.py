from rest_framework import serializers


 # Overrides the get_queryset method to filter the results
class CompanySafeRelatedField(serializers.HyperlinkedRelatedField):
    # queryset only returns values for the company
    def get_queryset(self):
        request = self.context['request']
        company_id = request.user.company_id
        return super().get_queryset().filter(company_id=company_id)

# Assigns CompanySafeRelatedFIeld to serializer_related_field
class CompanySafeSerializerMixin(object):
     # Mixin used with HyperlinkedRelatedFIeld ensures that only company values are returned
     serializer_related_field = CompanySafeRelatedField
