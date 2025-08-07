from rest_framework import serializers

class EmployeesSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=50)
    phone=serializers.CharField(max_length=15)
    city=serializers.CharField(max_length=50)

    def update(self, instance, validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.phone=validated_data.get('phone',instance.phone)
        instance.city=validated_data.get('city',instance.city)
        instance.save()
        return instance
    

    
