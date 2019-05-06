import json
from users.models import User
from django.views.generic import View
from .mixins import CSRFExemptMixin
from carousel.mixins import HttpResponseMixin
from users.forms import UserForm
from .utils import is_json


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
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'User not found'})
            return self.render_to_response(error_data, status=404)

        # new_data = {}
        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            data[key] = value

        form = UserForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'Something'})
        return self.render_to_response(json_data)

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'User not found'})
            return self.render_to_response(error_data, status=404)
        deleted_, item_deleted = obj.delete()
        print(deleted_)
        if deleted_ == 1:
            json_data = json.dumps({'message': 'Successfully deleted'})
            return self.render_to_response(json_data, status=200)

        error_data = json.dumps({'message': 'Could not delete item. Please try again.'})
        return self.render_to_response(error_data, status=400)


# List(Retrieve, Detail), Create, Update, Delete Endpoint

class UserListAPIView(HttpResponseMixin, CSRFExemptMixin, View):

    is_json = True
    queryet = None

    def get_queryset(self):
        qs = User.objects.all()
        self.queryset = qs
        return qs

    def get_object(self, id=None):
        if id is None:
            return None
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        passed_id = data.get('id', None)
        if passed_id is not None:
            obj = self.get_object(id=passed_id)
            if obj is None:
                error_data = json.dumps({'message': 'User not found'})
                return self.render_to_response(error_data, status=404)
            json_data = obj.serialize()
            return self.render_to_response(json_data)
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)
        data = json.loads(request.body)
        form = UserForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = json.dumps({'message': 'Now Allowed'})
        return self.render_to_response(data, status=400)

    # def delete(self, request, *args, **kwargs):
    #     data = json.dumps({'message': 'You cannot delete entire list'})
    #     return self.render_to_response(data, status=403)

    def put(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id', None)

        if not passed_id:
            error_data = json.dumps({'id': 'Required field to update'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(id=passed_id)
        if obj is None:
            error_data = json.dumps({'message': 'User not found'})
            return self.render_to_response(error_data, status=404)

        # new_data = {}
        data = json.loads(obj.serialize())
        for key, value in passed_data.items():
            data[key] = value

        form = UserForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'Something'})
        return self.render_to_response(json_data)

    def delete(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id', None)

        if not passed_id:
            error_data = json.dumps({'id': 'Required field to update'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(id=passed_id)
        if obj is None:
            error_data = json.dumps({'message': 'User not found'})
            return self.render_to_response(error_data, status=404)

        deleted_, item_deleted = obj.delete()
        print(deleted_)
        if deleted_ == 1:
            json_data = json.dumps({'message': 'Successfully deleted'})
            return self.render_to_response(json_data, status=200)

        error_data = json.dumps({'message': 'Could not delete item. Please try again.'})
        return self.render_to_response(error_data, status=400)
