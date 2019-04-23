import json
from users.models import User
from django.views.generic import View
from django.http import HttpResponse
from .mixins import CSRFExemptMixin
from carousel.mixins import HttpResponseMixin
from users.forms import UserForm


# Retrieve, Update, Delete Endpoint

class UserDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):

    is_json = True

    def get_object(self, id=None):
        qs = User.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'User not found'})
            return self.render_to_response(error_data, status=404)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps({'message': 'Not allowed, please use the /api/users/ endpoint'})
        return self.render_to_response(json_data, status=403)

    def put(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'User not found'})
            return self.render_to_response(error_data, status=404)
        # print(dir(request))
        print(request.body)
        new_data = json.loads(request.body)
        print(new_data['email'])
        json_data = json.dumps({'message': 'Something'})
        return self.render_to_response(json_data)

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'User not found'})
            return self.render_to_response(error_data, status=404)
        json_data = json.dumps({'message': 'Something'})
        return self.render_to_response(json_data, status=403)


# List & Create Endpoint

class UserListAPIView(HttpResponseMixin, CSRFExemptMixin, View):

    is_json = True

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        json_data = qs.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = json.dumps({'message': 'Now Allowed'})
        return self.render_to_response(data, status=400)

    def delete(self, request, *args, **kwargs):
        data = json.dumps({'message': 'You cannot delete entire list'})
        return self.render_to_response(data, status=403)
